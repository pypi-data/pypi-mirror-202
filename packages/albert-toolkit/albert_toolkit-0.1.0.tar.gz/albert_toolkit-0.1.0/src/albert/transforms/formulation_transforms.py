import logging
from typing import Any

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_array, check_is_fitted, check_X_y

from albert.data.reports import ReportRET28 as unpackReport
from albert.internal.utils import validate_dataframe_has_columns
from albert.pipeline import AlbertConfigurableBaseEstimator

logger = logging.getLogger("TransformModule")
logger.setLevel(logging.DEBUG)
FORMAT = "$(asctime)-15s %(message)s"
logging.basicConfig(format=FORMAT)


class FormulationRescale(BaseEstimator, TransformerMixin):
    """
    For formulations that do not have components that sum to exactly 100
    this transform will appropriately rescale the formulations
    """

    def __init__(self) -> None:
        super().__init__()

    def fit(self, X: Any, y: Any | None = None) -> TransformerMixin:
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        # We are going to form a summation column that represents the sum total
        # composition of a given formula

        # in the result of a report RET27 we have the following columns that we will group by
        # colInventoryId - The specific project formulation id
        # propertyTaskId - The Property Measurement Task Id
        # albertId - The Inventory Id in the formulation -- note that if the Id is a basic raw
        #               material with several CAS components then there will be multiple rows
        #               with the same albertId, one for each CAS component

        # The tuple formed by these three represents a subgroup of rows
        # that reflect the total contribution (through the 'value' field) that this
        # given group makes to the total formula composition
        # NOTE: for a given subgroup the 'value' column will have the same
        # value for all entries, it is the casMaxPercentage column that reflects
        # within that value how much is a particular component.

        # We take the first element in each group since the 'value' entry is the
        # same for all elements of the group -- we just want to know how much
        # this inventory item as a whole contributed to the formulation
        temp_df = (
            df.groupby(["colInventoryId", "propertyTaskId", "albertId"])["value"]
            .first()
            .reset_index()
        )

        # Rename and type the value column to total_calculated, this is
        # the column we will aggregate over when adding up the contribution of
        # each inventory item in the formulation.
        temp_df.rename(columns={"value": "total_calculated"}, inplace=True)
        temp_df["total_calculated"] = temp_df["total_calculated"].astype(float)

        # Now we join this new total_calculated column back into the source
        # frame, using the (colInventoryId, propertyTaskId) as an index
        # so that every inventory item within the given project formulation task
        # will know what the sum total of the formula it is a part of was
        df = df.merge(
            temp_df.groupby(["colInventoryId", "propertyTaskId"])["total_calculated"]
            .sum()
            .reset_index(),
            on=["colInventoryId", "propertyTaskId"],
        )
        df["value"] = df["value"].astype(float)
        df["value_orig"] = df["value"]

        # Now we take each value and rescale it by 100/T where T is the actual total
        # this gives us the new value of that inventory item when the formula sums to 100
        df.loc[:, "value"] *= 100 / df.loc[:, "total_calculated"]
        df["total_orig"] = df["total"]

        # Now every formula will sum to 100 set the 'total' column so it reflect this.
        df["total"] = 100
        return df


