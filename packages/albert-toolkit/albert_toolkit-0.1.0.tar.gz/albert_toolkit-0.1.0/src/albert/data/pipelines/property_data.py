import os

import dotenv
import pandas as pd

from albert.pipeline import AlbertPipeline, Pipeline, PipelineConfig
from albert.session import AlbertSession
from albert.transforms import (
    DictUnionResults,
    FormulationPivot,
    FormulationRescale,
    FormulationUnpack,
    FrameCleanup,
    FrameMergeUnion,
    PropertyPivot,
    ToDataFrame,
)
from albert.transforms.operating_condition_transforms import (
    ToUnitDictionary,
    RepeatStepPropertyTask,
    UpdateDuplicateSOPOPC,
    FormSOPKeys,
    UpdateSOPNames,
)
from albert.transforms.report_gather import ReportGather

__all__ = [
    "FormulationPivotPipeline",
    "PropertyPivotPipeline",
    "UnitDictionaryPipeline",
    "OperatingConditionsPipeline",
]


class FormulationPivotPipeline(Pipeline):
    """
    A pipeline class for transforming raw formulation data into a formulation pivot

    Parameters:
        dataColumnId (str): The id of the data column to pull from the report.
        dataTemplateId (str): The id of the data template to use.

    Methods:
        __init__(self, dataColumnId, dataTemplateId): Constructor method. Initializes the pipeline with a series of
            transformation steps to be applied to the data.
    """

    def __init__(self, dataColumnId, dataTemplateId):
        """
        Constructor method. Initializes the pipeline with a series of transformation steps to be applied to the data.

        Parameters:
            dataColumnId (str): The id of the data column to pull from the report.
            dataTemplateId (str): The id of the data template to use.
        """

        self.dataColumnId = dataColumnId
        self.dataTemplateId = dataTemplateId

        # Create a dictionary of report parameters.
        report_params = {
            "dataColumnId": dataColumnId,
            "dataTemplateId": dataTemplateId,
            "batch_size": 50000,
        }

        # Build all the steps of the pipeline in the constructor of the base pipeline class
        super().__init__(
            [
                ("pull", ReportGather("RET27", report_parameters=report_params)),
                ("todf", ToDataFrame()),
                ("rescale", FormulationRescale()),
                (
                    "clean",
                    FrameCleanup(
                        drop_duplicates=True,
                        nan_fills={"casName": "Unknown", "casPercentageMax": 100},
                    ),
                ),
                ("unpack", FormulationUnpack()),
                ("pivot", FormulationPivot()),
            ]
        )


class PropertyPivotPipeline(Pipeline):
    """
    A pipeline class for transforming property data.

    Parameters:
        dataColumnId (str): The id of the data column to pull from the report.
        dataTemplateId (str): The id of the data template to use.

    Methods:
        __init__(self, dataColumnId, dataTemplateId): Constructor method. Initializes the pipeline with a series of
            transformation steps to be applied to the data.
    """

    def __init__(self, dataColumnId, dataTemplateId):
        """
        Constructor method. Initializes the pipeline with a series of transformation steps to be applied to the data.

        Parameters:
            dataColumnId (str): The id of the data column to pull from the report.
            dataTemplateId (str): The id of the data template to use.
        """

        self.dataColumnId = dataColumnId
        self.dataTemplateId = dataTemplateId

        # Create a dictionary of report parameters.
        report_params = {"dataColumnId": dataColumnId, "dataTemplateId": dataTemplateId}

        # Build all the steps of the pipeline in the constructor of the base pipeline class
        super().__init__(
            [
                ("pull", ReportGather("RET30", report_parameters=report_params)),
                ("todf", ToDataFrame()),
                ("pivot", PropertyPivot()),
            ]
        )


class _BaseUnitDictionaryPipeline(Pipeline):
    def __init__(self, dataColumnId, dataTemplateId):
        self.dataColumnId = dataColumnId
        self.dataTemplateId = dataTemplateId

        report_params = {"dataColumnId": dataColumnId, "dataTemplateId": dataTemplateId}
        super().__init__(
            [
                ("pull", ReportGather("RET32", report_parameters=report_params)),
                ("todf", ToDataFrame()),
                ("clean_nan", FrameCleanup(nan_drops=["parameterId"])),
                ("clean_fillna", FrameCleanup(nan_fills={"__all__": ""})),
                ("sopKey", FormSOPKeys()),
                ("unit_dict", ToUnitDictionary()),
            ]
        )


class _RepeatDFPipeline(Pipeline):
    def __init__(self, dataColumnId, dataTemplateId):
        self.dataColumnId = dataColumnId
        self.dataTemplateId = dataTemplateId

        report_params = {"dataColumnId": dataColumnId, "dataTemplateId": dataTemplateId}
        super().__init__(
            [
                ("pull", ReportGather("RET33", report_parameters=report_params)),
                ("todf", ToDataFrame()),
                ("clean_nan", FrameCleanup(nan_drops=["parameterId"])),
                ("clean_fillna", FrameCleanup(nan_fills={"__all__": ""})),
                ("sopKey", FormSOPKeys()),
                ("repeat", RepeatStepPropertyTask()),
            ]
        )


class UnitDictionaryPipeline(Pipeline):
    def __init__(self, dataColumnId, dataTemplateId):
        self.dataColumnId = dataColumnId
        self.dataTemplateId = dataTemplateId

        report_params = {"dataColumnId": dataColumnId, "dataTemplateId": dataTemplateId}
        super().__init__(
            [
                (
                    "features",
                    DictUnionResults(
                        ["unit_dict", "repeat_df"],
                        [
                            (
                                "pull_unit_dict",
                                _BaseUnitDictionaryPipeline(**report_params),
                            ),
                            ("pull_repeat_df", _RepeatDFPipeline(**report_params)),
                        ],
                        n_jobs=2,
                    ),
                ),
                ("dict_apply", UpdateDuplicateSOPOPC()),
            ]
        )


class OperatingConditionsPipeline(Pipeline):
    """
    Pipeline which implements the operatingCondition_query & update_sopnames
    from legacy system
    """

    def __init__(self, dataColumnId, dataTemplateId):
        self.dataColumnId = dataColumnId
        self.dataTemplateId = dataTemplateId

        report_params = {"dataColumnId": dataColumnId, "dataTemplateId": dataTemplateId}
        super().__init__(
            [
                ("pull", ReportGather("RET31", report_parameters=report_params)),
                ("todf", ToDataFrame()),
                ("clean_nan", FrameCleanup(nan_drops=["parameterId"])),
                ("clean_fillna", FrameCleanup(nan_fills={"shortName": ""})),
                ("sopKey", FormSOPKeys()),
                ("updateKeys", UpdateSOPNames()),
            ]
        )
