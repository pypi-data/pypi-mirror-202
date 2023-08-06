import numpy as np
import pint
import pkg_resources

from albert.pipeline import AlbertConfigurableBaseEstimator
from sklearn.pipeline import TransformerMixin
from albert.internal.utils import *
from albert.api.apis.tags import prediction_models_api


class UnitStandardization:
    """
    Takes experiment data and standardizes its operating condition
    parameter measurements based on the most popular unit per
    operating condition.
    Parameters:
    -----------
    operating condition data - json containing columns: opcValue, unitName,
    sopOperatingCondition
    unit dictionary -  with sopOperatingCondition's for keys and
    their most popular unit as values
    Returns:
    --------
    A json  with the same format as the passed-in  operating condition data
    with three new columns: standardized opcValue's, standardized
    opcUnits, and the Pint object these items are derived from.
    """

    def __init__(self, value: str, unit: str, name: str):
        if not isinstance(value, str):
            raise TypeError("Value must be a string")
        if not isinstance(unit, str):
            raise TypeError("Unit must be a string")
        if not isinstance(name, str):
            raise TypeError("Name must be a string")
        self.value = value
        self.unit = unit
        self.name = name
        self.ureg = pint.UnitRegistry(
            pkg_resources.resource_filename(
                __package__.split(".")[0], "resources/unit_registry_custom.txt"
            ),
            autoconvert_offset_to_baseunit=True,
        )
        self.Q_ = self.ureg.Quantity

    def unit_check(self):
        """
        Takes the input unit and check whether the unit is real
        Returns: The actual unit from Unit registry , if the unit is unreal the empty string returned
        """
        try:
            res = self.ureg.Quantity(self.unit.lower())
            if res is not None and res != "dimensionless":
                self.unit = str(res.units)
                return str(res.units)
            else:
                self.unit = ""
                return ""
        except:
            self.unit = ""
            return ""

    def unit_convert(self, unit_dict: dict):
        """
        Args:
            value: cleaned Value which entered by user
            unit: unit associated to the opc value entered
            name: represents the opc name
            unit_dict: which contains the opc name as a key and most used unit as a value for the conversion
        Returns: When opc name is in unit dict then value and unit converted into the most used unit only when the unit dimensionality identical
        """
        value = self.value
        unit = self.unit
        name = self.name
        try:
            quantity = self.Q_(float(value), str(unit).lower())
            if (str(unit) in self.ureg) or (str(unit).lower() in self.ureg):
                if name in unit_dict.keys():
                    # checking for the dimensionality of input unit and unit we need to convert
                    if str(self.Q_(str(unit).lower()).dimensionality) == str(
                        self.Q_(unit_dict[name].lower()).dimensionality
                    ):
                        res = quantity.to(unit_dict[name].lower())
                        self.value = str(round(res.magnitude, 2))
                        self.unit = str(res.units)
                        return self.value, self.unit
                    else:
                        return self.value, self.unit
                else:
                    return value, unit
            else:
                return value, unit
        except Exception as e:
            return value, unit

    def unit_convert_SI(self):
        """
        Args:
            value: cleaned Value which entered by user
            unit: unit associated to the opc value entered
            name: represents the opc name
            unit_dict: which contains the opc name as a key and most used unit as a value for the conversion
        Returns: When opc name is in unit dict then value and unit converted into the most used unit only when the unit dimensionality identical
        """
        value = self.value
        unit = self.unit
        name = self.name
        try:
            quantity = self.Q_(float(value), str(unit).lower())
            if (str(unit) in self.ureg) or (str(unit).lower() in self.ureg):
                res = quantity.to_base_units()
                self.value = str(round(res.magnitude, 2))
                self.unit = str(res.units)
                return self.value, self.unit
            else:
                return value, unit
        except Exception as e:
            return value, unit


