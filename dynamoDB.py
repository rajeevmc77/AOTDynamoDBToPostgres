import boto3
from boto3.dynamodb.conditions import Key

dynamodb = None

def init(tableName):
    global dynamodb
    table = None
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(tableName)
    return table


def scanTable(tableName):
    scan_kwargs = {
        # 'FilterExpression': Key('year').between(*year_range),
        # 'ProjectionExpression': "#yr, title, info.rating",
        # 'ExpressionAttributeNames': {"#yr": "year"}
    }
    done = False
    start_key = None
    table = init(tableName)
    if not table:
        raise StopIteration
    while not done:
        if start_key:
            scan_kwargs['ExclusiveStartKey'] = start_key
        response = table.scan(**scan_kwargs)
        if 'Items' not in response:
            raise StopIteration
        yield response['Items']
        start_key = response.get('LastEvaluatedKey', None)
        done = start_key is None