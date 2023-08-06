from albert.api.paths.api_v3_reports_id.get import ApiForget
from albert.api.paths.api_v3_reports_id.put import ApiForput
from albert.api.paths.api_v3_reports_id.delete import ApiFordelete


class ApiV3ReportsId(
    ApiForget,
    ApiForput,
    ApiFordelete,
):
    pass
