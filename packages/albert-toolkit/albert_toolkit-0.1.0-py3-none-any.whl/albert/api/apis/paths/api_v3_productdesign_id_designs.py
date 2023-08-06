from albert.api.paths.api_v3_productdesign_id_designs.get import ApiForget
from albert.api.paths.api_v3_productdesign_id_designs.post import ApiForpost
from albert.api.paths.api_v3_productdesign_id_designs.delete import ApiFordelete
from albert.api.paths.api_v3_productdesign_id_designs.patch import ApiForpatch


class ApiV3ProductdesignIdDesigns(
    ApiForget,
    ApiForpost,
    ApiFordelete,
    ApiForpatch,
):
    pass
