from typing import Any

import numpy as np
from pydantic import BaseModel, Field
from tqdm.auto import tqdm

from albert.api import ApiClient
from albert.api.api_client import ApiResponse
from albert.api.apis.tags import analytics_api, reports_catalogue_api
from albert.internal.utils import convert_dynamic_schema_to_python_types

__all__ = [
    "ReportBase",
    "ReportRET27",
    "ReportRET28",
    "ReportRET30",
    "ReportRET31",
    "ReportRET32",
    "ReportRET33",
    "ReportRET38",
]


class ReportBase(BaseModel):
    report_type_id: str = Field(alias="reportTypeId")
    report_type: str = Field(alias="reportType")
    category: str = ""
    description: str = ""  # Optional Description
    client: ApiClient = None

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, **data: Any) -> None:
        # Before we deserialize into the model -- there are some fields
        # that need to be type cast
        for k in data.keys():
            if "DynamicSchema" in str(type(data[k])):
                data[k] = str(data[k])
        super().__init__(**data)

    def get(self, **params):
        raise NotImplementedError(
            "The get parameter needs to be implemented for this Report class"
        )

    def parse_api_response(self, response: ApiResponse):
        pass

    def _set_client(self, client: ApiClient = None) -> None:
        """
        Sets the internal client reference so that users can call .get or other report
        fetching functions without having to explicitly pass in the client.
        """
        if client:
            self.client = client
        else:
            self.client = None

    def __repr__(self) -> str:
        return f"Report <Id:{self.report_type_id}, Name:{self.report_type}, Cat:{self.category}, Desc:{self.description}, HasClient:{self.client is not None}>"


class _DACDATLimitReport(ReportBase):
    """
    Concrete Report Class Implementation for RET27 and RET30
    Retrieves and parses out the report
    """

    dataColumnId: str = ""
    dataTemplateId: str = ""

    def get(self, dataColumnId, dataTemplateId, batch_size=6000, limit=None):
        self.dataColumnId = dataColumnId
        self.dataTemplateId = dataTemplateId

        if self.dataColumnId == "" or self.dataTemplateId == "":
            raise ValueError(
                "both a data column id and a data template id are required to run this report"
            )

        start = 0
        size = min(batch_size, limit) if limit is not None else batch_size
        all_items = []
        with tqdm(desc=f"Pulling Report {self.report_type_id}", unit="rows") as pb:
            while True:
                api_instance = analytics_api.AnalyticsApi(self.client)

                path_params = {"id": self.report_type_id}

                query_params = {
                    "inputData": {
                        "inputData[dataColumnsId]": self.dataColumnId,
                        "inputData[dataTemplatesId]": self.dataTemplateId,
                        "inputData[skip]": start,
                        "inputData[limit]": size,
                    }
                }

                api_response = api_instance.get_report_type_datascience(
                    query_params=query_params, path_params=path_params
                )

                zz = api_response.body
                items = list(list(zz["Items"])[0])
                all_items.extend(items)
                pb.update(len(items))
                start += len(items)

                if (len(items) < size) or (limit is not None and len(items) >= limit):
                    # We were returned fewer items than requested
                    # so there is no additional data to pull
                    break
                elif limit is not None and (len(items) + size) >= limit:
                    # make the next batch precisely the number needed to hit the limit
                    size = limit - len(items)

        return list(
            map(
                lambda x: convert_dynamic_schema_to_python_types(dict(x)),
                tqdm(all_items, desc="Processing"),
            )
        )

    def __repr__(self) -> str:
        return f"{self.report_type_id} <Name:{self.report_type}, Cat:{self.category}, Desc:{self.description}, HasClient:{self.client is not None}\n\t\t DAC:{self.dataColumnId}, DAT:{self.dataTemplateId}>"


class ReportRET27(_DACDATLimitReport):
    pass


# Alias for Formulation Raw Data
FormulationRawDataReport = ReportRET27


class ReportRET30(_DACDATLimitReport):
    pass


# Alias for RET30
PropertyRawDataReport = ReportRET30


class ReportRET31(_DACDATLimitReport):
    pass


# Alias for RET31
OperatingConditionRawDataReport = ReportRET31


class ReportRET32(_DACDATLimitReport):
    pass


# Alias for RET32
OperatingConditionRawUnitCountReport = ReportRET32


class ReportRET33(_DACDATLimitReport):
    pass


class ReportRET38(_DACDATLimitReport):
    pass


class ReportRET28(ReportBase):
    formulas: list[str] = []

    def get(self, formulas):
        if isinstance(formulas, list):
            self.formulas = formulas
        else:
            self.formulas = [formulas]

        if len(formulas) < 1:
            raise ValueError("you must specify at least one formula to unpack")

        self.formulas = list(set(self.formulas))

        formulaIdx = 0
        all_items = []
        with tqdm(
            desc=f"Pulling Report {self.report_type_id}",
            unit="rows",
            total=len(self.formulas),
        ) as pb:
            while formulaIdx < len(self.formulas):
                api_instance = analytics_api.AnalyticsApi(self.client)

                path_params = {"id": self.report_type_id}

                query_params = {
                    "inputData": {
                        "inputData[formulas]": self.formulas[formulaIdx]
                        # "inputData[formulas]": v
                        # for v in self.formulas[start : start + size]
                    }
                }

                api_response = api_instance.get_report_type_datascience(
                    query_params=query_params, path_params=path_params
                )

                zz = api_response.body
                items = list(list(zz["Items"])[0])
                all_items.extend(items)
                pb.update(1)
                formulaIdx += 1

        return list(
            map(
                lambda x: convert_dynamic_schema_to_python_types(dict(x)),
                tqdm(items, desc="Processing"),
            )
        )

    def __repr__(self) -> str:
        return f"{self.report_type_id} <Name:{self.report_type}, Cat:{self.category}, Desc:{self.description}, HasClient:{self.client is not None}>"
