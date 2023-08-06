from albert.data_cleaning import DataCleaning, DataCleaningValueUnit


def test_cleanValueAndUnit():

    assert DataCleaningValueUnit("10 - 55", "celsius").clean_value_and_unit() == ("32.5", "celsius")

    assert DataCleaningValueUnit ("-10 to 100", "celsius").clean_value_and_unit () == ("45.0", "celsius")

    assert DataCleaningValueUnit ("-", "").clean_value_and_unit () == ("", "")

    assert DataCleaningValueUnit ("--", "").clean_value_and_unit() == ("", "")

    assert DataCleaningValueUnit ("--", "").clean_value_and_unit () == ("", "")

    assert DataCleaningValueUnit ("90", "percent").clean_value_and_unit () == ("0.9", "")

    assert DataCleaningValueUnit ("140c", "").clean_value_and_unit () == ("140.0", "celsius")

    assert DataCleaningValueUnit ("Green", "").clean_value_and_unit () == ("0.0", "")

    assert DataCleaningValueUnit ("", "n/a").clean_value_and_unit () == ("", "")

    assert DataCleaningValueUnit ("n/a", "").clean_value_and_unit () == ("", "")

    assert DataCleaningValueUnit ("0.5", "RPM").clean_value_and_unit () == ("0.5", "RPM")

    assert DataCleaningValueUnit ("rt", "").clean_value_and_unit () == ("25.0", "celsius")

    assert DataCleaningValueUnit ("5", "cm").clean_value_and_unit () == ("5.0", "cm")

    assert DataCleaningValueUnit ("0.5", "RPM").clean_value_and_unit () == ("0.5", "RPM")

    assert DataCleaningValueUnit ("1k", "cm").clean_value_and_unit () == ("1000.0", "cm")

    assert DataCleaningValueUnit ("string test with spaces", "cm").clean_value_and_unit () == ("stringtestwithspaces", "cm")

    assert DataCleaningValueUnit ("~48", "J/cm² - Total").clean_value_and_unit () == ("48.0", "J/cm² - Total")

    assert DataCleaningValueUnit ("1 wk", "").clean_value_and_unit () == ("1.0", "week")

    assert DataCleaningValueUnit ("260°c", "").clean_value_and_unit () == ("260.0", "celsius")

    assert DataCleaningValueUnit ("3", "C/min").clean_value_and_unit () == ("3.0", "celsius/min")

    assert DataCleaningValueUnit ("1st", "second").clean_value_and_unit () == ("1.0", "second")

    assert DataCleaningValueUnit ("104th", "hour").clean_value_and_unit () == ("104.0", "hour")

    assert DataCleaningValueUnit ("104st", "hour").clean_value_and_unit () == ("104st", "hour")

    assert DataCleaningValueUnit ("92.4 Percent", "").clean_value_and_unit () == ("0.924", "")

    assert DataCleaningValueUnit ("10,25", "minute").clean_value_and_unit () == ("10.25", "minute")

    assert DataCleaningValueUnit ("10 to 25", "minute").clean_value_and_unit () == ("17.5", "minute")

    assert DataCleaningValueUnit ("rt", "").clean_value_and_unit () == ("25.0", "celsius")

    assert DataCleaningValueUnit ("ss", "").clean_value_and_unit () == ("stainlesssteel", "")

    assert DataCleaningValueUnit ("25 or higher", "minute").clean_value_and_unit () == ("25.0", "minute")

    assert DataCleaningValueUnit ("XI", "minute").clean_value_and_unit () == ("11.0", "minute")

    assert DataCleaningValueUnit ("null", "minute").clean_value_and_unit () == ("", "")

    assert DataCleaningValueUnit ("$20", "").clean_value_and_unit () == ("20.0", "")

    assert DataCleaningValueUnit ("< 50", "mins").clean_value_and_unit () == ("50.0", "mins")

    assert DataCleaningValueUnit ("< 50", "c").clean_value_and_unit () == ("50.0", "celsius")

    assert DataCleaningValueUnit ("9 days", "c").clean_value_and_unit () == ("9.0", "day")

