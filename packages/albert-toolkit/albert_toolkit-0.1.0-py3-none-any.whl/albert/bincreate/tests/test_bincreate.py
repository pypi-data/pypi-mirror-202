import unittest
from albert.bincreate import BinCreator
from albert.utils import *
import pandas as pd

input_data = {'data': [{'intervalId': 'default', 'inputs': [
    {'name': 'HDT by DMA_HDT Pressure_1', 'id': 'PRG151_PRM185_1', 'value': '6.0', 'unit': 'megapascals',
     'rowId': 'ROW2'},
    {'name': 'HDT by DMA_Temperature Rate_1', 'id': 'PRG151_PRM106_1', 'value': '2.0', 'unit': 'Celsius / min',
     'rowId': 'ROW3'},
    {'name': 'HDT by DMA_Temperature Range_1', 'id': 'PRG151_PRM187_1', 'value': '112.5', 'unit': 'celsius',
     'rowId': 'ROW4'},
    {'name': 'HDT by DMA_Specimen Size_1', 'id': 'PRG151_PRM139_1', 'value': '5.9x3', 'unit': 'mm²', 'rowId': 'ROW5'},
    {'name': 'HDT by DMA_Span Width_1', 'id': 'PRG151_PRM70_1', 'value': '40.0', 'unit': 'millimeter', 'rowId': 'ROW6'},
    {'name': 'HDT by DMA_Number of Duplicates_1', 'id': 'PRG151_PRM38_1', 'value': '1.0', 'unit': 'Sample(s)',
     'rowId': 'ROW7'},
    {'name': 'HDT by DMA_Orientation_1', 'id': 'PRG151_PRM379_1', 'value': 'flat', 'unit': 'Flat or Edge',
     'rowId': 'ROW8'},
    {'name': '7534-94-3', 'value': 19.801980198019802, 'smiles': 'CC(=C)C(=O)O[C@H]1C[C@@H]2CC[C@@]1(C)C2(C)C',
     'albertId': 'INVA144441'},
    {'name': '7732-18-5', 'value': 0.19801980198019803, 'smiles': 'O', 'albertId': 'INVA144441'},
    {'name': '108-88-3', 'value': 0.19567556990509735, 'smiles': 'Cc1ccccc1', 'albertId': 'INVA19803'},
    {'name': '67-56-1', 'value': 0.6020948331865767, 'smiles': 'CO',
     'albertId': 'INVA19803,INVA17482,INVA20151,INVA19656'},
    {'name': '82985-35-1', 'value': 9.745719596908325, 'smiles': 'CCC(NC(CC)[Si](OC)(OC)OC)[Si](OC)(OC)OC',
     'albertId': 'INVA19803'},
    {'name': '110-82-7', 'value': 0.07424999999999998, 'smiles': 'C1CCCCC1', 'albertId': 'INVA17482'},
    {'name': '128000-08-8', 'value': 14.793000000000001, 'smiles': None, 'albertId': 'INVA17482'},
    {'name': '128-37-0', 'value': 0.015, 'smiles': 'Cc1cc(c(O)c(c1)C(C)(C)C)C(C)(C)C', 'albertId': 'INVA17482'},
    {'name': '110-54-3', 'value': 0.07424999999999998, 'smiles': 'CCCCCC', 'albertId': 'INVA17482'},
    {'name': '5970-45-6', 'value': 2.0000000000000004, 'smiles': None, 'albertId': 'INVA164020'},
    {'name': '71-36-3', 'value': 0.05, 'smiles': 'CCCCO', 'albertId': 'INVA164020'},
    {'name': '7664-39-3', 'value': 0.1, 'smiles': 'F', 'albertId': 'INVA164020'},
    {'name': 'INVA164020_Unknown', 'value': 2.85, 'smiles': None, 'albertId': 'INVA164020'},
    {'name': 'INVA145356_Unknown', 'value': 10.0, 'smiles': None, 'albertId': 'INVA145356'},
    {'name': '14808-60-7', 'value': 5.0, 'smiles': 'O=[Si]=O', 'albertId': 'INVA104995'},
    {'name': '1309-37-1', 'value': 4.9, 'smiles': 'O1[Fe]2O[Fe]1O2', 'albertId': 'INVA114029'},
    {'name': 'INVA114029_Unknown', 'value': 0.1, 'smiles': None, 'albertId': 'INVA114029'},
    {'name': '429-60-7', 'value': 9.51, 'smiles': 'CO[Si](CCC(F)(F)F)(OC)OC', 'albertId': 'INVA20151'},
    {'name': 'U22-295 Proprietary 1', 'value': 0.09615384615384616, 'smiles': None, 'albertId': 'INVA163976'},
    {'name': 'U99-504_1 Secret', 'value': 0.09615384615384616, 'smiles': None, 'albertId': 'INVA163976'},
    {'name': 'U99-508_1 Proprietary 2', 'value': 0.09615384615384616, 'smiles': None, 'albertId': 'INVA163976'},
    {'name': 'U22-263_1 Secret 1 ', 'value': 0.09615384615384616, 'smiles': None, 'albertId': 'INVA163976'},
    {'name': 'wewq', 'value': 9.615384615384617, 'smiles': 'test12', 'albertId': 'INVA163976'},
    {'name': '75-07-0', 'value': 0.0008000000000000001, 'smiles': 'CC=O', 'albertId': 'INVA19656'},
    {'name': 'INVA19656_Unknown', 'value': 9.98921, 'smiles': None, 'albertId': 'INVA19656'}], 'entity': 'task',
                        'id': 'TASFOR100098', 'parentId': 'INVMO3214-001', 'inventoryId': 'INVMO3214-001',
                        'workflowId': 'WFL36324', 'projectId': 'PROMO3214', 'modelId': 'PMD8', 'modelVersion': '1.15',
                        'modelOrganization': 'Albert',
                        'modelEndpoint': '/api/v3/propmodels/models/{modelId}/{modelVersion}',
                        'dataColumnId': 'DAC1011', 'dataColumnName': 'HDT', 'dataColumnUniqueId': 'DAC1011#COL4',
                        'dataTemplateId': 'DAT39', 'loopType': 'local', 'predictionType': 'loop'}],
              'auditFlag': {'softFlag': [],
                            'hardFlag': [{'name': 'HDT by DMA_HDT Pressure_1', 'value': 'OPC not found in unit_dict '},
                                         {'name': 'HDT by DMA_Temperature Rate_1',
                                          'value': 'OPC not found in unit_dict '},
                                         {'name': 'HDT by DMA_Temperature Range_1',
                                          'value': 'OPC not found in unit_dict '},
                                         {'name': 'HDT by DMA_Specimen Size_1', 'value': 'OPC not found in unit_dict '},
                                         {'name': 'HDT by DMA_Span Width_1', 'value': 'OPC not found in unit_dict '},
                                         {'name': 'HDT by DMA_Number of Duplicates_1',
                                          'value': 'OPC not found in unit_dict '},
                                         {'name': 'HDT by DMA_Orientation_1', 'value': 'OPC not found in unit_dict '},
                                         {'name': 'HDT by DMA_HDT Pressure_1', 'value': 'OPC not found in unit_dict '},
                                         {'name': 'HDT by DMA_Temperature Rate_1',
                                          'value': 'OPC not found in unit_dict '},
                                         {'name': 'HDT by DMA_Temperature Range_1',
                                          'value': 'OPC not found in unit_dict '},
                                         {'name': 'HDT by DMA_Specimen Size_1', 'value': 'OPC not found in unit_dict '},
                                         {'name': 'HDT by DMA_Span Width_1', 'value': 'OPC not found in unit_dict '},
                                         {'name': 'HDT by DMA_Number of Duplicates_1',
                                          'value': 'OPC not found in unit_dict '},
                                         {'name': 'HDT by DMA_Orientation_1', 'value': 'OPC not found in unit_dict '}]}}


