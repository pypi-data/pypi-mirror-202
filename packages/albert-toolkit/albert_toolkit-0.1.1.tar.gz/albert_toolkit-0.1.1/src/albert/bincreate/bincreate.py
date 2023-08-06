import numpy as np
from sklearn.cluster import AgglomerativeClustering
from sklearn.feature_extraction.text import TfidfVectorizer
from albert.utils import *
import warnings
warnings.filterwarnings("ignore")


class BinCreator:

    def __init__(self):
        pass

    @staticmethod
    def equal_frequency_binning(vals, nbins):
        """
        Takes list of values and number of bins and returns equal frequency bins as sorted list
        """
        return np.interp(np.linspace(0, len(vals), nbins + 1),
                         np.arange(len(vals)),
                         np.sort(vals)).tolist()

    @staticmethod
    def max_nearest_neighbor_binning(value_list):
        # Catches empty lists and nan only lists
        if len(value_list) == 0 or all(np.isnan(x) for x in value_list):
            return []

        value_series = pd.Series(value_list)
        total = len(value_list)
        vals = value_series.value_counts().index.tolist()
        cts = value_series.value_counts().values.tolist()
        # Sort both lists to ascend by values
        vals, cts = (list(x) for x in zip(*sorted(zip(vals, cts))))
        sub_list = []
        subtotal = 0
        bins = []

        for idx, ct in enumerate(cts):
            sub_list.append(idx)
            subtotal += ct
            # NOTE:.1 is the bin threshold, it should be closely monitored
            if subtotal > total * .1:
                if len(sub_list) != 1:
                    # Find value with highest count across sub_list
                    bin_name = vals[cts.index(max([cts[x] for x in sub_list]))]
                else:
                    bin_name = vals[sub_list[0]]

                # Reset counters
                sub_list = []
                subtotal = 0

                bins.append(bin_name)

        return bins

    @staticmethod
    def oneBinFlag(bins, opcName):
        hard_flags = []
        if len(bins) <= 1:
            hard_flag = {"name": opcName,
                         "value": "Values does not have enough data points to warrant it's own bin"}

            if hard_flag and hard_flag not in hard_flags:
                hard_flags.append(hard_flag)

        return hard_flags

    @staticmethod
    def stringIntegerFlag(df):
        """
        String and numeric inputs in the same opc
        """
        soft_flags = []
        for i, row in df.iterrows():
            if len(row['dataType']) > +1:
                soft_flag = {"name": row['name'],
                             "value": "opc is mixture of string and integer"}

                if soft_flag and soft_flag not in soft_flags:
                    soft_flags.append(soft_flag)

        return soft_flags

        pass

    def transform(self, json_input: dict[str]) -> dict[str]:
        try:
            data = json_input['data']
            audit_flag = json_input['auditFlag']
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

            if "albertId" in inputs_df :
                # Model prediction case (contains cas info)
                opc_df = inputs_df[inputs_df.albertId.isnull()]
                cas_df = inputs_df[inputs_df.albertId.notnull()]
            else:
                # Model build case (doesn't have any albertId's)
                opc_df = inputs_df


            # Function to determine value type
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

            str_int_check = opc_df.groupby('name')['dataType'].apply(lambda x: list(set(x))).reset_index()

            str_int_flag = BinCreator.stringIntegerFlag(str_int_check)
            if str_int_flag is not None:
                audit_flag['softFlag'] = audit_flag['softFlag'] + str_int_flag

            # Separate values into string and number groups
            string_group = opc_df[opc_df.dataType == 'string'].groupby('name')['value'].apply(
                lambda x: list(set(x))).reset_index()
            number_group = opc_df[opc_df.dataType == 'number'].groupby('name')['value'].apply(
                lambda x: list(x)).reset_index()

            # Convert None's to nan's and number group values to floats
            number_group['value'] = number_group['value'].apply(lambda x: [y if y is not None else np.nan for y in x])
            number_group['value'] = number_group['value'].apply(lambda x: list(map(float, x)))

            bin_labels = {}
            # String binning
            for i, row in string_group.iterrows():
                cluster_maps = {}
                rows = [str(x) for x in row.value]
                if rows:
                    words = np.asarray(rows)  # So that indexing with a list will work
                    if len(words) < 10:
                        for wrd in words:
                            cluster_maps[wrd] = [wrd]

                        bin_labels[row['name']] = {'string': cluster_maps}
                    elif len(words) > 10:

                        vectorizer = TfidfVectorizer(analyzer='char')
                        X2 = vectorizer.fit_transform(np.unique(words))
                        scores = (X2.toarray())

                        frequency_table = pd.Series(words).value_counts().reset_index()
                        frequency_table = frequency_table.sort_values("index")
                        frequency_table.columns = ['word', "count"]

                        agglo = AgglomerativeClustering(n_clusters=max(1, len(np.unique(words)) // 3))

                        agglo.fit(scores)

                        frequency_table['cluster'] = agglo.labels_

                        group_cluster = frequency_table.groupby('cluster')['word'].apply(
                            lambda x: list(x)).reset_index()
                        group_cluster.columns = ["cluster", "word_list"]

                        binned_strs = frequency_table.sort_values('count').drop_duplicates(subset='cluster',
                                                                                           keep="first")

                        merged_frame = group_cluster.merge(binned_strs, how="outer")

                        for index, row_vals in merged_frame.iterrows():
                            word = row_vals.word
                            word_list = row_vals.word_list
                            cluster_maps[word] = word_list

                        one_bin_flag = BinCreator.oneBinFlag(list(words[agglo.labels_]), row['name'])
                        if one_bin_flag is not None:
                            audit_flag['hardFlag'] = audit_flag['hardFlag'] + one_bin_flag

                        bin_labels[row['name']] = {'string': cluster_maps}
                    else:
                        for wrd in words:
                            cluster_maps[wrd] = [wrd]
                        bin_labels[row['name']] = {'string': cluster_maps}

            for roww in opc_df.name.unique().tolist():
                if roww in bin_labels:
                    bin_labels[roww]["number"] = ["nan"]
                else:
                    bin_labels[roww] = {"number": ["nan"]}

            # Numerical binning
            for i, row in number_group.iterrows():
                opc_values = row.value
                # Remove None's when present
                non_nan_values = [x for x in opc_values if ~np.isnan(x)]
                if opc_values:
                    # NOTE: # of bins currently arbitrarily set to half the number of unique values
                    # nbins = math.ceil(len(set(opc_values))/2)
                    # bins = equal_frequency_binning(opc_values, nbins)
                    bins = BinCreator.max_nearest_neighbor_binning(non_nan_values)
                    # Add nan to bins when present
                    # if len(non_nan_values) != opc_values:
                    # bin_labels[row["name"]]["number"].append("nan")

                    bin_labels[row["name"]]["number"].extend(bins)

            opc_df = opc_df.replace({"": None})
            opc_df = opc_df.replace({np.nan: None})

            if cas_df is not None:
                cas_df = cas_df.replace({"": None})
                cas_df = cas_df.replace({np.nan: None})

                data = df_to_json_converter(metadata_df, opc_df, cas_df)

            else:
                data = df_to_json_converter(metadata_df, opc_df)

            response = {"data": data, "bin_labels": bin_labels,  "auditFlag": audit_flag}
            return response

        except Exception as e:
            raise ("failed to create bins", str(e))
