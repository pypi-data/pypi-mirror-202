import pandas as pd
import pytest
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.utils.estimator_checks import parametrize_with_checks

from albert.transforms.dataframe_transforms import (FrameMergeUnion,
                                                    FrameSelector, FrameSet)

# @parametrize_with_checks([FrameSelector("")])
# def test_sklearn_compatible_transform(estimator, check):
#     check(estimator)


def test_frame_selector_transform():
    df1 = pd.DataFrame({"A": ["a", "b", "c", "d"], "B": [0, 1, 2, 3]})
    df2 = pd.DataFrame({"A": ["e", "f", "g", "h"], "B": [4, 5, 6, 7]})

    df_set = FrameSet({"primary": df1, "secondary": df2})

    assert FrameSelector("primary").fit_transform(df_set).equals(df1)
    assert FrameSelector("secondary").fit_transform(df_set).equals(df2)


def test_frame_selector_in_pipeline():
    # Sample data
    data1 = {"key": ["A", "B", "C", "D", "E"], "value": [1, 2, 3, 4, 5]}
    data2 = {"key": ["A", "B", "C", "D", "E"], "value": [644, 7654, 812, 900, 100]}
    df1 = pd.DataFrame(data1)
    df2 = pd.DataFrame(data2)

    pipeline = Pipeline(
        [
            (
                "features",
                FeatureUnion(
                    n_jobs=1,
                    transformer_list=[
                        (
                            "df1",
                            Pipeline(
                                [
                                    ("selector", FrameSelector("primary")),
                                ]
                            ),
                        ),
                        (
                            "df2",
                            Pipeline(
                                [
                                    ("selector", FrameSelector("secondary")),
                                ]
                            ),
                        ),
                    ],
                ),
            ),
        ]
    )

    res = pipeline.fit_transform(FrameSet({"primary": df1, "secondary": df2}))
    print(res)
