from typing import Any, overload, Sequence, Generic, TypeVar, Dict
from pydantic import BaseModel

__all__ = ["BaseFilter"]

C = TypeVar("C")


class ExactMatchWrapper(Generic[C]):
    def __init__(self, val: C) -> None:
        self.value: C = val

    def get_exact_value(self) -> C:
        return self.value


# Our desired interface would be something like this for a Filter
# PredictionFilter(dataColumnName=exact())


class FilterParameter(Generic[C], BaseModel):
    is_exact: bool = False
    param_value: C | None = None

    def __init__(self, value: C | ExactMatchWrapper[C] | None = None) -> None:
        super().__init__()
        # If the user has specified an exact match we will wrap the parameter so that
        # any query generators have the ability to know whether to do an exact match
        # or a similar to match

        if value is not None:
            if isinstance(value, ExactMatchWrapper):
                self.is_exact = True
                self.param_value = value.get_exact_value()
            else:
                self.param_value = value

    def get_parameter(self) -> C | None:
        if self.param_value is not None:
            return self.param_value

        return None

    def is_exact_parameter(self) -> bool:
        return self.is_exact


class FilterParameterChoices(Generic[C], BaseModel):
    parameters: list[FilterParameter[C]] | None = None


def exact(value: Any) -> FilterParameter[Any]:
    return FilterParameter(ExactMatchWrapper(value))


def approx(value: Any):
    return FilterParameter(value)


def _flexible_initializer(**data: Any) -> Dict[str, Any]:
    for k, v in data.items():
        if isinstance(v, str):
            data[k] = approx(v)
    return data


class BaseFilter(BaseModel):
    def __init__(self, **data: Any) -> None:
        super().__init__(**_flexible_initializer(**data))

    def filter(self, input_: Any) -> list[bool]:
        raise NotImplementedError(
            "the filter method for the used filter has not been implemented"
        )
