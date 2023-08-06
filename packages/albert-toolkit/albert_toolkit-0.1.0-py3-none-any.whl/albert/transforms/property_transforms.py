import logging
from typing import Any

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_array, check_is_fitted, check_X_y

from albert.data.reports import ReportRET28 as unpackReport
from albert.internal.utils import validate_dataframe_has_columns
from albert.pipeline import AlbertConfigurableBaseEstimator


class PropertyPivot(AlbertConfigurableBaseEstimator, TransformerMixin):
    def __init__(self) -> None:
        super().__init__()

    def fit(self, X: Any, y: Any | None = None):
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        assert validate_dataframe_has_columns(
            X, ["dataPoint", "propertyTaskId", "intervalOrder", "trialNo"]
        ), "input dataframe is missing required columns"

        # Convert column typing from str to float
        X["dataPoint"] = pd.to_numeric(X["dataPoint"], errors="coerce")

        # Fill NaN's for intervals to keep non-interval data in groupby
        X["intervalOrder"].fillna(0, inplace=True)

        # Create aggregate to merge to formulations pivot
        new_df = (
            X.groupby(["propertyTaskId", "intervalOrder"])
            .agg(
                propertyDataPoint_mean=pd.NamedAgg(column="dataPoint", aggfunc=np.mean),
                propertyDataPoint_std=pd.NamedAgg(column="dataPoint", aggfunc=np.std),
                trialCount=pd.NamedAgg(column="trialNo", aggfunc="count"),
            )
            .reset_index()
        )

        # Rename summary statistic columns with appropriate property name
        new_df.rename(
            columns={
                "propertyDataPoint_mean": f"{X.loc[0, 'dataColumnName']}_mean",
                "propertyDataPoint_std": f"{X.loc[0, 'dataColumnName']}_std",
            },
            inplace=True,
        )

        # Drop rows that don't have property data points from string coercion
        new_df.dropna(
            subset=[f"{X.loc[0, 'dataColumnName']}_mean"],
            axis=0,
            inplace=True,
        )

        return new_df
