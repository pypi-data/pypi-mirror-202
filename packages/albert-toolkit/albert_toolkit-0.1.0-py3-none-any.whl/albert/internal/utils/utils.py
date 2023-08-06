import os
import dotenv
import numpy as np
from typing import Any
import pandas as pd


def load_albert_config(override_env_vars=True) -> None:
    if os.path.isdir("~/.albert/"):
        if os.path.exists("~/.albert/config"):
            dotenv.load_dotenv("~/.albert/config", override=override_env_vars)


def get_albert_parameter(
    user_input: Any | None = None,
    environment_variable: str | None = None,
    default_value: Any | None = None,
) -> str | None:
    """
    user_input: a parameter that the user may have set which contains the value that if set should
                be used
    environment_variable: name of an environment variable to use if user_input is None
    default_value: value to use if user_input is None or == "" and environment variable is not defined
    """
    if user_input is not None:
        if isinstance(user_input, str):
            if user_input != "":
                return user_input
        else:
            return user_input

    elif environment_variable is not None:
        if environment_variable in os.environ:
            return os.environ[environment_variable]

    elif default_value is not None:
        return default_value

    return None


def convert_dynamic_schema_to_python_types(item: dict) -> dict:
    for k, v in item.items():
        if hasattr(v, "keys"):
            # likely another frozendict
            item[k] = convert_dynamic_schema_to_python_types(dict(v))
        elif hasattr(v, "isnumeric"):
            if v.isnumeric():
                item[k] = float(v)
            else:
                item[k] = str(v)
        elif hasattr(v, "is_finite"):  # Decimal Type Most likely
            if v.is_finite():
                item[k] = float(v)
            elif v.is_nan():
                item[k] = np.nan
            elif v.is_infinite():
                item[k] = np.inf
        else:
            item[k] = None

    return item


def validate_dataframe_has_columns(X: pd.DataFrame, columns: list[str]) -> bool:
    res = True
    for c in columns:
        if c not in X.columns:
            res = False
            print(f"Missing column {c}")

    return res


def json_to_df_converter(json_input):
    """
    Takes JSON input and converts it into a DataFrame
    """
    metadata_df = pd.DataFrame.from_records(json_input)
    for idx, entry in enumerate(metadata_df['inputs']):
        row_df = pd.DataFrame.from_dict(entry)
        row_df['idx'] = idx
        if idx > 0:
            inputs_df = pd.concat([inputs_df, row_df])
        else:
            inputs_df = row_df

    return metadata_df, inputs_df


def df_to_json_converter(metadata_df, opc_df, cas_df=None):
    """
    Takes a DataFrame and converts it into a nested list of dictionaries
    JSON structure
    """

    opc_cols = ['name', 'id', 'value', 'unit', 'rowId']
    cas_cols = ['name', 'value', 'smiles', 'albertId']

    json_output = []

    for i in range(len(metadata_df)):
        if len(opc_df) != 0:
            metadata_df.at[i, 'inputs'] = [row.to_dict() for _, row in opc_df[opc_df.idx == i][opc_cols].iterrows()]

            if (cas_df is not None) and (i in cas_df.idx.unique()):
                metadata_df.loc[i, 'inputs'].extend(
                    [row.to_dict() for _, row in cas_df[cas_df.idx == i][cas_cols].iterrows()])

    return [row.to_dict() for _, row in metadata_df.iterrows()]