import typing_extensions

from albert.api.paths import PathValues
from albert.api.apis.paths.api_v3_predictions_health import ApiV3PredictionsHealth
from albert.api.apis.paths.api_v3_predictions import ApiV3Predictions
from albert.api.apis.paths.api_v3_predictions_parent_id import ApiV3PredictionsParentId
from albert.api.apis.paths.api_v3_predictions_mergedat import ApiV3PredictionsMergedat
from albert.api.apis.paths.api_v3_predictions_mergedac import ApiV3PredictionsMergedac
from albert.api.apis.paths.api_v3_predictions_models_id import ApiV3PredictionsModelsId
from albert.api.apis.paths.api_v3_predictions_models_parent_id_version_id import ApiV3PredictionsModelsParentIdVersionId
from albert.api.apis.paths.api_v3_predictions_models_parent_id_version import ApiV3PredictionsModelsParentIdVersion
from albert.api.apis.paths.api_v3_predictions_models import ApiV3PredictionsModels
from albert.api.apis.paths.api_v3_predictions_tasks import ApiV3PredictionsTasks
from albert.api.apis.paths.api_v3_locations_health import ApiV3LocationsHealth
from albert.api.apis.paths.api_v3_locations import ApiV3Locations
from albert.api.apis.paths.api_v3_locations_id import ApiV3LocationsId
from albert.api.apis.paths.api_v3_locations_async_id import ApiV3LocationsAsyncId
from albert.api.apis.paths.api_v3_productdesign_health import ApiV3ProductdesignHealth
from albert.api.apis.paths.api_v3_productdesign import ApiV3Productdesign
from albert.api.apis.paths.api_v3_productdesign_search import ApiV3ProductdesignSearch
from albert.api.apis.paths.api_v3_productdesign_suggest import ApiV3ProductdesignSuggest
from albert.api.apis.paths.api_v3_productdesign_id import ApiV3ProductdesignId
from albert.api.apis.paths.api_v3_productdesign_id_designs import ApiV3ProductdesignIdDesigns
from albert.api.apis.paths.api_v3_productdesign_id_products import ApiV3ProductdesignIdProducts
from albert.api.apis.paths.api_v3_productdesign_id_values import ApiV3ProductdesignIdValues
from albert.api.apis.paths.api_v3_productdesign_id_grid import ApiV3ProductdesignIdGrid
from albert.api.apis.paths.api_v3_productdesign_id_unpack import ApiV3ProductdesignIdUnpack
from albert.api.apis.paths.api_v3_productdesign_inventories_id import ApiV3ProductdesignInventoriesId
from albert.api.apis.paths.api_v3_productdesign_mergeinventory import ApiV3ProductdesignMergeinventory
from albert.api.apis.paths.api_v3_inventories_health import ApiV3InventoriesHealth
from albert.api.apis.paths.api_v3_inventories import ApiV3Inventories
from albert.api.apis.paths.api_v3_inventories_id import ApiV3InventoriesId
from albert.api.apis.paths.api_v3_reports_health import ApiV3ReportsHealth
from albert.api.apis.paths.api_v3_reports_search import ApiV3ReportsSearch
from albert.api.apis.paths.api_v3_reports_suggest import ApiV3ReportsSuggest
from albert.api.apis.paths.api_v3_reports_inventory_equipment_usage import ApiV3ReportsInventoryEquipmentUsage
from albert.api.apis.paths.api_v3_reports_inventory_movements import ApiV3ReportsInventoryMovements
from albert.api.apis.paths.api_v3_reports_type import ApiV3ReportsType
from albert.api.apis.paths.api_v3_reports_analytics_id import ApiV3ReportsAnalyticsId
from albert.api.apis.paths.api_v3_reports_datascience_id import ApiV3ReportsDatascienceId
from albert.api.apis.paths.api_v3_reports_type_id import ApiV3ReportsTypeId
from albert.api.apis.paths.api_v3_reports import ApiV3Reports
from albert.api.apis.paths.api_v3_reports_copy import ApiV3ReportsCopy
from albert.api.apis.paths.api_v3_reports_id import ApiV3ReportsId

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.API_V3_PREDICTIONS_HEALTH: ApiV3PredictionsHealth,
        PathValues.API_V3_PREDICTIONS: ApiV3Predictions,
        PathValues.API_V3_PREDICTIONS_PARENT_ID: ApiV3PredictionsParentId,
        PathValues.API_V3_PREDICTIONS_MERGEDAT: ApiV3PredictionsMergedat,
        PathValues.API_V3_PREDICTIONS_MERGEDAC: ApiV3PredictionsMergedac,
        PathValues.API_V3_PREDICTIONS_MODELS_ID: ApiV3PredictionsModelsId,
        PathValues.API_V3_PREDICTIONS_MODELS_PARENT_ID_VERSION_ID: ApiV3PredictionsModelsParentIdVersionId,
        PathValues.API_V3_PREDICTIONS_MODELS_PARENT_ID_VERSION: ApiV3PredictionsModelsParentIdVersion,
        PathValues.API_V3_PREDICTIONS_MODELS: ApiV3PredictionsModels,
        PathValues.API_V3_PREDICTIONS_TASKS: ApiV3PredictionsTasks,
        PathValues.API_V3_LOCATIONS_HEALTH: ApiV3LocationsHealth,
        PathValues.API_V3_LOCATIONS: ApiV3Locations,
        PathValues.API_V3_LOCATIONS_ID: ApiV3LocationsId,
        PathValues.API_V3_LOCATIONS_ASYNC_ID: ApiV3LocationsAsyncId,
        PathValues.API_V3_PRODUCTDESIGN_HEALTH: ApiV3ProductdesignHealth,
        PathValues.API_V3_PRODUCTDESIGN: ApiV3Productdesign,
        PathValues.API_V3_PRODUCTDESIGN_SEARCH: ApiV3ProductdesignSearch,
        PathValues.API_V3_PRODUCTDESIGN_SUGGEST: ApiV3ProductdesignSuggest,
        PathValues.API_V3_PRODUCTDESIGN_ID: ApiV3ProductdesignId,
        PathValues.API_V3_PRODUCTDESIGN_ID_DESIGNS: ApiV3ProductdesignIdDesigns,
        PathValues.API_V3_PRODUCTDESIGN_ID_PRODUCTS: ApiV3ProductdesignIdProducts,
        PathValues.API_V3_PRODUCTDESIGN_ID_VALUES: ApiV3ProductdesignIdValues,
        PathValues.API_V3_PRODUCTDESIGN_ID_GRID: ApiV3ProductdesignIdGrid,
        PathValues.API_V3_PRODUCTDESIGN_ID_UNPACK: ApiV3ProductdesignIdUnpack,
        PathValues.API_V3_PRODUCTDESIGN_INVENTORIES_ID: ApiV3ProductdesignInventoriesId,
        PathValues.API_V3_PRODUCTDESIGN_MERGEINVENTORY: ApiV3ProductdesignMergeinventory,
        PathValues.API_V3_INVENTORIES_HEALTH: ApiV3InventoriesHealth,
        PathValues.API_V3_INVENTORIES: ApiV3Inventories,
        PathValues.API_V3_INVENTORIES_ID: ApiV3InventoriesId,
        PathValues.API_V3_REPORTS_HEALTH: ApiV3ReportsHealth,
        PathValues.API_V3_REPORTS_SEARCH: ApiV3ReportsSearch,
        PathValues.API_V3_REPORTS_SUGGEST: ApiV3ReportsSuggest,
        PathValues.API_V3_REPORTS_INVENTORY_EQUIPMENT_USAGE: ApiV3ReportsInventoryEquipmentUsage,
        PathValues.API_V3_REPORTS_INVENTORY_MOVEMENTS: ApiV3ReportsInventoryMovements,
        PathValues.API_V3_REPORTS_TYPE: ApiV3ReportsType,
        PathValues.API_V3_REPORTS_ANALYTICS_ID: ApiV3ReportsAnalyticsId,
        PathValues.API_V3_REPORTS_DATASCIENCE_ID: ApiV3ReportsDatascienceId,
        PathValues.API_V3_REPORTS_TYPE_ID: ApiV3ReportsTypeId,
        PathValues.API_V3_REPORTS: ApiV3Reports,
        PathValues.API_V3_REPORTS_COPY: ApiV3ReportsCopy,
        PathValues.API_V3_REPORTS_ID: ApiV3ReportsId,
    }
)

