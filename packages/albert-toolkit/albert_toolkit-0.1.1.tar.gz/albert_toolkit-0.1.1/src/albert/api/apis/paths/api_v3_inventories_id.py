from albert.api.paths.api_v3_inventories_id.get import ApiForget
from albert.api.paths.api_v3_inventories_id.delete import ApiFordelete
from albert.api.paths.api_v3_inventories_id.patch import ApiForpatch


class ApiV3InventoriesId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
