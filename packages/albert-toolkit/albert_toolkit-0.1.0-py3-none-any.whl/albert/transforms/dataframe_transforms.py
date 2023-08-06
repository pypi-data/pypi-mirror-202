from typing import Any, Dict, List

import numpy as np
from pandas import DataFrame
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import FeatureUnion
from sklearn.utils.validation import check_array, check_is_fitted, check_X_y

# __all__ = ["FrameSet", "FrameSelector", "FrameTypeSelector", "FrameMergeUnion"]


class FrameSet:
    """A class for holding a set of pandas DataFrames

    Attributes:
        frames (Dict[str, pandas.DataFrame]): a dictionary that holds the name-dataframe pairs.
    """

    def __init__(self, frames: Dict[str, DataFrame]) -> None:
        """Initialize the FrameSet object.

        Args:
            frames (Dict[str, pandas.DataFrame]): a dictionary that holds the name-dataframe pairs.
        """
        self.frames = frames

    def add_frame(self, name: str, frame: DataFrame, overwrite=False) -> None:
        """Add a new DataFrame to the set.

        Args:
            name (str): the name of the DataFrame
            frame (pandas.DataFrame): the DataFrame to add
            overwrite (bool, optional): whether to overwrite an existing DataFrame with the same name. Defaults to False.

        Raises:
            KeyError: if the frame name is already in the set and overwrite is set to False
        """
        if (name in self.frames) and (not overwrite):
            raise KeyError(
                f"the frame name {name} is already in the set and overwrite is set to false"
            )

        self.frames[name] = frame

    def drop_frame(self, name: str) -> None:
        """Remove a DataFrame from the set.

        Args:
            name (str): the name of the DataFrame to remove
        """
        if name in self.frames:
            del self.frames[name]

    def __getitem__(self, key: str) -> DataFrame:
        """Access a DataFrame by its name.

        Args:
            key (str): the name of the DataFrame to access

        Raises:
            KeyError: if no frame with the given name is in the set

        Returns:
            pandas.DataFrame: the DataFrame with the given name
        """
        if key not in self.frames:
            raise KeyError(f"no frame with the name {key} was in the FrameSet")
        return self.frames[key]

    def has_frame(self, key: str) -> bool:
        """Check if a DataFrame with the given name is in the set.

        Args:
            key (str): the name of the DataFrame to check

        Returns:
            bool: True if the DataFrame is in the set, False otherwise
        """
        if key in self.frames:
            return True
        return False