class FormulationUnpack(AlbertConfigurableBaseEstimator, TransformerMixin):
    """
    Consumes a formulation data frame and unpacks composite formula inventory items into
    raw CAS components.
    """

    def __init__(self) -> None:
        super().__init__()

    def fit(self, X: Any, y=None) -> TransformerMixin:
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        assert isinstance(X, pd.DataFrame), "input should be a pandas dataframe"
        assert "inventoryId" in X, "input should contain an inventoryId column"

        if "unpackLevel" not in X.columns:
            X["unpackLevel"] = 0

        def _recursive_unpack(X: pd.DataFrame, level: int = 1):
            # See if we have any formulas to unpack
            parent_df = X[X.inventoryId == "Formulas"]

            # no formulas to unpack? Just return the original DF
            if len(parent_df) == 0:
                return X

            # Grab the original DF w the nested formulas dropped from the frame
            # this will be what we push the unpacked formulas back into
            out_df = X[X.inventoryId != "Formulas"].copy(deep=True)

            all_childProductInventory = list(set(parent_df["childProductInventory"]))

            child_df = pd.DataFrame(
                # Use the PipelineConfig object to get an albert session and call the reporting API
                self.config.session.get_report_obj("RET28").get(
                    all_childProductInventory
                )
            )

            # Drop any duplicate records
            child_df.drop_duplicates(inplace=True)

            child_df["unpackLevel"] = level

            # Merge child and parent formulations DataFrames
            child_df = child_df.merge(
                parent_df,
                left_on=["colInventoryId"],
                right_on=["childProductInventory"],
                how="left",
                suffixes=("", "_y"),
            )

            # Scale child proportions based on parent formulation
            child_df["value"] = child_df["value"].astype(float)
            child_df["value"] *= child_df["value_y"] / child_df["total"]

            # DataFrame cleaning
            child_df.drop(
                [
                    "colInventoryId",
                    "productName",
                    "total",
                    "albertId_y",
                    "casName_y",
                    "inventoryName_y",
                    "value_y",
                    "inventoryId_y",
                    "childProductInventory_y",
                    "casPercentageMax_y",
                    "casCategoryId_y",
                    "unpackLevel_y",
                ],
                axis=1,
                inplace=True,
            )

            child_df.rename(
                columns={
                    "colInventoryId_y": "colInventoryId",
                    "productName_y": "productName",
                    "total_y": "total",
                },
                inplace=True,
            )

            # Consolidate duplicate CAS #'s
            child_df.casName.fillna("Unknown", inplace=True)
            child_df.casPercentageMax.fillna(100, inplace=True)

            child_df = (
                child_df.groupby(
                    [
                        "colInventoryId",
                        "propertyTaskId",
                        "albertId",
                        "casName",
                        "casPercentageMax",
                    ]
                )
                .agg(
                    {
                        "productName": "first",
                        "total": "first",
                        "inventoryName": "first",
                        "inventoryId": "first",
                        "childProductInventory": "first",
                        "casCategoryId": "first",
                        "unpackLevel": "first",
                        "value": "sum",
                    }
                )
                .reset_index()
            )

            return pd.concat(
                [out_df, _recursive_unpack(child_df, level + 1)]
            ).reset_index(drop=True)

        return _recursive_unpack(X, 1)


class FormulationPivot(
    BaseEstimator,
    TransformerMixin,
):
    """
    Consumes a data frame that contains raw property data and converts it into
    a formulation pivot
    """

    def __init__(self) -> None:
        super().__init__()

    def fit(self, X, y) -> TransformerMixin:
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        assert isinstance(X, pd.DataFrame), "input should be a pandas dataframe"
        assert validate_dataframe_has_columns(
            X,
            [
                "colInventoryId",
                "propertyTaskId",
                "albertId",
                "casPercentageMax",
                "casName",
                "value",
            ],
        ), "dataframe does not contain the required columns for this transform"

        # Get CAS sum totals for all raw materials
        X["CasMaxSum"] = X.groupby(["colInventoryId", "propertyTaskId", "albertId"])[
            "casPercentageMax"
        ].transform(lambda x: sum(x))

        # Downselect for raw materials with sums below 100 (99.9 used to ignore roundoff error)
        rawmat_unknowns = X[X["CasMaxSum"] < 99.9]
        # Keep only one copy of each raw materials
        rawmat_unknowns.drop_duplicates(
            subset=["colInventoryId", "propertyTaskId", "albertId"], inplace=True
        )

        # Append copies of rawmat rows back to original dataqframe but with
        # casCategoryId of 7 -- What the hell is this??
        X = X.append(
            rawmat_unknowns.assign(**{"casCategoryId": 7, "casPercentageMax": np.nan})
        )

        # Backfill nans to amount missing in raw material
        X["casPercentageMax"].fillna(100 - X["CasMaxSum"], inplace=True)

        # Adjust CasMaxSum to 100 for all updated raw materials
        X["CasMaxSum"] = np.where(X["CasMaxSum"] < 100, 100, X["CasMaxSum"])

        # Create updated name column for raw materials with unknown CAS #'s
        # Here anywhere we have an unknown we are going to rename it to
        # <albertId>_Unknown to indicate it is an inventory item with unknown cas
        X["updated_cas_name"] = np.where(
            (X["casCategoryId"] == 7) | (X["casName"].str.contains("Unknown")),
            X["albertId"].astype("str") + "_" + "Unknown",
            X["casName"],
        )

        # Calculate the proportions fo all CAS #'s with respect to their parent
        # formulations
        X["ScaledCasMax"] = X["casPercentageMax"] / X["CasMaxSum"] * 100
        X["ScaledValue"] = X["value"] * X["ScaledCasMax"] / 100

        # Merge CAS #'s that repeat across multiple raw materials..
        X = (
            X.groupby(["colInventoryId", "propertyTaskId", "updated_cas_name"])
            .agg({"ScaledValue": "sum"})
            .reset_index()
        )

        # Generate formulation/CAS # pivot table
        pivot = pd.pivot_table(
            X,
            values="ScaledValue",
            index=["colInventoryId", "propertyTaskId"],
            columns=["updated_cas_name"],
        ).reset_index()
        pivot.fillna(0, inplace=True)
        pivot.columns.name = "Components"
        pivot.index.name = "Formula"
        return pivot
