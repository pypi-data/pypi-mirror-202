import logging
from typing import Any, Dict, Callable

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_array, check_is_fitted, check_X_y

from albert.data.reports import ReportRET28 as unpackReport
from albert.internal.utils import validate_dataframe_has_columns
from albert.pipeline import AlbertConfigurableBaseEstimator
from albert.transforms.util_transforms import DictApply


class ToUnitDictionary(BaseEstimator, TransformerMixin):
    def __init__(self) -> None:
        super().__init__()

    def fit(self, X: Any, y: Any | None = None):
        return self

    def transform(self, X: pd.DataFrame) -> dict[str, str]:
        assert validate_dataframe_has_columns(
            X, ["parameterGroupId", "parameterId", "unitCount", "sopOperatingCondition"]
        ), "required columns were not found"

        units = X.loc[
            X.groupby(["parameterGroupId", "parameterId", "sopOperatingCondition"])[
                "unitCount"
            ].idxmax()
        ]

        unit_dict = dict(zip(units.sopOperatingCondition, units.unitName))

        return unit_dict


class RepeatStepPropertyTask(BaseEstimator, TransformerMixin):
    def __init__(self) -> None:
        super().__init__()

    def fit(self, X: Any, y: Any | None = None):
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        assert validate_dataframe_has_columns(
            X, ["parameterGroupId", "parameterId", "sopOperatingCondition"]
        ), "required columns are missing in dataframe"

        return (
            X.groupby("sopOperatingCondition")
            .agg({"parameterGroupParameterCount": max})
            .reset_index()
        )


class UpdateDuplicateSOPOPC(DictApply):
    def __init__(self) -> None:
        super().__init__(self.update_func)

    def update_func(self, data: Dict[str, Any]) -> Dict[str, Any]:
        repeat_df = data["repeat_df"]
        unit_dict = data["unit_dict"]
        # TODO: Get rid of nested for loop
        for idx, row in repeat_df.iterrows():
            temp = row["sopOperatingCondition"]
            for idx in range(int(row["parameterGroupParameterCount"])):
                if idx != 0:
                    unit_dict[f"{row['sopOperatingCondition']}_{idx + 1}"] = unit_dict[
                        f"{row['sopOperatingCondition']}_{idx}"
                    ]
                else:
                    unit_dict[
                        f"{row['sopOperatingCondition']}_{idx + 1}"
                    ] = unit_dict.pop(temp)

        return unit_dict


class FormSOPKeys(BaseEstimator, TransformerMixin):
    def __init__(self) -> None:
        super().__init__()

    def fit(self, X: Any, y: Any | None = None):
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        assert validate_dataframe_has_columns(X, ["parameterGroupId", "parameterId"])

        X["sopOperatingCondition"] = X["parameterGroupId"] + "_" + X["parameterId"]

        return X


class UpdateSOPNames(BaseEstimator, TransformerMixin):
    def __init__(self) -> None:
        super().__init__()

    def fit(self, X: Any, y: Any | None = None):
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        assert validate_dataframe_has_columns(
            X,
            [
                "parameterValue",
                "parameterId",
                "propertyTaskId",
                "intervalOrder",
                "parameterGroupId",
                "parameterGroup",
                "sequenceOrder",
                "sopOperatingCondition",
            ],
        )

        # Replace different forms of None Values with NaN's
        X["parameterValue"] = (
            X["parameterValue"]
            .astype(str)
            .str.lower()
            .replace(
                to_replace=["none", None, "unknown", "nan", "na", "n.a.", "n/a", ""],
                value=np.NaN,
            )
        )

        # Convert parameterId's to str type -- #TODO Why?
        X.dropna(subset=["parameterId"], inplace=True)
        X["parameterId"] = X["parameterId"].astype(str)
        X.drop_duplicates(inplace=True)

        # Fill NaN's for interval to keep non-interval data in groupBy
        X["intervalOrder"].fillna(0, inplace=True)

        # Identify duplicate operating conditions at the interval level
        X.sort_values(
            by=[
                "propertyTaskId",
                "intervalOrder",
                "parameterGroupId",
                "parameterId",
                "parameterGroup",
                "sequenceOrder",
            ],
            inplace=True,
        )

        updated_df = (
            X.reset_index()
            .groupby(["propertyTaskId", "intervalOrder", "sopOperatingCondition"])
            .agg({"index": "unique"})
            .reset_index()
        )

        # Update duplicate sopOperatingCondition names in DF
        def update_dupes(x):
            temp = [
                x["sopOperatingCondition"] + "_" + str(y + 1)
                for y in range(len(x["index"]))
            ]

            for idx, val in enumerate(temp):
                X.loc[x["index"][idx], "sopOperatingCondition"] = val

        updated_df.apply(update_dupes, axis=1)

        # cast OPC value column to a string and remove double underscore
        # from sopOperatingConditions
        X["parameterValue"] = X["parameterValue"].astype(str)
        X["sopOperatingCondition"] = X["sopOperatingCondition"].apply(
            lambda x: x.replace("__", "_")
        )
        X.rename(
            columns={
                "sopOperatingCondition": "name",
                "parameterValue": "value",
                "unitName": "unit",
            },
            inplace=True,
        )

        X["intervalOrder"] = X["intervalOrder"].astype(float)

        return X
