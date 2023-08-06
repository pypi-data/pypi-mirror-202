import json
import os

import pandas as pd
import pytest
from deepdiff import DeepDiff
from sklearn.pipeline import Pipeline

from albert.api.exceptions import ApiException
from albert.session import AlbertSession
from albert.transforms.dataframe_transforms import FrameMergeUnion, ToDataFrame
from albert.transforms.report_gather import PipelineConfig, ReportGather
from albert.transforms.util_transforms import DictUnionResults, StageLoader


def test_dict_union():
    # Sample data
    data1 = {"key": ["A", "B", "C", "D", "E"], "value": [1, 2, 3, 4, 5]}
    data2 = {"key": ["A", "B", "C", "D", "E"], "value": [644, 7654, 812, 900, 100]}
    df1 = pd.DataFrame(data1)
    df2 = pd.DataFrame(data2)

    jstr = '{"a":1234,"b":"bobjones","c":"asdf1234"}'
    jdoc = json.loads(jstr)

    # Some example jdocs
    docs = [jdoc] * 10

    pipeline = Pipeline(
        [
            (
                "features",
                DictUnionResults(
                    transformer_output_names=["df1", "df2", "jdocs"],
                    transformer_list=[
                        ("obj1", StageLoader(df1)),
                        ("obj2", StageLoader(df2)),
                        ("obj3", StageLoader(docs)),
                    ],
                ),
            ),
        ]
    )
    res = pipeline.transform(None)
    assert "df1" in res.keys()
    assert "df2" in res.keys()
    assert "jdocs" in res.keys()

    assert res["df1"].equals(df1)
    assert res["df2"].equals(df2)
    assert not DeepDiff(docs, res["jdocs"])
