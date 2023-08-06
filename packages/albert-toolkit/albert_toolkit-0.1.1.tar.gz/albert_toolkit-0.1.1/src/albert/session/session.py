import inspect
from itertools import compress
from typing import Any, Dict, List

from libjwtpython.token_auth import decodeJWT, signJWT
import dotenv
import os
import albert.api
import albert.data.reports
from albert.api import ApiException
from albert.api.apis.tags import analytics_api, default_api, reports_catalogue_api
from albert.data.reports import ReportBase
from albert.data.warehouse.dbsession import AlbertWarehouseInterface
from albert.data.warehouse.queries import WarehouseQueries

from albert.internal.utils.utils import get_albert_parameter
from ..filters.report_filters import ReportFilter
from ..version import __version__
from .token_manager import TokenManager


class AlbertSession(TokenManager, WarehouseQueries):
    """
    Albert Invent API Wrapper -- Extends Token Manager to handle JWT
    """

    default_host = "https://app.albertinvent.com"
    default_dev_host = "https://dev.albertinventdev.com"
    default_dot_env_file = os.path.join(os.path.expanduser("~"), ".albert/config")

    # client = __version__

    def __init__(
        self,
        endpoint: str = default_host,
        token=None,  # JWT Token
        threads=5,
        db_user=None,
        db_password=None,
        db_host=None,
        db_port=53535,
        db_database=None,
        dot_env_file=default_dot_env_file,
        **kwargs,
    ) -> None:
        # Load the dotenv file first
        # We will always try to load the default
        # albert config file if it exists otherwise
        # load the file the user specified
        if dot_env_file == self.default_dot_env_file:
            if os.path.exists(dot_env_file):
                print(
                    "Found Albert Configuration -- Environment will be configured automatically"
                )
                if not dotenv.load_dotenv(dot_env_file, override=True):
                    raise ValueError(
                        "improperly formatted albert config file -- please run `albert init`"
                        " to set the correct config parameters"
                    )
        elif not dotenv.load_dotenv(dot_env_file, override=True):
            raise FileExistsError(f"dot env file not valid [{dot_env_file}]")

        if endpoint == self.default_dev_host:
            token_env = "ALBERT_TOKEN_DEV"
        else:
            token_env = "ALBERT_TOKEN"

        super().__init__(get_albert_parameter(token, token_env), **kwargs)
        super(WarehouseQueries, self).__init__(
            get_albert_parameter(db_user, "DB_USER"),
            get_albert_parameter(db_password, "DB_PASSWORD"),
            get_albert_parameter(db_host, "DB_HOST"),
            int(get_albert_parameter(db_port, "DB_PORT")),
            get_albert_parameter(db_database, "DB_DATABASE"),
        )
        self.host: str = endpoint
        self.config = albert.api.Configuration(host=self.host)
        self.threads = threads

        # TODO: If the user didn't specify a token we need to generate one using other means,
        # for the moment raise an error
        if not self.has_valid_token():
            raise NotImplementedError(
                "Currently you must supply a valid JWT Token as part of the init call"
            )

        # Set the access token
        self.config.access_token = self._get_token()

        # Setup the API Client
        self.client = albert.api.ApiClient(self.config, pool_threads=threads)

    def __getstate__(self):
        return {
            "host": self.host,
            "config": self.config,
            "threads": self.threads,
            "token": self._get_token(),
        }

    def __setstate__(self, state_info):
        self.host = state_info["host"]
        self.config = state_info["config"]
        self.threads = state_info["threads"]
        self._set_token(state_info["token"])
        self.client = albert.api.ApiClient(self.config, pool_threads=self.threads)

    def get_report_obj(self, report_id):
        # Will raise an API exception if the report does not
        # exist -- we will simply bubble up the error if that happens
        resp = reports_catalogue_api.GetReportTypeById(
            self.client
        ).get_report_type_by_id(path_params={"id": report_id})

        if "reportTypeId" in resp.body:
            report_cls_name = f"Report{resp.body['reportTypeId']}"

            fns = list(
                filter(
                    lambda x: x[0] == report_cls_name,
                    inspect.getmembers(albert.data.reports),
                )
            )
            robj: ReportBase = None
            rdata = dict(resp.body)

            if len(fns) > 0:
                robj = fns[0][1](**rdata)
            else:
                robj = ReportBase(**rdata)

            robj.client = self.client
            return robj

        pass

    def available_reports(
        self, report_filter: ReportFilter | None = None
    ) -> List[ReportBase]:
        # List all the available reports through the reporting API
        resp = reports_catalogue_api.GetReportTypes(self.client).get_report_types()
        reports: List[ReportBase] = list(
            map(lambda x: ReportBase(**x), resp.body["Items"])
        )

        final_reports = []

        # For each report we want to try to determine if it is a known type in the reports
        #  module via refelction. if it is then we will create a report of that type
        # rather than the basic report base.
        for r in reports:
            # Set the client field in the report so that the user can call .get() if it
            # has been implemented for that report type
            r.client = self.client
            try:
                resp = reports_catalogue_api.GetReportTypeById(
                    self.client
                ).get_report_type_by_id(path_params={"id": r.report_type_id})

                report_cls_name = f"Report{r.report_type_id}"

                fns = list(
                    filter(
                        lambda x: x[0] == report_cls_name,
                        inspect.getmembers(albert.data.reports),
                    )
                )
                if len(fns) > 0:
                    final_reports.append(fns[0][1](**r.dict(by_alias=True)))
                else:
                    final_reports.append(r)

            except ApiException:
                print(f"Unable to get details of report {r.report_type_id}")
                final_reports.append(r)

        if report_filter is not None:
            return list(compress(final_reports, report_filter.filter(final_reports)))
        else:
            return final_reports
