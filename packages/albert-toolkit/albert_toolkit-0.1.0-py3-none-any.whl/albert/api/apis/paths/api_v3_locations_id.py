from albert.api.paths.api_v3_locations_id.get import ApiForget
from albert.api.paths.api_v3_locations_id.delete import ApiFordelete
from albert.api.paths.api_v3_locations_id.patch import ApiForpatch


class ApiV3LocationsId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
