from albert.transforms.report_gather import ReportGather
from albert.session import AlbertSession
from albert.api.exceptions import ApiException
from sklearn.pipeline import Pipeline
from albert.pipeline import AlbertPipeline, PipelineConfig
from albert.data.reports import ReportRET28
from albert.transforms import (
    FrameMergeUnion,
    ToDataFrame,
    FrameCleanup,
    FormulationRescale,
    FormulationUnpack,
)
import os
import pandas as pd
import dotenv
from sklearn.preprocessing import StandardScaler
import pytest


@pytest.mark.usefixtures("ci_tokenset")
def test_nested_pipeline_configure():
    # Parallel Paths with a simple Join on a dataframe column
    report_params = {
        "dataColumnId": "DAC335",
        "dataTemplateId": "DAT286",
        "batch_size": 50000,
    }
    ret2730merge = FrameMergeUnion(
        merge_on="propertyTaskId",
        n_jobs=2,
        transformer_list=[
            (
                "ret27",
                Pipeline(
                    [
                        (
                            "pull",
                            ReportGather("RET27", report_parameters=report_params),
                        ),
                        ("todf", ToDataFrame()),
                        ("rescale", FormulationRescale()),
                        (
                            "clean",
                            FrameCleanup(
                                drop_duplicates=True,
                                nan_fills={
                                    "casName": "Unknown",
                                    "casPercentageMax": 100,
                                },
                            ),
                        ),
                        ("unpack", FormulationUnpack()),
                        # ('pivot',FormulationPivot())
                    ]
                ),
            ),
            (
                "ret30",
                Pipeline(
                    [
                        (
                            "pull",
                            ReportGather("RET30", report_parameters=report_params),
                        ),
                        ("todf", ToDataFrame()),
                        # ('pivot',PropertyPivot())
                    ]
                ),
            ),
        ],
    )
    pipe = AlbertPipeline(
        PipelineConfig(
            session=AlbertSession(
                endpoint="https://dev.albertinventdev.com",
                token=os.environ["ALBERT_TOKEN_DEV"],
            )
        ),
        [
            (
                "features",
                FrameMergeUnion(
                    merge_on=["propertyTaskId", "intervalOrder"],
                    n_jobs=2,
                    transformer_list=[
                        ("ret2730merge", ret2730merge),  # Nested FrameMergeUnion
                        (
                            "Ret38",
                            Pipeline(
                                [
                                    (
                                        "pull",
                                        ReportGather(
                                            "RET30", report_parameters=report_params
                                        ),
                                    ),
                                    ("todf", ToDataFrame()),
                                    # ('pivot',PropertyPivot())
                                ]
                            ),
                        ),
                    ],
                ),
            )
        ],
    )
    pipe.run()


@pytest.mark.usefixtures("ci_tokenset")
def test_pipeline_configure():
    report_params = {
        "dataColumnId": "DAC335",
        "dataTemplateId": "DAT286",
        "batch_size": 50000,
    }
    pipe = AlbertPipeline(
        PipelineConfig(
            session=AlbertSession(
                endpoint="https://dev.albertinventdev.com",
                token=os.environ["ALBERT_TOKEN_DEV"],
            )
        ),
        [
            (
                "features",
                FrameMergeUnion(
                    merge_on="propertyTaskId",
                    n_jobs=2,
                    transformer_list=[
                        (
                            "ret27",
                            Pipeline(
                                [
                                    (
                                        "pull",
                                        ReportGather(
                                            "RET27", report_parameters=report_params
                                        ),
                                    ),
                                    ("todf", ToDataFrame()),
                                    ("rescale", FormulationRescale()),
                                    (
                                        "clean",
                                        FrameCleanup(
                                            drop_duplicates=True,
                                            nan_fills={
                                                "casName": "Unknown",
                                                "casPercentageMax": 100,
                                            },
                                        ),
                                    ),
                                    ("unpack", FormulationUnpack()),
                                    ("scalar", StandardScaler())
                                    # ('pivot',FormulationPivot())
                                ]
                            ),
                        ),
                        (
                            "ret30",
                            Pipeline(
                                [
                                    (
                                        "pull",
                                        ReportGather(
                                            "RET30", report_parameters=report_params
                                        ),
                                    ),
                                    ("todf", ToDataFrame()),
                                    # ('pivot',PropertyPivot())
                                ]
                            ),
                        ),
                    ],
                ),
            )
        ],
    )