class UnitConversion(AlbertConfigurableBaseEstimator, TransformerMixin):
    
    def __init__(self):
        super().__init__()
    
    def transform(self, payload: dict[str]) -> dict[str]:
        try:
            data = payload["data"]
            audit_flag = payload["auditFlag"]
            metadata_df, inputs_df = json_to_df_converter(data)
            cas_df = None

            if "smiles" in inputs_df.columns:
                pass
            else:
                inputs_df["smiles"] = np.nan

            # try:
            #     # Model prediction case (contains cas info)
            #     opc_df = inputs_df[inputs_df.albertId.isnull()]
            #     cas_df = inputs_df[inputs_df.albertId.notnull()]
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


            opc_df.replace({"": None, np.nan: None}, inplace=True)

            if metadata_df is not None:
                metadata_df.replace({"": None, np.nan: None}, inplace=True)

            # Condition to check for input unit_dict value
            if "unit_dict" not in payload.keys():
                modelID = payload["data"][0]["modelId"]
                modelVersion = payload["data"][0]["modelVersion"]
                response = prediction_models_api.GetModelByVersion(
                    self.config.session.client
                ).get_model_by_version(
                    path_params={"parentId": modelID, "id": modelVersion}
                )
                response = convert_dynamic_schema_to_python_types(dict(response.body))
                unit_dict = response["unitDictionary"]
            else:  # convert based on user specification
                unit_dict = payload["unit_dict"]
            audit_flag = {"softFlag": [], "hardFlag": []}
            if len(opc_df) != 0:
                # Replacing unit column results with dimensionless and none/null into empty string
                opc_df["unit"].replace(
                    ["dimensionless", "Unitless", "unitless", "None"], "", inplace=True
                )
                opc_df["unit"] = opc_df["unit"].fillna("")

                # Applying unit_convert to convert the value into required unit as mentioned with unit_dict
                opc_df[["value", "unit"]] = [UnitStandardization(value, unit, name).unit_convert(
                    unit_dict) for value, unit, name in zip(
                        opc_df["value"], opc_df["unit"], opc_df["name"]
                    )
                ]

                soft_flag, hard_flag = UnitConversion.checkAuditFlags(opc_df)

                if soft_flag:
                    audit_flag["softFlag"] = audit_flag["softFlag"] + soft_flag
                if hard_flag:
                    audit_flag["hardFlag"] = audit_flag["hardFlag"] + hard_flag

                soft_flag, hard_flag = UnitConversion.checkAuditFlagsopc(
                    opc_df, unit_dict
                )

                if soft_flag:
                    audit_flag["softFlag"] = audit_flag["softFlag"] + soft_flag
                if hard_flag:
                    audit_flag["hardFlag"] = audit_flag["hardFlag"] + hard_flag

                soft_flag, hard_flag = UnitConversion.checkAuditFlagsopc(
                    opc_df, unit_dict
                )

                if soft_flag:
                    audit_flag["softFlag"] = audit_flag["softFlag"] + soft_flag
                if hard_flag:
                    audit_flag["hardFlag"] = audit_flag["hardFlag"] + hard_flag
            else:
                hard_flag = {"name": "OPC data", "value": "OPC dataframe is empty"}
                audit_flag["hardFlag"] = audit_flag["hardFlag"] + [hard_flag]

            if cas_df is not None:
                cas_df.replace({"": None, np.nan: None}, inplace=True)
                data = df_to_json_converter(metadata_df, opc_df, cas_df)
            else:
                data = df_to_json_converter(metadata_df, opc_df)

            response = {"data": data, "auditFlag": audit_flag}

            return response

        except Exception as e:
            raise ("Unit conversion failure", str(e))

    @staticmethod
    def checkAuditFlags(df):
        soft_flags = []
        hard_flags = []

        df = df[~df.value.isnull()]

        grouped_data = (
            df.groupby("name")["unit"].apply(lambda x: list(set(x))).reset_index()
        )

        for i, row in grouped_data.iterrows():
            if len(row["unit"]) > 1:
                hard_flags.append(
                    {"name": row["name"], "value": "Multiple incompatible units found"}
                )

        return soft_flags, hard_flags

    @staticmethod
    def checkAuditFlagsopc(df, unit_dict):
        soft_flags = []
        hard_flags = []

        for i, row in df.iterrows():
            if row["name"] not in unit_dict.keys():
                hard_flags.append(
                    {"name": row["name"], "value": "OPC not found in unit_dict "}
                )
        return soft_flags, hard_flags
