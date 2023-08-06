from albert.api.paths.api_v3_reports_type.get import ApiForget
from albert.api.paths.api_v3_reports_type.post import ApiForpost
from albert.api.paths.api_v3_reports_type.patch import ApiForpatch


class ApiV3ReportsType(
    ApiForget,
    ApiForpost,
    ApiForpatch,
):
    pass
