import inspect
from typing import Any, Dict

from pandas import DataFrame
from sklearn.base import BaseEstimator, TransformerMixin

import albert.data.reports
from albert.api.apis.tags import reports_catalogue_api
from albert.pipeline import AlbertConfigurableBaseEstimator, PipelineConfig
from albert.session import AlbertSession


class ReportGather(AlbertConfigurableBaseEstimator, TransformerMixin):
    def __init__(
        self,
        report_id: str,
        report_parameters: Dict[str, Any],
        return_type: str = "json",
    ) -> None:
        self.report_id = report_id
        self.report_parameters = report_parameters

        if return_type.lower() not in ["json", "dataframe", "df"]:
            raise ValueError(f"unknown return type requested {return_type}")

        self.return_type = return_type.lower()

    def fit(self, X, y=None):
        return self

    def transform(self, X: PipelineConfig | None):
        if X is None:
            X = self.config

        # this will raise a key error if the api_client isn't set
        session: AlbertSession = X.get_param("session")

        # This will raise an API Exception if the report cannot be found
        resp = reports_catalogue_api.GetReportTypeById(
            session.client
        ).get_report_type_by_id(path_params={"id": self.report_id.upper()})

        report_cls_name = f"Report{self.report_id.upper()}"

        fns = list(
            filter(
                lambda x: x[0] == report_cls_name,
                inspect.getmembers(albert.data.reports),
            )
        )

        if len(fns) > 0:
            params = dict(resp.body)
            if "category" not in params:
                params["category"] = "unknown"

            report_obj: albert.data.reports.ReportBase = fns[0][1](**params)
        else:
            raise NotImplementedError(
                f"cannot find implementation to retrieve the requested report type {self.report_id}"
                "-- please contact albert support to implement this feature"
            )

        # Reports that implement the get method usually return a list of JSON records
        report_obj.client = session.client
        res = report_obj.get(**self.report_parameters)

        if self.return_type == "json":
            return res
        elif self.return_type in ["dataframe", "df"]:
            return DataFrame(res)
