import typing_extensions

from albert.api.apis.tags import TagValues
from albert.api.apis.tags.prediction_flow_api import PredictionFlowApi
from albert.api.apis.tags.prediction_models_api import PredictionModelsApi
from albert.api.apis.tags.predictions_api import PredictionsApi
from albert.api.apis.tags.locations_api import LocationsApi
from albert.api.apis.tags.product_design_api import ProductDesignApi
from albert.api.apis.tags.rows_api import RowsApi
from albert.api.apis.tags.columns_api import ColumnsApi
from albert.api.apis.tags.values_api import ValuesApi
from albert.api.apis.tags.grid_api import GridApi
from albert.api.apis.tags.unpack_api import UnpackApi
from albert.api.apis.tags.health_check_api import HealthCheckApi
from albert.api.apis.tags.inventory_api import InventoryApi
from albert.api.apis.tags.reports_catalogue_api import ReportsCatalogueApi
from albert.api.apis.tags.analytics_api import AnalyticsApi
from albert.api.apis.tags.user_reports_api import UserReportsApi
from albert.api.apis.tags.search_api import SearchApi
from albert.api.apis.tags.internal_api import InternalApi
from albert.api.apis.tags.reports_sp_api import ReportsSPApi
from albert.api.apis.tags.default_api import DefaultApi

TagToApi = typing_extensions.TypedDict(
    'TagToApi',
    {
        TagValues.PREDICTION_FLOW: PredictionFlowApi,
        TagValues.PREDICTION_MODELS: PredictionModelsApi,
        TagValues.PREDICTIONS: PredictionsApi,
        TagValues.LOCATIONS: LocationsApi,
        TagValues.PRODUCT_DESIGN: ProductDesignApi,
        TagValues.ROWS: RowsApi,
        TagValues.COLUMNS: ColumnsApi,
        TagValues.VALUES: ValuesApi,
        TagValues.GRID: GridApi,
        TagValues.UNPACK: UnpackApi,
        TagValues.HEALTH_CHECK: HealthCheckApi,
        TagValues.INVENTORY: InventoryApi,
        TagValues.REPORTS_CATALOGUE: ReportsCatalogueApi,
        TagValues.ANALYTICS: AnalyticsApi,
        TagValues.USER_REPORTS: UserReportsApi,
        TagValues.SEARCH: SearchApi,
        TagValues.INTERNAL: InternalApi,
        TagValues.REPORTS_SP: ReportsSPApi,
        TagValues.DEFAULT: DefaultApi,
    }
)

tag_to_api = TagToApi(
    {
        TagValues.PREDICTION_FLOW: PredictionFlowApi,
        TagValues.PREDICTION_MODELS: PredictionModelsApi,
        TagValues.PREDICTIONS: PredictionsApi,
        TagValues.LOCATIONS: LocationsApi,
        TagValues.PRODUCT_DESIGN: ProductDesignApi,
        TagValues.ROWS: RowsApi,
        TagValues.COLUMNS: ColumnsApi,
        TagValues.VALUES: ValuesApi,
        TagValues.GRID: GridApi,
        TagValues.UNPACK: UnpackApi,
        TagValues.HEALTH_CHECK: HealthCheckApi,
        TagValues.INVENTORY: InventoryApi,
        TagValues.REPORTS_CATALOGUE: ReportsCatalogueApi,
        TagValues.ANALYTICS: AnalyticsApi,
        TagValues.USER_REPORTS: UserReportsApi,
        TagValues.SEARCH: SearchApi,
        TagValues.INTERNAL: InternalApi,
        TagValues.REPORTS_SP: ReportsSPApi,
        TagValues.DEFAULT: DefaultApi,
    }
)