class FrameCleanup(BaseEstimator, TransformerMixin):
    """
    A custom transformer that cleans up the input DataFrame by dropping duplicates,
    filling in NaN values, and dropping specified columns.

    Parameters:
    ----------
    drop_duplicates: bool
        Whether to drop duplicate rows from the DataFrame.
    nan_fills: Dict or None
        A dictionary where keys are column names and values are the values used to fill
        NaN values in those columns.
    nan_drops: List[str] or None
        A list of column names to drop if they contain NaN values.
    drop_columns: List[str] or List[int] or None
        A list of column names or indices to drop from the DataFrame.
    inplace: bool
        Whether to perform the clean-up in place or to return a new DataFrame.

    Methods:
    -------
    fit(X, y=None):
        This method does not perform any action and only returns the object itself.

    transform(X):
        Cleans up the input DataFrame by dropping duplicates, filling in NaN values,
        and dropping specified columns.

        Parameters:
        ----------
        X: pandas DataFrame
            The input DataFrame to be cleaned up.

        Returns:
        -------
        pandas DataFrame:
            The cleaned up DataFrame.
    """

    def __init__(
        self,
        drop_duplicates: bool = False,
        nan_fills: dict | None = None,
        nan_drops: list[str] | None = None,
        drop_columns: list[str] | list[int] | None = None,
        inplace: bool = True,
    ) -> None:
        """
        Initializes an instance of FrameCleanup class.

        Parameters:
        ----------
        drop_duplicates: bool
            Whether to drop duplicate rows from the DataFrame.
        nan_fills: Dict or None
            A dictionary where keys are column names and values are the values used to fill
            NaN values in those columns.
        nan_drops: List[str] or None
            A list of column names to drop if they contain NaN values.
        drop_columns: List[str] or List[int] or None
            A list of column names or indices to drop from the DataFrame.
        inplace: bool
            Whether to perform the clean-up in place or to return a new DataFrame.
        """
        super().__init__()

        self.drop_duplicates: bool = drop_duplicates
        self.nan_fills: dict | None = nan_fills
        self.nan_drops: list[str] | None = nan_drops
        self.drop_columns: list[str] | list[int] | None = drop_columns
        self.inplace: bool = inplace

    def fit(self, X: Any, y: Any | None = None):
        """
        This method does not perform any action and only returns the object itself.

        Parameters:
        ----------
        X: pandas DataFrame
            The input DataFrame to be cleaned up.
        y: Not used

        Returns:
        -------
        FrameCleanup:
            The same object that is passed to the method.
        """
        return self

    def transform(self, X: DataFrame) -> DataFrame:
        """
        Cleans up the input DataFrame by dropping duplicates, filling in NaN values,
        and dropping specified columns.

        Parameters:
        ----------
        X: pandas DataFrame
            The input DataFrame to be cleaned up.

        Returns:
        -------
        pandas DataFrame:
            The cleaned up DataFrame.
        """
        if not isinstance(X, DataFrame):
            raise TypeError(
                f"cannot perform a data frame cleanup operation on {type(X)}"
            )

        out_df = X

        if self.nan_fills is not None:
            self._fillna_values(out_df)

        if self.nan_drops is not None:
            self._dropna_values(out_df)

        if self.drop_duplicates:
            self._drop_duplicates(out_df)

        if self.drop_columns is not None:
            self._drop_columns(out_df)

        return out_df

    def _fillna_values(self, df: DataFrame) -> None:
        """
        Fills NaN values in the DataFrame with the specified values.

        Parameters:
        ----------
        df: pandas DataFrame
            The input DataFrame to be cleaned up.
        """
        for k, v in self.nan_fills.items():
            if self.inplace:
                if k == "__all__":
                    df.fillna(v, inplace=True)
                else:
                    df[k].fillna(v, inplace=True)
            else:
                if k == "__all__":
                    df = df.fillna(v)
                else:
                    df = df[k].fillna(v)

    def _dropna_values(self, df: DataFrame) -> None:
        """
        Drops rows containing NaN values in the specified columns.

        Parameters:
        ----------
        df: pandas DataFrame
            The input DataFrame to be cleaned up.
        """
        if self.inplace:
            df.dropna(subset=self.nan_drops, inplace=True)
        else:
            df = df.dropna(subset=self.nan_drops)

    def _drop_duplicates(self, df: DataFrame) -> None:
        """
        Drops duplicate rows in the DataFrame.

        Parameters:
        ----------
        df: pandas DataFrame
            The input DataFrame to be cleaned up.
        """
        if self.inplace:
            df.drop_duplicates(inplace=True)
        else:
            df = df.drop_duplicates()

    def _drop_columns(self, df: DataFrame) -> None:
        """
        Drops specified columns from the DataFrame.

        Parameters:
        ----------
        df: pandas DataFrame
            The input DataFrame to be cleaned up.
        """
        curColumns = df.columns
        for ii in self.drop_columns:
            if isinstance(ii, str):
                if self.inplace:
                    df.drop(ii, axis=1, inplace=True)
                else:
                    df = df.drop(ii, axis=1)
            elif isinstance(ii, int):
                if self.inplace:
                    df.drop(curColumns[ii], axis=1, inplace=True)
                else:
                    df = df.drop(curColumns[ii], axis=1)
            else:
                raise TypeError("unknown drop column specification...")


class FrameSelector(BaseEstimator, TransformerMixin):
    """
    Select a specific frame from a collection of frames represented by a dictionary or a FrameSet object.

    Parameters:
    frame_name (str): The name of the frame to be selected.
    """

    def __init__(self, frame_name: str = "") -> None:
        super().__init__()
        self.frame_name = frame_name

    def _more_tags(self):
        return {"no_validation": True}

    def fit(self, X: Any, y: Any | None = None):
        """
        Fit the FrameSelector to the data.

        This is a dummy method that returns self.

        Parameters:
        X (Dict[str, DataFrame] | FrameSet): A collection of data frames.
        y (None): No target variable is expected.

        Returns:
        self
        """

        return self

    def transform(self, X: Dict[str, DataFrame] | FrameSet) -> DataFrame:
        """
        Select a specific data frame from the collection.

        Parameters:
        X (Dict[str, DataFrame] | FrameSet): A collection of data frames.

        Returns:
        DataFrame: The selected data frame.

        Raises:
        TypeError: If X is not of type Dict[str, DataFrame] or FrameSet.
        KeyError: If the frame with the specified name is not present in the collection.
        """

        if not isinstance(X, (Dict, FrameSet)):
            raise TypeError(
                f"cannot operate FrameSelector on type {type(X)} non Dict[str, DataFrame]"
                " | FrameSet types"
            )

        if isinstance(X, FrameSet):
            if not X.has_frame(self.frame_name):
                raise KeyError(
                    f"frame name {self.frame_name} is not present in the frame collection"
                )
        else:
            if self.frame_name not in X:
                raise KeyError(
                    f"frame name {self.frame_name} is not present in the frame collection"
                )

        return X[self.frame_name]


