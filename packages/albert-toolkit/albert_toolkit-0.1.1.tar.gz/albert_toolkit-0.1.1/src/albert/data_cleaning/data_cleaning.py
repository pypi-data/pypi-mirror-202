"""
Python module for operating condition data cleaning
"""
import numpy as np
import pandas as pd
import re
import qcelemental as qcel
import pint
from roman import fromRoman
import pkg_resources
from albert.pipeline import AlbertConfigurableBaseEstimator
from sklearn.pipeline import TransformerMixin
from albert.internal.utils import json_to_df_converter, df_to_json_converter


class DataCleaningValueUnit :
    """
    This class can be used for cleaning operating condition values and units
    """

    def __init__ (self, value: str, unit: str) :
        if not isinstance (value, str) :
            raise TypeError ("Value must be a string")
        if not isinstance (unit, str) :
            raise TypeError ("Unit must be a string")

        self.value = value
        self.unit = unit
        self.Q_ = pint.UnitRegistry (
            pkg_resources.resource_filename (
                __package__.split (".")[0], "resources/unit_registry_custom.txt"
            ), autoconvert_offset_to_baseunit=True
        ).Quantity

        self.find_replace_dict = dict (pd.read_excel (
            pkg_resources.resource_filename (__package__.split (".")[0], 'resources/replace_rules.xlsx')
        )[["Input", "Output"]].to_records (index=False))
        self.find_replace_rules = {str (key) : str (self.find_replace_dict[key]) for key in
                                   self.find_replace_dict.keys ()}


    def clean_special_characters (self) :
        value = self.value
        try :
            cleaned_value = re.sub ("[`~?$!)({}\]\[_]", "", str (value)).strip ()
            cleaned_value = re.sub (r'(?<=[a-zA-Z])-(?=[a-zA-Z])', '', cleaned_value)

            values = re.findall (r"\b(\d{1,3}.?\d{0,2} ?%)", cleaned_value)
            for v in values :
                replace_value = float (re.sub ("%", "", v)) / 100
                cleaned_value = re.sub (v, str (replace_value), cleaned_value)

            cleaned_value = cleaned_value.rstrip (".")
            cleaned_value = cleaned_value.rstrip (",")
            cleaned_value = cleaned_value.rstrip ("+")
            cleaned_value = cleaned_value.rstrip ("-")
            cleaned_value = cleaned_value.lstrip (">")
            cleaned_value = cleaned_value.lstrip ("<")

            cleaned_value = re.sub (r"- *$", "", cleaned_value)
            cleaned_value = re.sub (r"\. *$", "", cleaned_value)
            cleaned_value = cleaned_value.strip ()

            self.value = cleaned_value
        except :
            pass

    def clean_keywords (self) :
        value = self.value
        try :
            cleaned_value = re.sub (r"exactly|approximately|or higher$|or lower$", "", str (value),
                                    flags=re.IGNORECASE).strip ()
            if cleaned_value.lower () == "green" :
                cleaned_value = "0"
            self.value = cleaned_value
        except :
            pass

    def clean_roman_values (self) :
        value = self.value
        try :
            cleaned_value = fromRoman (value)
            self.value = cleaned_value
        except :
            pass

    def clean_float_values (self) :
        value = self.value
        try :
            cleaned_value = str (float (value))
            self.value = cleaned_value
        except :
            pass

    def clean_null_values (self) :
        value = self.value
        unit = self.unit
        try :
            if value == "-" or value == "--" or len (re.findall (",", str (value))) > 2 :
                cleaned_value = ""
            else :
                cleaned_value = re.sub (r"^none$|^unknown$|^nan$|^na$|^n/a$|^tbd$|^null$|^n\.a\.$", "", str (value),
                                        flags=re.IGNORECASE).strip ()
            self.value = cleaned_value

            if unit == "-" or unit == "--" or len (re.findall (",", str (unit))) > 2 :
                cleaned_unit = ""
            else :
                cleaned_unit = re.sub (r"^none$|^unknown$|^nan$|^na$|^n/a$|^tbd$|^null$|^n\.a\.$", "", str (unit),
                                       flags=re.IGNORECASE).strip ()
            self.unit = cleaned_unit
        except :
            pass

    def clean_ordinal_values (self) :
        value = self.value

        try :
            cleaned_value = re.sub (r"(?<=1\d)th\b|(?<=1)st\b|(?<=2)nd\b|(?<=3)rd\b|(?<=[04-9])th\b", r'',
                                    str (value)).strip ()
            self.value = cleaned_value
        except :
            pass

    def clean_find_and_replace (self) :
        value = self.value
        try :
            if value in self.find_replace_rules.keys () :
                cleaned_value = self.find_replace_rules[value]
            else :
                cleaned_value = value
            self.value = cleaned_value
        except Exception as e :
            self.value = value

    def clean_string_case (self) :
        value = self.value
        try :
            cleaned_value = str (value).lower ().strip ()
            self.value = cleaned_value
        except :
            pass

    @staticmethod
    def is_number (value) :
        try :
            float (value)
            return True
        except ValueError :
            return False

    @staticmethod
    def is_chemical_element (elem: str) -> str :
        try :
            if not DataCleaningValueUnit.isNumber (elem) and elem.isalpha () and elem.lower () != "x" :
                elem = qcel.periodictable.to_name (elem)
            else :
                pass
        except :
            pass
        return elem

    def clean_element_name (self) :
        value = self.value
        try :
            cleaned_value = " ".join ([DataCleaningValueUnit.is_chemical_element (x) for x in str (value).split (" ")])
            self.value = cleaned_value
        except :
            pass

    def clean_range_values (self) :
        value = self.value

        try :
            if re.findall (r"(?<=\d) *± *\d+.?\d*", value) :
                cleaned_value = re.sub (r"(?<=\d) *± *\d+.?\d*", '', str (value)).strip ()
                self.value = cleaned_value

            cleaned_value = re.sub (r"(?<=\d) *to *(?=\d)", r'-', str (value)).strip ()
            range_values = cleaned_value.split ("-")
            if range_values[0] == "" and self.is_number (range_values[1]) and self.is_number (range_values[2]) :
                cleaned_value = (-float (range_values[1]) + float (range_values[2])) / 2
            elif self.is_number (range_values[0]) and self.is_number (range_values[1]) :
                cleaned_value = (float (range_values[0]) + float (range_values[1])) / 2
            self.value = cleaned_value
        except :
            pass

    def clean_special_characters_numbers (self) :
        value = self.value
        try :
            cleaned_value = re.sub (r"\b(?<=\d),(?=\d)\b", '.', str (value)).strip ()
            self.value = cleaned_value
        except Exception as e :
            pass

    def clean_units_in_values (self) :
        value = self.value
        try :
            cleaned_value = re.sub (r"(?<=\d) *[cC]$|(?<=\d) *°c$|(?<=\d) *°C$", ' celsius', str (value)).strip ()
            cleaned_value = re.sub (r"(?<=\d) *[cC] */|(?<=\d) *°c */|(?<=\d) *°C */", ' celsius/',
                                    cleaned_value).strip ()

            if re.match (r"^(\d+.?\d*) *h$", cleaned_value) :
                cleaned_value = re.sub (r"^(\d+.?\d*) *h$", r'\1 hour', cleaned_value).strip ()

            if re.match (r"^(\d+.?\d*) *k$", cleaned_value) :
                cleaned_value = re.sub (r"^(\d+.?\d*) *k$", r'\1', cleaned_value).strip ()
                cleaned_value = str (float (cleaned_value) * 1000)

            self.value = cleaned_value
        except :
            pass

    def clean_units (self) :
        unit = self.unit
        try :
            cleaned_unit = re.sub ("^c$|^C$|^°c|°C$|^RT$|^°C or RT$|^°c or RT$", "celsius", str (unit)).strip ()
            cleaned_unit = re.sub ("^c/|^C/", "celsius/", cleaned_unit).strip ()
            cleaned_unit = re.sub ("/c$|/C$", "/celsius  ", cleaned_unit).strip ()

            cleaned_unit = re.sub ("/m2$", "/meter ** 2", cleaned_unit).strip ()
            cleaned_unit = re.sub ("/m3$", "/meter ** 3", cleaned_unit).strip ()
            cleaned_unit = re.sub ("^m2$", "meter ** 2", cleaned_unit).strip ()
            cleaned_unit = re.sub ("^m3$", "meter ** 3", cleaned_unit).strip ()
            cleaned_unit = re.sub ("/cm2$", "/centimeter ** 2", cleaned_unit).strip ()
            cleaned_unit = re.sub ("/cm3$", "/centimeter ** 3", cleaned_unit).strip ()
            cleaned_unit = re.sub ("^cm2$", "centimeter ** 2", cleaned_unit).strip ()
            cleaned_unit = re.sub ("^cm3$", "centimeter ** 3", cleaned_unit).strip ()

            if unit.lower () == "unitless" :
                cleaned_unit = ""
            self.unit = cleaned_unit
        except :
            pass

    def clean_percent_values (self) :
        value = self.value
        unit = self.unit
        try :
            values = re.findall (r"\b(\d{1,3}.?\d{0,2} ?percent)\b", str (value), flags=re.IGNORECASE)
            for v in values :
                replace_value = float (re.sub ("percent", "", v, flags=re.IGNORECASE)) / 100
                cleaned_value = re.sub (v, str (replace_value), value)

            if unit.lower () == "percent" :
                cleaned_value = re.sub (" *%", "", value).strip ()
                cleaned_value = str (float (cleaned_value) / 100)

            self.value = cleaned_value
            self.unit = ""
        except :
            pass

    def split_value_and_unit (self) :
        """
        Takes the value which entered by the user and check whether it consists of any unit along
        Returns: Extracted unit from value has been overwrite to the unit features
        """
        value = self.value
        unit = self.unit

        try :
            if value is None or value == "" :
                self.value = ""
                self.unit = ""

            if unit.replace (" ", "") == "min/side" :
                unit = "minute/side"

            # if 'notes' in str (name).lower () :
            #     return value, unit
            if re.findall ("^\d.*", value) :
                res = self.Q_ (value)  # checks any units has been entered along with the value
                if res.units == "minute" and unit.replace (" ", "") == "/side" :
                    self.value = str (float (res.magnitude))
                    self.unit = "minute/side"
                if (str (res.units) is not None) and str (res.units) != "dimensionless" :
                    self.value = str (float (res.magnitude))
                    self.unit = str (res.units)
                else :
                    pass
            else :
                pass
        except :
            pass

    def clean_spaces (self) :
        value = self.value
        try :
            cleaned_value = re.sub ("\s+", "", str (value))
            self.value = cleaned_value
        except :
            pass

    def clean_value_and_unit (self) :
        try :
            self.clean_null_values ()
            self.clean_find_and_replace ()
            self.clean_ordinal_values ()
            self.clean_element_name ()
            self.clean_percent_values ()
            self.clean_special_characters_numbers ()
            self.clean_range_values ()
            self.clean_units_in_values ()
            self.clean_keywords ()
            self.clean_roman_values ()
            self.clean_string_case ()
            self.clean_null_values ()
            self.clean_special_characters ()
            self.clean_float_values ()
            self.clean_units ()
            self.split_value_and_unit ()
            self.clean_spaces ()

            return self.value, self.unit
        except :
            pass


