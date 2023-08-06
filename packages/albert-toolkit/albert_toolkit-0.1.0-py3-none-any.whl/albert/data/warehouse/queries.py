from albert.data.warehouse.dbwarehouse_schema import (
    Unit,
    ParameterGroupParameter,
    ParameterGroupParameterUnit,
    ParamterGroupSpecialParameter,
    Prediction,
    PropertyDatum,
    InventoryCas,
)
from albert.data.warehouse.dbsession import AlbertWarehouseInterface
from albert.filters.prediction_filters import PredictionFilter
from sqlalchemy.orm import aliased, Query
from sqlalchemy.sql import func, not_, null
from sqlalchemy.sql.elements import BinaryExpression
from sqlalchemy import and_, or_
from typing import Any, Tuple, List
import logging
import pandas as pd


# SELECT
#     id,
#     taskId,
#     predictionType,
#     intervalId,
#     createdByName,
#     workflowId,
#     inventoryId,
#     dataColumnId,
#     dataColumnName,
#     modelId,
#     modelName,
#     userAverageDataPoint,
#     userStandardDeviation,
#     variable,
#     variableValue,
#     normalizedPrediction,
#     normalizedStd,
#     `normalizedStd/prediction`,
#     oneSigmaUpper,
#     oneSigmaLower,
#     percentFormulaKnown,
#     flaggingMetadata,
#     createdAt,
#     updatedAt,
#     createdByName FROM `prediction` WHERE taskId='TASFOR284488' #AND
# #predictionType = 'base'
# #AND createdByName LIKE '%Venky%'
# #AND intervalId='ROW4'
# #AND dataColumnId='DAC1230'
# #AND variable ='INVA25314'
# #AND userAverageDataPoint>0
# ORDER BY createdAt DESC


# Pull loops for a specific user/task/type
# SELECT
#     id,
#     taskId,
#     predictionType,
#     intervalId,
#     createdByName,
#     workflowId,
#     inventoryId,
#     dataColumnId,
#     dataColumnName,
#     modelId,
#     modelName,
#     userAverageDataPoint,
#     userStandardDeviation,
#     variable,
#     variableValue,
#     normalizedPrediction,
#     normalizedStd,
#     `normalizedStd/prediction`,
#     oneSigmaUpper,
#     oneSigmaLower,
#     percentFormulaKnown,
#     flaggingMetadata,
#     createdAt,
#     updatedAt
# FROM `prediction`
# WHERE predictionType='base'
# #AND createdByName LIKE '%Chris Leff%'
# AND createdByName LIKE '%Support%'
# #intervalId='default'
# #AND dataColumnId='DAC2639'
# #AND taskId='TASFOR319098'
# ORDER BY createdAt DESC


