from typing import Any, overload, Sequence
from ..data.reports import ReportBase
from .base import BaseFilter, FilterParameter
import re

__all__ = ["ReportFilter"]


class ReportFilter(BaseFilter):
    id: FilterParameter[str] | str | None = None
    name: FilterParameter[str] | str | None = None
    category: FilterParameter[str] | str | None = None
    desc: FilterParameter[str] | str | None = None
    any: FilterParameter[str] | str | None = None

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)

    @overload
    def filter(self, input_: ReportBase) -> bool:
        ...

    @overload
    def filter(self, input_: Sequence[ReportBase]) -> list[bool]:
        ...

    def filter(self, input_: ReportBase | Sequence[ReportBase]) -> bool | list[bool]:
        if isinstance(input_, Sequence):
            return list(map(lambda x: self.__filter_report(x), input_))
        else:
            return self.__filter_report(input_)

    def __filter_report(self, r: ReportBase) -> bool:  # noqa: C901
        flags: list[bool] = []

        def search_field(search_for: str, field: str) -> None:
            if re.search(search_for, field, re.IGNORECASE) is not None:
                flags.append(True)
            else:
                flags.append(False)

        # disallow the use of any and other field search values
        if self.any is not None and (
            (self.id is not None) or (self.name is not None) or (self.desc is not None)
        ):
            raise ValueError(
                "must specify either 'any' to search all fields, or only those specific fields you want to search"
            )

        def get_val(vv: FilterParameter[str] | str) -> str:
            if isinstance(vv, FilterParameter):
                sval = vv.get_parameter()
                if sval is not None:
                    return sval
                else:
                    return ""
            else:
                return vv

        if self.any is not None:
            sval = get_val(self.any)
            search_field(sval, r.report_type_id)
            search_field(sval, r.report_type)
            search_field(sval, r.description)
            search_field(sval, r.category)
            # If any of the fields matched the search string return true
            return any(flags)

        if self.id is not None:
            search_field(get_val(self.id), r.report_type_id)
        if self.name is not None:
            search_field(get_val(self.name), r.report_type)
        if self.desc is not None:
            search_field(get_val(self.desc), r.description)
        if self.category is not None:
            search_field(get_val(self.category), r.category)

        # Return true only if all the conditions that were specified were matched
        return all(flags)