class DataCleaning (AlbertConfigurableBaseEstimator, TransformerMixin) :

    def __int__(self):
        super().__init__()
        
    @staticmethod
    def clean_opc_df (df: pd.DataFrame) -> pd.DataFrame :
        cleaned_data = [DataCleaningValueUnit (str(value), str(unit)) for value, unit in
                        zip (df['value'], df['unit'])]
        df[["value", "unit"]] = [cd.clean_value_and_unit () for cd in cleaned_data]
        return df

    @staticmethod
    def checkListValueAuditFlag (df: pd.DataFrame) -> (list, list) :
        soft_flags = []
        hard_flags = []

        for value, unit, name in zip (df['value'], df['unit'], df['name']) :
            if len (re.findall (",", str (value))) > 2 :
                soft_flag = {}
                hard_flag = {"name" : name,
                             "value" : "More than two commas in the value"}

                if soft_flag and soft_flag not in soft_flags :
                    soft_flags.append (soft_flag)
                if hard_flag and hard_flag not in hard_flags :
                    hard_flags.append (hard_flag)
        return soft_flags, hard_flags

    @staticmethod
    def isNumber (s: str) -> bool :
        try :
            float (s)
            return True
        except ValueError :
            return False

    @staticmethod
    def rangeOrNumber (value: str) -> str :
        value = re.sub (r"(?<=\d) *to *(?=\d)", r'-', str (value))

        if re.findall (r"\d-\d", value) :
            return "range"
        elif DataCleaning.isNumber (value) :
            return "number"
        else :
            return "string"

    @staticmethod
    def checkRangeAndNumericAuditFlag (df: pd.DataFrame) -> (list, list) :
        soft_flags = []
        hard_flags = []

        df = df[df.value != ""]
        df['type'] = [DataCleaning.rangeOrNumber (x) for x in df['value']]
        grouped_data = df.groupby ('name')['type'].apply (lambda x : list (set (x))).reset_index ()

        for i, row in grouped_data.iterrows () :
            if "range" in row['type'] and "number" in row['type'] :
                soft_flags.append ({"name" : row['name'],
                                    "value" : "Numbers and Ranges found"})

        return soft_flags, hard_flags

    @staticmethod
    def checkPercentNaAuditFlag (df: pd.DataFrame) -> (list, list) :
        soft_flags = []
        hard_flags = []

        grouped_data = df.groupby ('name')['value'].apply (lambda x : (x == "").sum () / len (x)).reset_index ()

        for i, row in grouped_data.iterrows () :
            if row['value'] >= 0.5 :
                hard_flags.append ({"name" : row['name'],
                                    "value" : "NA values equal to " + str (round (row['value'] * 100, 2)) + "%"})

        return soft_flags, hard_flags


    def transform (self, payload: dict[str]) -> dict[str] :
        try :
            data = payload["data"]
            metadata_df, inputs_df = json_to_df_converter (data)
            cas_df = None

            if "smiles" in inputs_df.columns :
                pass
            else :
                inputs_df["smiles"] = np.nan


            if "albertId" in inputs_df :
                # Model prediction case (contains cas info)
                opc_df = inputs_df[inputs_df.albertId.isnull()]
                cas_df = inputs_df[inputs_df.albertId.notnull()]
            else:
                # Model build case (doesn't have any albertId's)
                opc_df = inputs_df


            opc_df.replace ({"" : None, np.nan : None})

            if metadata_df is not None :
                metadata_df.replace ({"" : None, np.nan : None}, inplace=True)

            audit_flag = {"softFlag" : [], "hardFlag" : []}

            if len (opc_df) != 0 :
                soft_flag, hard_flag = DataCleaning.checkListValueAuditFlag (opc_df)
                if soft_flag :
                    audit_flag['softFlag'] = audit_flag['softFlag'] + soft_flag
                if hard_flag :
                    audit_flag['hardFlag'] = audit_flag['hardFlag'] + hard_flag

                soft_flag, hard_flag = DataCleaning.checkRangeAndNumericAuditFlag (opc_df)
                if soft_flag :
                    audit_flag['softFlag'] = audit_flag['softFlag'] + soft_flag
                if hard_flag :
                    audit_flag['hardFlag'] = audit_flag['hardFlag'] + hard_flag

                opc_df = DataCleaning.clean_opc_df (opc_df)

                soft_flag, hard_flag = DataCleaning.checkPercentNaAuditFlag (opc_df)
                if soft_flag :
                    audit_flag['softFlag'] = audit_flag['softFlag'] + soft_flag
                if hard_flag :
                    audit_flag['hardFlag'] = audit_flag['hardFlag'] + hard_flag

                opc_df.replace ({"" : None, np.nan : None}, inplace=True)
            else :
                hard_flag = {"name" : "OPC data", "value" : "OPC dataframe is empty"}
                audit_flag['hardFlag'] = audit_flag['hardFlag'] + [hard_flag]

            if metadata_df is not None :
                metadata_df.replace ({"" : None, np.nan : None}, inplace=True)

            if cas_df is not None :
                cas_df.replace ({"" : None, np.nan : None}, inplace=True)

                data = df_to_json_converter (metadata_df, opc_df, cas_df)

            else :
                data = df_to_json_converter (metadata_df, opc_df)

            response = {"data" : data,
                        "auditFlag" : audit_flag}

            return response

        except Exception as e :
            raise ("Data cleaning failure", str (e))
