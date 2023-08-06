import numpy as np
import distance
from albert.pipeline import AlbertConfigurableBaseEstimator
from sklearn.pipeline import TransformerMixin
from albert.internal.utils import convert_dynamic_schema_to_python_types
from albert.api.apis.tags import prediction_models_api
from albert.utils import *


class BinAssign(AlbertConfigurableBaseEstimator, TransformerMixin):
    """
    Assigns each OPC value to the corresponding bin
    """

    def __init__(self):
        super().__init__()

    @staticmethod
    def assign(value, data_type, bin_dict):
        """
        value: each opc_value from json
        data_type: each opc_value's data type (string or number)
        bin_dict: dictionary for each operating condition value
        """

        bins = bin_dict[data_type]
        if data_type == 'string':
            # Check if the bins are list or dict for backward compatibility
            if type(bins) == dict:
                assigned_bin = np.nan
                for k, v in bins.items():
                    if value in v:
                        assigned_bin = k
            else:
                match = [distance.levenshtein(i, value) for i in bins]
                assigned_bin = bins[match.index(min(match))]

        elif data_type == 'number':
            if value == '':
                assigned_bin = 'nan'
            else:
                if 'nan' in bins:
                    # Remove nan from assignable bins when value is numeric
                    bins = sorted([x for x in bins if x != 'nan'])
                if len(bins) == 0:
                    # Catches numerical user inputs when the model was not trained with numbers for this opc
                    assigned_bin = 'nan'
                elif float(value) < bins[0]:
                    # Catches cases where value is smaller than first bin label
                    assigned_bin = bins[0]
                elif float(value) >= bins[-1]:
                    # Catches cases where value is greater than last bin label
                    assigned_bin = bins[-1]
                else:
                    # Looks through sorted list for first bin greater than value and selects prior bin
                    assigned_bin_idx = next(idx for idx, val in enumerate(sorted(bins)) if val > float(value)) - 1
                    next_bin_idx = assigned_bin_idx + 1
                    assigned_bin_diff = abs(float(value) - bins[assigned_bin_idx])
                    next_bin_diff = abs(bins[next_bin_idx] - float(value))
                    # NOTE: closeness THRESHOLD for bumping value up to next bin
                    if not (next_bin_diff < assigned_bin_diff and next_bin_diff < bins[next_bin_idx] * 0.02):
                        assigned_bin = bins[assigned_bin_idx]
                    else:
                        assigned_bin = bins[next_bin_idx]

        else:
            raise Exception("Unable to get bin datatype")
        return assigned_bin

    def transform(self, payload: dict[str]) -> dict[str]:
        try:
            data = payload['data']

            audit_flag = payload['auditFlag']

            inputJSON = payload

            if 'bin_labels' not in inputJSON.keys() :
                modelID = inputJSON['data'][0]['modelId']
                modelVersion = inputJSON['data'][0]['modelVersion']
                response = prediction_models_api.GetModelByVersion(
                    self.config.session.client
                ).get_model_by_version(
                    path_params={"parentId": modelID, "id": modelVersion})
                response = convert_dynamic_schema_to_python_types(dict(response.body))
                bins = response['binlabels']
            else:
                bins = payload["bin_labels"]

            metadata_df, inputs_df = json_to_df_converter(data)
            cas_df = None

            # try:
            #     # Model prediction case (contains cas info)
            #     opc_df = inputs_df[inputs_df.albertId.isnull()]
            #     cas_df = inputs_df[inputs_df.albertId.notnull()]
            #
            # except:
            #     # Model build case (doesn't have any albertId's)
            #     opc_df = inputs_df

            if "albertId" in inputs_df:
                # Model prediction case (contains cas info)
                opc_df = inputs_df[inputs_df.albertId.isnull()]
                cas_df = inputs_df[inputs_df.albertId.notnull()]
            else:
                # Model build case (doesn't have any albertId's)
                opc_df = inputs_df


            def string_or_number(val):
                try:
                    if val is not None:
                        float(val)
                    return 'number'
                except:
                    return 'string'

            opc_df['dataType'] = opc_df['value'].apply(lambda x: string_or_number(x))
            # opc_df['dataType'] = opc_df['value'].apply (
            #     lambda x : 'number' if x is not None and isinstance (x, (int, float, np.int, np.floating)) else
            #     'string')

            opc_df['value'].replace({None: ""}, inplace=True)
            opc_df['value'].fillna('', inplace=True)

            val_list = []
            for value, data_type, name in zip(opc_df['value'], opc_df['dataType'], opc_df['name']):
                if name in bins.keys():
                    # check if data type is number or string
                    if data_type == 'number':
                        if 'number' in bins[name].keys():
                            val_list.append(BinAssign.assign(value, data_type, bins[name]))
                        else:
                            val_list.append('nan')
                    if data_type == 'string':
                        if 'string' in bins[name].keys():
                            val_list.append(BinAssign.assign(value, data_type, bins[name]))
                        else:
                            val_list.append('nan')
                else:
                    val_list.append(value)
                    audit_flag['hardFlag'] += [{"name": name, "value": "Input name not present in bin labels"}]

            opc_df['value'] = val_list

            opc_df.drop(columns=['dataType'], inplace=True)

            opc_df.replace({"": None, "nan": None, np.nan: None}, inplace=True)

            if metadata_df is not None:
                metadata_df.replace({"": None, np.nan: None}, inplace=True)

            if cas_df is not None:
                cas_df.replace({"": None, np.nan: None}, inplace=True)

                data = df_to_json_converter(metadata_df, opc_df, cas_df)

            else:
                data = df_to_json_converter(metadata_df, opc_df)

            response = {"data": data, "auditFlag": audit_flag}
            return response

        except Exception as e:
            raise ("failed to assign bins", str(e))