path_to_api = PathToApi(
    {
        PathValues.API_V3_PREDICTIONS_HEALTH: ApiV3PredictionsHealth,
        PathValues.API_V3_PREDICTIONS: ApiV3Predictions,
        PathValues.API_V3_PREDICTIONS_PARENT_ID: ApiV3PredictionsParentId,
        PathValues.API_V3_PREDICTIONS_MERGEDAT: ApiV3PredictionsMergedat,
        PathValues.API_V3_PREDICTIONS_MERGEDAC: ApiV3PredictionsMergedac,
        PathValues.API_V3_PREDICTIONS_MODELS_ID: ApiV3PredictionsModelsId,
        PathValues.API_V3_PREDICTIONS_MODELS_PARENT_ID_VERSION_ID: ApiV3PredictionsModelsParentIdVersionId,
        PathValues.API_V3_PREDICTIONS_MODELS_PARENT_ID_VERSION: ApiV3PredictionsModelsParentIdVersion,
        PathValues.API_V3_PREDICTIONS_MODELS: ApiV3PredictionsModels,
        PathValues.API_V3_PREDICTIONS_TASKS: ApiV3PredictionsTasks,
        PathValues.API_V3_LOCATIONS_HEALTH: ApiV3LocationsHealth,
        PathValues.API_V3_LOCATIONS: ApiV3Locations,
        PathValues.API_V3_LOCATIONS_ID: ApiV3LocationsId,
        PathValues.API_V3_LOCATIONS_ASYNC_ID: ApiV3LocationsAsyncId,
        PathValues.API_V3_PRODUCTDESIGN_HEALTH: ApiV3ProductdesignHealth,
        PathValues.API_V3_PRODUCTDESIGN: ApiV3Productdesign,
        PathValues.API_V3_PRODUCTDESIGN_SEARCH: ApiV3ProductdesignSearch,
        PathValues.API_V3_PRODUCTDESIGN_SUGGEST: ApiV3ProductdesignSuggest,
        PathValues.API_V3_PRODUCTDESIGN_ID: ApiV3ProductdesignId,
        PathValues.API_V3_PRODUCTDESIGN_ID_DESIGNS: ApiV3ProductdesignIdDesigns,
        PathValues.API_V3_PRODUCTDESIGN_ID_PRODUCTS: ApiV3ProductdesignIdProducts,
        PathValues.API_V3_PRODUCTDESIGN_ID_VALUES: ApiV3ProductdesignIdValues,
        PathValues.API_V3_PRODUCTDESIGN_ID_GRID: ApiV3ProductdesignIdGrid,
        PathValues.API_V3_PRODUCTDESIGN_ID_UNPACK: ApiV3ProductdesignIdUnpack,
        PathValues.API_V3_PRODUCTDESIGN_INVENTORIES_ID: ApiV3ProductdesignInventoriesId,
        PathValues.API_V3_PRODUCTDESIGN_MERGEINVENTORY: ApiV3ProductdesignMergeinventory,
        PathValues.API_V3_INVENTORIES_HEALTH: ApiV3InventoriesHealth,
        PathValues.API_V3_INVENTORIES: ApiV3Inventories,
        PathValues.API_V3_INVENTORIES_ID: ApiV3InventoriesId,
        PathValues.API_V3_REPORTS_HEALTH: ApiV3ReportsHealth,
        PathValues.API_V3_REPORTS_SEARCH: ApiV3ReportsSearch,
        PathValues.API_V3_REPORTS_SUGGEST: ApiV3ReportsSuggest,
        PathValues.API_V3_REPORTS_INVENTORY_EQUIPMENT_USAGE: ApiV3ReportsInventoryEquipmentUsage,
        PathValues.API_V3_REPORTS_INVENTORY_MOVEMENTS: ApiV3ReportsInventoryMovements,
        PathValues.API_V3_REPORTS_TYPE: ApiV3ReportsType,
        PathValues.API_V3_REPORTS_ANALYTICS_ID: ApiV3ReportsAnalyticsId,
        PathValues.API_V3_REPORTS_DATASCIENCE_ID: ApiV3ReportsDatascienceId,
        PathValues.API_V3_REPORTS_TYPE_ID: ApiV3ReportsTypeId,
        PathValues.API_V3_REPORTS: ApiV3Reports,
        PathValues.API_V3_REPORTS_COPY: ApiV3ReportsCopy,
        PathValues.API_V3_REPORTS_ID: ApiV3ReportsId,
    }
)