def test_json_to_df_converter():
    meta_df, inp_df = json_to_df_converter(input_data['data'])
    if isinstance(inp_df, pd.DataFrame):
        assert True


class TestBinCreator(unittest.TestCase):

    def test_transform(self):
        # create example JSON input

        # create mock headers
        headers = {"content-type": "application/json", "authorization": "Bearer my-token", "uuid": "1234"}

        # create instance of transformer
        transformer = BinCreator()

        # transform input
        output = transformer.transform(input_data)
        print("----", output)
        # # assert expected output
        expected_output = {'data': [{'intervalId': 'default', 'inputs': [
            {'name': 'HDT by DMA_HDT Pressure_1', 'id': 'PRG151_PRM185_1', 'value': '6.0', 'unit': 'megapascals',
             'rowId': 'ROW2'},
            {'name': 'HDT by DMA_Temperature Rate_1', 'id': 'PRG151_PRM106_1', 'value': '2.0', 'unit': 'Celsius / min',
             'rowId': 'ROW3'},
            {'name': 'HDT by DMA_Temperature Range_1', 'id': 'PRG151_PRM187_1', 'value': '112.5', 'unit': 'celsius',
             'rowId': 'ROW4'},
            {'name': 'HDT by DMA_Specimen Size_1', 'id': 'PRG151_PRM139_1', 'value': '5.9x3', 'unit': 'mm²',
             'rowId': 'ROW5'},
            {'name': 'HDT by DMA_Span Width_1', 'id': 'PRG151_PRM70_1', 'value': '40.0', 'unit': 'millimeter',
             'rowId': 'ROW6'},
            {'name': 'HDT by DMA_Number of Duplicates_1', 'id': 'PRG151_PRM38_1', 'value': '1.0', 'unit': 'Sample(s)',
             'rowId': 'ROW7'},
            {'name': 'HDT by DMA_Orientation_1', 'id': 'PRG151_PRM379_1', 'value': 'flat', 'unit': 'Flat or Edge',
             'rowId': 'ROW8'},
            {'name': '7534-94-3', 'value': 19.801980198019802, 'smiles': 'CC(=C)C(=O)O[C@H]1C[C@@H]2CC[C@@]1(C)C2(C)C',
             'albertId': 'INVA144441'},
            {'name': '7732-18-5', 'value': 0.19801980198019803, 'smiles': 'O', 'albertId': 'INVA144441'},
            {'name': '108-88-3', 'value': 0.19567556990509735, 'smiles': 'Cc1ccccc1', 'albertId': 'INVA19803'},
            {'name': '67-56-1', 'value': 0.6020948331865767, 'smiles': 'CO',
             'albertId': 'INVA19803,INVA17482,INVA20151,INVA19656'},
            {'name': '82985-35-1', 'value': 9.745719596908325, 'smiles': 'CCC(NC(CC)[Si](OC)(OC)OC)[Si](OC)(OC)OC',
             'albertId': 'INVA19803'},
            {'name': '110-82-7', 'value': 0.07424999999999998, 'smiles': 'C1CCCCC1', 'albertId': 'INVA17482'},
            {'name': '128000-08-8', 'value': 14.793000000000001, 'smiles': None, 'albertId': 'INVA17482'},
            {'name': '128-37-0', 'value': 0.015, 'smiles': 'Cc1cc(c(O)c(c1)C(C)(C)C)C(C)(C)C', 'albertId': 'INVA17482'},
            {'name': '110-54-3', 'value': 0.07424999999999998, 'smiles': 'CCCCCC', 'albertId': 'INVA17482'},
            {'name': '5970-45-6', 'value': 2.0000000000000004, 'smiles': None, 'albertId': 'INVA164020'},
            {'name': '71-36-3', 'value': 0.05, 'smiles': 'CCCCO', 'albertId': 'INVA164020'},
            {'name': '7664-39-3', 'value': 0.1, 'smiles': 'F', 'albertId': 'INVA164020'},
            {'name': 'INVA164020_Unknown', 'value': 2.85, 'smiles': None, 'albertId': 'INVA164020'},
            {'name': 'INVA145356_Unknown', 'value': 10.0, 'smiles': None, 'albertId': 'INVA145356'},
            {'name': '14808-60-7', 'value': 5.0, 'smiles': 'O=[Si]=O', 'albertId': 'INVA104995'},
            {'name': '1309-37-1', 'value': 4.9, 'smiles': 'O1[Fe]2O[Fe]1O2', 'albertId': 'INVA114029'},
            {'name': 'INVA114029_Unknown', 'value': 0.1, 'smiles': None, 'albertId': 'INVA114029'},
            {'name': '429-60-7', 'value': 9.51, 'smiles': 'CO[Si](CCC(F)(F)F)(OC)OC', 'albertId': 'INVA20151'},
            {'name': 'U22-295 Proprietary 1', 'value': 0.09615384615384616, 'smiles': None, 'albertId': 'INVA163976'},
            {'name': 'U99-504_1 Secret', 'value': 0.09615384615384616, 'smiles': None, 'albertId': 'INVA163976'},
            {'name': 'U99-508_1 Proprietary 2', 'value': 0.09615384615384616, 'smiles': None, 'albertId': 'INVA163976'},
            {'name': 'U22-263_1 Secret 1 ', 'value': 0.09615384615384616, 'smiles': None, 'albertId': 'INVA163976'},
            {'name': 'wewq', 'value': 9.615384615384617, 'smiles': 'test12', 'albertId': 'INVA163976'},
            {'name': '75-07-0', 'value': 0.0008000000000000001, 'smiles': 'CC=O', 'albertId': 'INVA19656'},
            {'name': 'INVA19656_Unknown', 'value': 9.98921, 'smiles': None, 'albertId': 'INVA19656'}], 'entity': 'task',
                                     'id': 'TASFOR100098', 'parentId': 'INVMO3214-001', 'inventoryId': 'INVMO3214-001',
                                     'workflowId': 'WFL36324', 'projectId': 'PROMO3214', 'modelId': 'PMD8',
                                     'modelVersion': '1.15', 'modelOrganization': 'Albert',
                                     'modelEndpoint': '/api/v3/propmodels/models/{modelId}/{modelVersion}',
                                     'dataColumnId': 'DAC1011', 'dataColumnName': 'HDT',
                                     'dataColumnUniqueId': 'DAC1011#COL4', 'dataTemplateId': 'DAT39',
                                     'loopType': 'local', 'predictionType': 'loop'}],
                           'bin_labels': {'HDT by DMA_Orientation_1': {'string': {'flat': ['flat']}, 'number': ['nan']},
                                          'HDT by DMA_Specimen Size_1': {'string': {'5.9x3': ['5.9x3']},
                                                                         'number': ['nan']},
                                          'HDT by DMA_HDT Pressure_1': {'number': ['nan', 6.0]},
                                          'HDT by DMA_Temperature Rate_1': {'number': ['nan', 2.0]},
                                          'HDT by DMA_Temperature Range_1': {'number': ['nan', 112.5]},
                                          'HDT by DMA_Span Width_1': {'number': ['nan', 40.0]},
                                          'HDT by DMA_Number of Duplicates_1': {'number': ['nan', 1.0]}},
                           'auditFlag': {'softFlag': [], 'hardFlag': [
                               {'name': 'HDT by DMA_HDT Pressure_1', 'value': 'OPC not found in unit_dict '},
                               {'name': 'HDT by DMA_Temperature Rate_1', 'value': 'OPC not found in unit_dict '},
                               {'name': 'HDT by DMA_Temperature Range_1', 'value': 'OPC not found in unit_dict '},
                               {'name': 'HDT by DMA_Specimen Size_1', 'value': 'OPC not found in unit_dict '},
                               {'name': 'HDT by DMA_Span Width_1', 'value': 'OPC not found in unit_dict '},
                               {'name': 'HDT by DMA_Number of Duplicates_1', 'value': 'OPC not found in unit_dict '},
                               {'name': 'HDT by DMA_Orientation_1', 'value': 'OPC not found in unit_dict '},
                               {'name': 'HDT by DMA_HDT Pressure_1', 'value': 'OPC not found in unit_dict '},
                               {'name': 'HDT by DMA_Temperature Rate_1', 'value': 'OPC not found in unit_dict '},
                               {'name': 'HDT by DMA_Temperature Range_1', 'value': 'OPC not found in unit_dict '},
                               {'name': 'HDT by DMA_Specimen Size_1', 'value': 'OPC not found in unit_dict '},
                               {'name': 'HDT by DMA_Span Width_1', 'value': 'OPC not found in unit_dict '},
                               {'name': 'HDT by DMA_Number of Duplicates_1', 'value': 'OPC not found in unit_dict '},
                               {'name': 'HDT by DMA_Orientation_1', 'value': 'OPC not found in unit_dict '}]}}

        assert output == expected_output
