import boto3
import sys
import json
import time

count = 0
countError = 0

def setEmptyAttributes(item):
    for (key,value) in item.items():
        if isinstance(value,dict):
            setEmptyAttributes(value)
        else:
            if value is None:
                item[key] = " "
    return item


def bulkInsertRows(documents, dynamoTableName):
    global count
    global countError
    retVal = True
    documentsCount = len(documents)
    batchSize = 20
    startInex = 0
    endIndex = batchSize
    try:
        start_time = time.time()
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(dynamoTableName)
        print('Bulk Insert to DynamoDB table {} - Starting at {}'.format(dynamoTableName, start_time))
        while startInex < endIndex:
            rows = documents[startInex:endIndex]
            bulkInsertRowsInBatch(rows,table)
            startInex = endIndex
            endIndex = (endIndex + batchSize) if (endIndex + batchSize) <= documentsCount else  documentsCount
        elapsed_time = time.time() - start_time
        print('Bulk Insert to DynamoDB success count {} error count {} time taken {}'
              .format(count, countError, elapsed_time))
    except:
        retVal = False
        exp = sys.exc_info()
        print('Unable to bulkInsertRows Into tempcompletedorders due to exception ', exp[1])
    return retVal


def bulkInsertRowsInBatch(rows, table):
    global count
    global countError
    retVal = True
    try:
        #with table.batch_writer(overwrite_by_pkeys=['orderNumber', 'orderedDate']) as batch:
        for row in rows:
            data = json.dumps(row, default=str)
            try:
                #batch.put_item(Item={
                table.put_item(Item={
                    "orderNumber":row["orderNumber"],
                    "orderedDate":str(row["orderedDate"]),
                    "data":data
                })
                count = count + 1
            except:
                countError = countError + 1
                sizeOfData = sys.getsizeof(data)
                lengthOfData = len(data)
                sys.stderr.write('Error - {} Object Size {} bytes Length {} '.format(countError,
                                                                                     sizeOfData, lengthOfData))
                sys.stderr.write('\r\n')
                sys.stderr.write('{}'.format(data))
                sys.stderr.write('\r\n')
                sys.stderr.write('----------')
                sys.stderr.write('\r\n')
                print('Error - {} Object Size {} bytes Length {} '.format(countError,sizeOfData, lengthOfData))
                print('----------')
                exp = sys.exc_info()
                print('Failed to Insert due to exception ', exp[1])
    except:
        retVal = False
        exp = sys.exc_info()
        print('Unable to bulkInsertRowsInBatch Into tempcompletedorders due to exception ', exp[1])
    return  retVal


