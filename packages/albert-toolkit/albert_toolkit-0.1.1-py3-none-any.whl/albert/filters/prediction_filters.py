from typing import Any, overload, Sequence, List, Tuple
from .base import BaseFilter, FilterParameter, exact, approx, _flexible_initializer
import re


class PredictionFilter(BaseFilter):
    """
    This is a non-traditional filter object,
    it does not implement the filter method directly
    as it is used only when building queries for the
    model prediction table of the database warehouse
    """

    id: FilterParameter[str] | str | None = None
    taskId: FilterParameter[str] | str | None = None
    predictionType: FilterParameter[str] | str | None = None
    intervalId: FilterParameter[str] | str | None = None
    workflowId: FilterParameter[str] | str | None = None
    inventoryId: FilterParameter[str] | str | None = None
    dataColumnId: FilterParameter[str] | str | None = None
    dataColumnName: FilterParameter[str] | str | None = None
    modelId: FilterParameter[str] | str | None = None
    modelName: FilterParameter[str] | str | None = None
    variable: FilterParameter[str] | str | None = None

    def get_filter_params(self) -> List[Tuple[str, bool, Any]]:
        vals: List[Tuple[str, bool, Any]] = []
        for pname in vars(self):
            var = getattr(self, pname)
            if var is not None:
                if isinstance(var, FilterParameter):
                    vals.append((pname, var.is_exact, var.get_parameter()))

        return vals
