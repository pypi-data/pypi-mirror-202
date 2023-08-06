from albert.api.paths.api_v3_predictions_models_parent_id_version.get import ApiForget
from albert.api.paths.api_v3_predictions_models_parent_id_version.delete import ApiFordelete
from albert.api.paths.api_v3_predictions_models_parent_id_version.patch import ApiForpatch


class ApiV3PredictionsModelsParentIdVersion(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
