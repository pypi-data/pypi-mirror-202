import os

import pandas as pd
import pytest
from libjwtpython.token_auth import signJWT
from sklearn.pipeline import Pipeline

from albert.api.exceptions import ApiException
from albert.session import AlbertSession
from albert.transforms.dataframe_transforms import FrameMergeUnion, ToDataFrame
from albert.transforms.report_gather import PipelineConfig, ReportGather


@pytest.fixture
def config() -> PipelineConfig:
    if "ALBERT_TOKEN_DEV" in os.environ:
        token = os.environ["ALBERT_TOKEN_DEV"]
    elif "JWT_TOKEN_SECRET" in os.environ:  # For CI Runners
        token: str = signJWT(
            sub="ALB#USR4",
            tenantId="TEN1",
            partition="",
            role="ALB#ROL3",
            uclass="admin",
            exp=900,
            aud="albert",
            version=2,
            userTypeId=1,
            name="DataScience",
        )
        os.environ["ALBERT_TOKEN_DEV"] = token
    else:
        raise KeyError("no token is available -- cannot continue")
    return PipelineConfig(
        AlbertSession(
            endpoint=AlbertSession.default_dev_host,
            token=token,
        ),
        {},
    )


def test_report_gather_ret27(config: PipelineConfig):
    rg = ReportGather(
        "RET27",
        {
            "dataColumnId": "DAC604",
            "dataTemplateId": "DAT34",
            "batch_size": 50000,
        },
    )

    # TODO Figure out some good ways to test that the result is a valid frame
    df = pd.DataFrame(rg.transform(config))
    print(df)


def test_report_gather_ret28(config: PipelineConfig):
    rg = ReportGather(
        "RET28",
        {"formulas": ["INVEXP2746-003"]},
    )

    # TODO Figure out some good ways to test that the result is a valid frame
    df = pd.DataFrame(rg.transform(config))
    print(df)


def test_report_gather_noimpl(config: PipelineConfig):
    rg = ReportGather("RET15", {})
    with pytest.raises(NotImplementedError, match="cannot find implementation"):
        rg.transform(config)


def test_report_gather_noreport(config: PipelineConfig):
    rg = ReportGather("RETNONE", {})
    with pytest.raises(ApiException, match="(404)"):
        rg.transform(config)


def test_report_gather_pipeline(config: PipelineConfig):
    report_params = {
        "dataColumnId": "DAC1889",
        "dataTemplateId": "DAT34",
        "batch_size": 50000,
    }
    pipe = Pipeline(
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
        ]
    )
    pipe.transform(config)