class WarehouseQueries(AlbertWarehouseInterface):
    def __init__(
        self,
        db_user: str | None = None,
        db_password: str | None = None,
        db_host: str | None = None,
        db_port: int | None = 53535,
        db_database: str | None = None,
    ):
        super().__init__(db_user, db_password, db_host, db_port, db_database)

    def get_all_inventory_cas_smiles(self) -> list[Any] | pd.DataFrame:
        a = aliased(InventoryCas)

        query: Query[Any] = (
            self.DWH_Session().query(a.casSmiles).distinct().where(a.casSmiles != None)
        )

        return query.all()

    def get_all_parameters(self) -> list[Any] | pd.DataFrame:
        a = aliased(ParameterGroupParameter)
        b = aliased(ParameterGroupParameterUnit)
        c = aliased(ParamterGroupSpecialParameter)
        u = aliased(Unit)

        query: Query[Any] = (
            self.DWH_Session()
            .query(a.id, a.name, func.ifnull(a.value, c.name), u.name)
            .join(
                b,
                and_(a.parentId == b.parentId, a.sequence == b.sequence),
                isouter=True,
            )
            .join(u, u.id == b.id, isouter=True)
            .join(
                c,
                and_(a.parentId == c.parentId, a.sequence == c.sequence),
                isouter=True,
            )
        )

        return query.all()

    def get_all_dac_dat_groups(self) -> List[Tuple[str, str, str, str, int]]:
        a = aliased(PropertyDatum)

        query: Query[Any] = (
            self.DWH_Session()
            .query(
                a.dataTemplateId,
                a.dataTemplateFullName,
                a.dataColumnId,
                a.dataColumnName,
                func.count().label("count"),
            )
            .where(and_(a.value.isnot(None), a.valueNumeric.isnot(None)))
            .group_by(a.dataTemplateId, a.dataColumnId)
        )

        return [x["name"] for x in query.column_descriptions], query.all()

    def get_all_dac_dat_data(self, dac, dat):
        a = aliased(PropertyDatum)

        query: Query[Any] = (
            self.DWH_Session()
            .query(a.taskId, a.dataColumnName, a.valueNumeric, a.valueString)
            .where(and_(a.dataColumnId == dac, a.dataTemplateId == dat))
        )

        return query.all()

    def get_model_predictions(
        self, filter: PredictionFilter, return_raw: bool = False
    ) -> list[Any] | pd.DataFrame:
        a = aliased(Prediction)

        query: Query[Any] = self.DWH_Session().query(
            a.id,
            a.taskId,
            a.predictionType,
            a.intervalId,
            a.createdByName,
            a.workflowId,
            a.inventoryId,
            a.dataColumnId,
            a.dataColumnName,
            a.modelId,
            a.modelName,
            a.userAverageDataPoint,
            a.userStandardDeviation,
            a.variable,
            a.variableValue,
            a.normalizedPrediction,
            a.normalizedStd,
            a.normalizedStd_prediction,
            a.oneSigmaUpper,
            a.oneSigmaLower,
            a.percentFormulaKnown,
            a.flaggingMetadata,
            a.createdAt,
            a.updatedAt,
        )

        # Now we modify the query with the filter parameters
        filter_params = filter.get_filter_params()

        def get_condition_statement(
            fname: str, is_exact: bool, value: Any
        ) -> BinaryExpression[Any]:
            if is_exact:
                return getattr(a, fname) == value
            else:
                if isinstance(value, str):
                    # for strings that are approximate we match using the LIKE parameter
                    return getattr(a, fname).like(value)
                else:
                    logging.warn(
                        (
                            f"approximate matching for type {type(value)} is not currently "
                            "supported, we will be using exact matching"
                        )
                    )
                    return getattr(a, fname) == value

        if len(filter_params) > 0:
            if len(filter_params) == 1:
                # We only have a single condition, so append the query with a simple where statement
                field_name, isexact, field_value = filter_params[0]
                query = query.where(
                    get_condition_statement(field_name, isexact, field_value)
                )
            else:
                # We have multiple matching conditions so we need to and them all together
                # First create a list of all of the conditions
                conditions = [
                    get_condition_statement(fn, ee, fv)
                    for (fn, ee, fv) in filter_params
                ]
                query = query.where(and_(*conditions))

        if return_raw:
            return query.all()
        else:
            # Return as a dataframe with column names that match
            # the names of the fields returned
            cnames = [d["name"] for d in query.column_descriptions]
            return pd.DataFrame(query.all(), columns=cnames)


# import requests

# def get_models(jwt_token):
#     # Set the API endpoint URL with the entity and ID parameters
#     url = "https://app.albertinvent.com/api/v3/predictions/models?entity=organization&id=Albert"

#     # Set the authorization header with the JWT token
#     headers = {"Authorization": "Bearer " + jwt_token}

#     # Make a GET request to the API endpoint with the headers
#     response = requests.get(url, headers=headers)

#     # Check if the response was successful
#     if response.status_code == 200:
#         # Return the response content as a string
#         return response.content.decode('utf-8')
#     else:
#         # If the response was not successful, raise an exception with the error code and message
#         response.raise_for_status()

# import requests

# def get_latest_version(jwt_token, modelID):
#     # Set the PMD68 endpoint URL
#     endpoint = f"https://app.albertinvent.com/api/v3/predictions/models/{modelID}"

#     # Set the authorization header with the JWT token
#     headers = {"Authorization": "Bearer " + jwt_token}

#     # Make a GET request to the PMD68 endpoint with the headers
#     response = requests.get(endpoint, headers=headers)

#     # Check if the response was successful
#     if response.status_code == 200:
#         # Parse the JSON response and return the "version" field as a string
#         return response.json()["version"]
#     else:
#         # If the response was not successful, raise an exception with the error code and message
#         response.raise_for_status()

# import requests

# def update_model(jwt_token, model_id, version, payload):
#     # Set the API endpoint URL with the model ID and version parameters
#     url = f"https://app.albertinvent.com/api/v3/predictions/models/{model_id}/version?id={version}"

#     # Set the authorization header with the JWT token
#     headers = {"Authorization": "Bearer " + jwt_token}

#     # Set the payload as JSON
#     json_payload = {"data": payload}

#     # Make a PATCH request to the API endpoint with the headers and payload
#     response = requests.patch(url, headers=headers, json=json_payload)

#     # Check if the response was successful or returned 204
#     if response.status_code == 204:
#         # Return True to indicate success
#         return True
#     else:
#         # If the response was not successful or 204, raise an exception with the error code and message
#         response.raise_for_status()

# model_id = "PMD29"

# payload = [
#         {
#         "operation":"update",
#         "attribute":"graduated",
#         "oldValue":False,
#         "newValue":True
#         }
#     ]

# version = get_latest_version(jwt,model_id)
# update_model(jwt,model_id,version,payload)
