import pandas as pd


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
    Takes metadata, operating condition and cas dtaFrames and converts it into a nested list of dictionaries
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
