from typing import Any, Dict, List, Callable

import numpy as np
from pandas import DataFrame
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import FeatureUnion
from sklearn.utils.validation import check_array, check_is_fitted, check_X_y


class StageLoader(BaseEstimator, TransformerMixin):
    """
    A custom transformer that loads a pre-processed object and returns it without making any changes.

    Parameters:
    ----------
    object: Any
        An object of any type that has been pre-processed

    Methods:
    -------
    fit(X, y=None):
        This method does not perform any action and only returns the object itself.

    transform(X: Any) -> Any:
        Return the object instance variable that was passed in the constructor.
    """

    def __init__(self, object: Any):
        """
        Initializes an instance of StageLoader class.

        Parameters:
        ----------
        object: Any
            An object of any type that has been pre-processed
        """
        self.object = object

    def fit(self, X, y=None):
        """
        This method does not perform any action and only returns the object itself.
        """
        return self

    def transform(self, X: Any) -> Any:
        """
        Return the object instance variable that was passed in the constructor.

        Parameters:
        ----------
        X: Any
            An input data that is ignored.

        Returns:
        -------
        Any:
            The object instance variable that was passed in the constructor.
        """
        return self.object


class DictUnionResults(FeatureUnion):
    """
    A custom transformer that stacks the outputs of other transformers into a dictionary.

    Parameters:
    ----------
    transformer_output_names: list of str
        The names of each transformer's output

    transformer_list: list of transformer objects
        The list of transformer objects to stack

    n_jobs: int or None, default=None
        The number of jobs to run in parallel. None means 1.

    transformer_weights: dict, optional
        Multiplicative weights for features per transformer.

    verbose: bool, optional
        If True, it will print progress updates.

    Methods:
    -------
    _hstack(Xs: List[Any]) -> Dict[str, Any]:
        Helper method that stacks the outputs of transformers horizontally into a dictionary.
    """

    def __init__(
        self,
        transformer_output_names: list,
        transformer_list: list,
        *,
        n_jobs: int = None,
        transformer_weights: dict = None,
        verbose: bool = False,
    ):
        """
        Initializes an instance of DictUnionResults class.

        Parameters:
        ----------
        transformer_output_names: list of str
            The names of each transformer's output

        transformer_list: list of transformer objects
            The list of transformer objects to stack

        n_jobs: int or None, default=None
            The number of jobs to run in parallel. None means 1.

        transformer_weights: dict, optional
            Multiplicative weights for features per transformer.

        verbose: bool, optional
            If True, it will print progress updates.
        """
        super().__init__(
            transformer_list,
            n_jobs=n_jobs,
            transformer_weights=transformer_weights,
            verbose=verbose,
        )

        self.transformer_output_names = transformer_output_names

    def _hstack(self, Xs: List[Any]) -> Dict[str, Any]:
        """
        Helper method that stacks the outputs of transformers horizontally into a dictionary.

        Parameters:
        ----------
        Xs: List of Any
            The output of each transformer.

        Returns:
        -------
        Dict[str, Any]:
            A dictionary of stacked outputs, where each key is a transformer's name and the corresponding value is its output.
        """
        assert isinstance(
            Xs, List
        ), "The DictUnionResult Transformer only operates on lists of objects"

        assert (len(Xs) > 0) and len(Xs) == len(self.transformer_output_names), (
            "The Length of the input list must match the length of the output "
            "names given to the DictUnion"
        )

        output_dict = {}

        for i, name in enumerate(self.transformer_output_names):
            output_dict[name] = Xs[i]

        return output_dict


class DictApply(BaseEstimator, TransformerMixin):
    def __init__(
        self,
        func_to_apply: Callable[[Dict[str, Any]], Any]
        | Dict[str, Callable[[Any], Any]],
    ) -> None:
        """
        Initializes the `DictApply` class instance with a callable object, either a function that
        takes a dictionary object as input or a dictionary of functions that take any object as
        input and return any object paired with the name of the object in the input dictionary
        that the function should be applied to.

        Parameters:
        ----------
        func_to_apply: Callable[[Dict[str, Any]], Any] or Dict[str, Callable[[Any], Any]]
            A callable object, either a function or a dictionary of functions.

        Returns:
        ----------
        None
        """
        super().__init__()
        self.apply_fn = func_to_apply

    def fit(self, X: Any, y: Any | None = None):
        """
        Fits the `DictApply` transformer to the input data.

        Parameters:
        ----------
        X: Any
            Input data. Not used in this method.
        y: Any or None, default=None
            Target data. Not used in this method.

        Returns:
        ----------
        self: DictApply
            The fitted `DictApply` transformer instance.
        """
        return self

    def transform(self, X: Dict[str, Any]) -> Dict[str, Any] | Any:
        """
        Applies the function(s) provided at initialization to the input dictionary `X`
        and returns the transformed dictionary or whatever the result of applying
        the function to the entire dictionary is.

        Parameters:
        ----------
        X: Dict[str, Any]
            Input dictionary object to be transformed.

        Returns:
        ----------
        out_dict: Dict[str, Any] or Any
            Transformed dictionary object.
        """
        if self.apply_fn is None:
            raise ValueError("the apply function is None -- nothing to do")

        if isinstance(self.apply_fn, dict):
            out_dict = {}
            for k, v in self.apply_fn.items():
                if not isinstance(v, Callable):
                    raise TypeError(f"the function for key {k} is not callable")
                elif k not in X:
                    raise KeyError(
                        f"did not find object with key {k} in the input dictionary"
                    )

                out_dict[k] = self.apply_fn[k](X[k])

            return out_dict
        else:
            return self.apply_fn(X)
