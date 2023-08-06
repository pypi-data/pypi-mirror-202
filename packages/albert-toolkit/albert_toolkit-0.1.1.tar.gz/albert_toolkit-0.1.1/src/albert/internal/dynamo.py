import boto3
from boto3.dynamodb.conditions import Key, Attr
from typing import Dict, Any, List


class DynamoModelInfo:
    def __init__(self, modelTableName="albert-app2", profile_name="dev") -> None:
        session = boto3.Session(profile_name=profile_name)
        self.dyn_res = session.resource("dynamodb")
        self.table = self.dyn_res.Table(modelTableName)
        self.table.load()

    def get_published_models(
        self, tenant_id, onDate: str = None
    ) -> List[Dict[str, Any]]:
        lastEvaluatedKey = None
        items = []

        primary_key = f"{tenant_id}#PMD"

        while True:
            if lastEvaluatedKey is None:
                res = self.table.query(
                    IndexName="GS1",
                    KeyConditionExpression=Key("GS1PK").eq(primary_key),
                    FilterExpression=(
                        Attr("createdAt").begins_with(onDate)
                        if onDate is not None
                        else None
                    ),
                )
            else:
                res = self.table.query(
                    IndexName="GS1",
                    KeyConditionExpression=Key("GS1PK").eq(primary_key),
                    FilterExpression=(
                        Attr("createdAt").begins_with(onDate)
                        if onDate is not None
                        else None
                    ),
                    ExclusiveStartKey=lastEvaluatedKey,
                )

            items.extend(res["Items"])
            if "LastEvaluatedKey" in res:
                lastEvaluatedKey = res["LastEvaluatedKey"]
            else:
                break

        return items