def test_df_transform():
    sample_input = {
        "data": [
            {
                "intervalId": "default",
                "inputs": [
                    {
                        "rowId": "ROW2",
                        "name": "HDT by DMA_HDT Pressure_1",
                        "id": "PRG151_PRM185_1",
                        "value": "6 megapascals",
                        "unit": ""
                    },
                    {
                        "rowId": "ROW3",
                        "name": "HDT by DMA_Temperature Rate_1",
                        "id": "PRG151_PRM106_1",
                        "value": "2",
                        "unit": "Celsius / min"
                    },
                    {
                        "rowId": "ROW4",
                        "name": "HDT by DMA_Temperature Range_1",
                        "id": "PRG151_PRM187_1",
                        "value": "25-200",
                        "unit": "celsius"
                    },
                    {
                        "rowId": "ROW5",
                        "name": "HDT by DMA_Specimen Size_1",
                        "id": "PRG151_PRM139_1",
                        "value": "5.9x3",
                        "unit": "mm\u00b2"
                    },
                    {
                        "rowId": "ROW6",
                        "name": "HDT by DMA_Span Width_1",
                        "id": "PRG151_PRM70_1",
                        "value": "40",
                        "unit": "millimeter"
                    },
                    {
                        "rowId": "ROW7",
                        "name": "HDT by DMA_Number of Duplicates_1",
                        "id": "PRG151_PRM38_1",
                        "value": "1",
                        "unit": "Sample(s)"
                    },
                    {
                        "rowId": "ROW8",
                        "name": "HDT by DMA_Orientation_1",
                        "id": "PRG151_PRM379_1",
                        "value": "Flat",
                        "unit": "Flat or Edge"
                    },
                    {
                        "name": "7534-94-3",
                        "value": 50,
                        "smiles": "CC(=C)C(=O)O[C@H]1C[C@@H]2CC[C@@]1(C)C2(C)C",
                        "albertId": "INVA144441"
                    },
                    {
                        "name": "7732-18-5",
                        "value": 50,
                        "smiles": "O",
                        "albertId": "INVA144441"
                    }
                ],
                "entity": "task",
                "id": "TASFOR100098",
                "parentId": "INVMO3214-001",
                "inventoryId": "INVMO3214-001",
                "workflowId": "WFL36324",
                "projectId": "PROMO3214",
                "modelId": "PMD8",
                "modelVersion": "1.15",
                "modelOrganization": "Albert",
                "modelEndpoint": "/api/v3/propmodels/models/{modelId}/{modelVersion}",
                "dataColumnId": "DAC1011",
                "dataColumnName": "HDT",
                "dataColumnUniqueId": "DAC1011#COL4",
                "dataTemplateId": "DAT39",
                "loopType": "local",
                "predictionType": "loop"
            }
        ]
    }

    sample_output = {
        "data": [
            {
                "intervalId": "default",
                "inputs": [
                    {
                        "name": "HDT by DMA_HDT Pressure_1",
                        "id": "PRG151_PRM185_1",
                        "value": "6.0",
                        "unit": "megapascal",
                        "rowId": "ROW2"
                    },
                    {
                        "name": "HDT by DMA_Temperature Rate_1",
                        "id": "PRG151_PRM106_1",
                        "value": "2.0",
                        "unit": "Celsius / min",
                        "rowId": "ROW3"
                    },
                    {
                        "name": "HDT by DMA_Temperature Range_1",
                        "id": "PRG151_PRM187_1",
                        "value": "112.5",
                        "unit": "celsius",
                        "rowId": "ROW4"
                    },
                    {
                        "name": "HDT by DMA_Specimen Size_1",
                        "id": "PRG151_PRM139_1",
                        "value": "5.9x3",
                        "unit": "mm²",
                        "rowId": "ROW5"
                    },
                    {
                        "name": "HDT by DMA_Span Width_1",
                        "id": "PRG151_PRM70_1",
                        "value": "40.0",
                        "unit": "millimeter",
                        "rowId": "ROW6"
                    },
                    {
                        "name": "HDT by DMA_Number of Duplicates_1",
                        "id": "PRG151_PRM38_1",
                        "value": "1.0",
                        "unit": "Sample(s)",
                        "rowId": "ROW7"
                    },
                    {
                        "name": "HDT by DMA_Orientation_1",
                        "id": "PRG151_PRM379_1",
                        "value": "flat",
                        "unit": "Flat or Edge",
                        "rowId": "ROW8"
                    },
                    {
                        "name": "7534-94-3",
                        "value": 50,
                        "smiles": "CC(=C)C(=O)O[C@H]1C[C@@H]2CC[C@@]1(C)C2(C)C",
                        "albertId": "INVA144441"
                    },
                    {
                        "name": "7732-18-5",
                        "value": 50,
                        "smiles": "O",
                        "albertId": "INVA144441"
                    }
                ],
                "entity": "task",
                "id": "TASFOR100098",
                "parentId": "INVMO3214-001",
                "inventoryId": "INVMO3214-001",
                "workflowId": "WFL36324",
                "projectId": "PROMO3214",
                "modelId": "PMD8",
                "modelVersion": "1.15",
                "modelOrganization": "Albert",
                "modelEndpoint": "/api/v3/propmodels/models/{modelId}/{modelVersion}",
                "dataColumnId": "DAC1011",
                "dataColumnName": "HDT",
                "dataColumnUniqueId": "DAC1011#COL4",
                "dataTemplateId": "DAT39",
                "loopType": "local",
                "predictionType": "loop"
            }
        ],
        "auditFlag": {
            "softFlag": [],
            "hardFlag": []
        }
    }

    assert DataCleaning().transform(sample_input) == sample_output