class FrameTypeSelector(BaseEstimator, TransformerMixin):
    """
    A custom transformer that selects the columns of the input DataFrame that match the given data type.

    Parameters:
    ----------
    dtype : str or type
        The data type or string representation of the data type to select.

    Methods:
    -------
    fit(X, y=None):
        This method does not perform any action and only returns the object itself.

    transform(X):
        Selects the columns of the input DataFrame that match the given data type.

        Parameters:
        ----------
        X: pandas DataFrame
            The input DataFrame from which to select columns.

        Returns:
        -------
        pandas DataFrame:
            A new DataFrame with only the columns that match the given data type.
    """

    def __init__(self, dtype):
        """
        Initializes an instance of FrameTypeSelector class.

        Parameters:
        ----------
        dtype: str or type
            The data type or string representation of the data type to select.
        """
        self.dtype = dtype

    def fit(self, X: Any, y: Any | None = None):
        """
        This method does not perform any action and only returns the object itself.

        Parameters:
        ----------
        X: pandas DataFrame
            The input DataFrame from which to select columns.

        y: Not used

        Returns:
        -------
        FrameTypeSelector:
            The same object that is passed to the method.
        """
        return self

    def transform(self, X):
        """
        Selects the columns of the input DataFrame that match the given data type.

        Parameters:
        ----------
        X: pandas DataFrame
            The input DataFrame from which to select columns.

        Returns:
        -------
        pandas DataFrame:
            A new DataFrame with only the columns that match the given data type.
        """
        assert isinstance(X, DataFrame), "Input X is not a pandas DataFrame"
        return X.select_dtypes(include=[self.dtype])


class ToDataFrame(BaseEstimator, TransformerMixin):
    """
    A custom transformer that converts the input data to a pandas DataFrame.

    Methods:
    -------
    fit(X, y=None):
        This method does not perform any action and only returns the object itself.

    transform(X):
        Converts the input data to a pandas DataFrame.

        Parameters:
        ----------
        X: Any
            The input data to be converted to a pandas DataFrame.

        Returns:
        -------
        pandas DataFrame:
            The input data as a pandas DataFrame.
    """

    def fit(self, X: Any, y: Any | None = None):
        """
        This method does not perform any action and only returns the object itself.

        Parameters:
        ----------
        X: Any
            The input data to be converted to a pandas DataFrame.

        Returns:
        -------
        ToDataFrame:
            The same object that is passed to the method.
        """
        return self

    def transform(self, X):
        """
        Converts the input data to a pandas DataFrame.

        Parameters:
        ----------
        X: Any
            The input data to be converted to a pandas DataFrame.

        Returns:
        -------
        pandas DataFrame:
            The input data as a pandas DataFrame.
        """
        return DataFrame(X)


class ToNumpyArray(BaseEstimator, TransformerMixin):
    """
    A custom transformer that converts the input pandas DataFrame to a numpy array.

    Methods:
    -------
    fit(X, y=None):
        This method does not perform any action and only returns the object itself.

    transform(X):
        Converts the input pandas DataFrame to a numpy array.

        Parameters:
        ----------
        X: pandas DataFrame
            The input DataFrame to be converted to a numpy array.

        Returns:
        -------
        numpy.ndarray:
            The input data as a numpy array.
    """

    def __init__(self) -> None:
        """
        Initializes an instance of ToNumpyArray class.
        """
        super().__init__()

    def fit(self, X, y=None):
        """
        This method does not perform any action and only returns the object itself.

        Parameters:
        ----------
        X: pandas DataFrame
            The input DataFrame to be converted to a numpy array.

        Returns:
        -------
        ToNumpyArray:
            The same object that is passed to the method.
        """
        return self

    def transform(self, X: DataFrame) -> np.ndarray:
        """
        Converts the input pandas DataFrame to a numpy array.

        Parameters:
        ----------
        X: pandas DataFrame
            The input DataFrame to be converted to a numpy array.

        Returns:
        -------
        numpy.ndarray:
            The input data as a numpy array.
        """
        return X.to_numpy()


class FrameMergeUnion(FeatureUnion):
    """
    Custom implementation of scikit-learn's FeatureUnion,
    which performs a union of data frames on the specified merge_on columns.

    Parameters
    ----------
    merge_on : str or list of str
        Column(s) to merge data frames on.
    transformer_list : list of (str, transformers) tuples
        List of transformer objects to be applied to the data.
    n_jobs : int or None, default None
        Number of jobs to run in parallel.
    transformer_weights : dict, optional
        Multiplicative weights for features per transformer.
    verbose : int, optional
        Controls the verbosity of the process.

    """

    def __init__(
        self,
        merge_on,
        transformer_list,
        *,
        n_jobs=None,
        transformer_weights=None,
        verbose=False,
        **merge_args,
    ):
        super().__init__(
            transformer_list,
            n_jobs=n_jobs,
            transformer_weights=transformer_weights,
            verbose=verbose,
        )
        self.merge_on = merge_on
        self.extra_args = merge_args

    def _hstack(self, Xs: List[DataFrame]):
        """
        Overwrite the _hstack operator to be a merge operation on dataframes instead of
        a concat.

        Parameters
        ----------
        Xs : list of pandas.DataFrame
            List of dataframes to be merged.

        Returns
        -------
        merged_df : pandas.DataFrame
            The resulting merged dataframe.
        """
        assert (
            (isinstance(Xs, List))
            and (len(Xs) > 0)
            and (all([isinstance(x, DataFrame) for x in Xs]))
        ), "the FrameMergeUnion Transformer only operates on List[DataFrame] objects"

        merged_df = None
        for df in Xs:
            if merged_df is None:
                merged_df = df
            else:
                merged_df = merged_df.merge(df, on=self.merge_on, **self.extra_args)

        return merged_df
