# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from albert.api.apis.tag_to_api import tag_to_api

import enum


class TagValues(str, enum.Enum):
    PREDICTION_FLOW = "Prediction Flow"
    PREDICTION_MODELS = "Prediction Models"
    PREDICTIONS = "Predictions"
    LOCATIONS = "Locations"
    PRODUCT_DESIGN = "ProductDesign"
    ROWS = "Rows"
    COLUMNS = "Columns"
    VALUES = "Values"
    GRID = "Grid"
    UNPACK = "Unpack"
    HEALTH_CHECK = "Health Check"
    INVENTORY = "Inventory"
    REPORTS_CATALOGUE = "Reports Catalogue"
    ANALYTICS = "Analytics"
    USER_REPORTS = "User Reports"
    SEARCH = "search"
    INTERNAL = "Internal"
    REPORTS_SP = "Reports SP"
    DEFAULT = "default"
