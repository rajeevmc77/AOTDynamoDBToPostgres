#!/usr/bin/python
import json

import dynamoDB
import postgresDB
from datetime import date, datetime
from pprint import pprint

import appConfig as cfg

totalDocumentsMigrated = 0

def bulkInsertToinserttempcompletedorders(dataRows):
    global totalDocumentsMigrated
    insertColumns = '"' + '","'.join(cfg.mappedColumns['tempcompletedorders']) + '"'
    sql = 'insert into public.tempcompletedorders ({}) values %s'.format(insertColumns)
    totalDocumentsMigrated = totalDocumentsMigrated + postgresDB.executeInsert(sql,dataRows)


def processtempcompletedordersTable(tableName):
    for dataBlock in dynamoDB.scanTable(tableName):
        pageSize = 0
        insertReadyTuples = []
        for dataRow in dataBlock:
            data = json.loads(dataRow['data'])
            processedRow = postgresDB.prepareDataForTableInsert('tempcompletedorders', data)
            tupleList = []
            for dataColumn in cfg.mappedColumns['tempcompletedorders']:
                if dataColumn in processedRow:
                    tupleList.append(processedRow[dataColumn])
                else:
                    tupleList.append(None)
            insertReadyTuples.append(tuple(tupleList))
            pageSize = pageSize + 1
            if pageSize > 100 :
                bulkInsertToinserttempcompletedorders(insertReadyTuples)
                pageSize = 0
                insertReadyTuples = []
        bulkInsertToinserttempcompletedorders(insertReadyTuples)


if __name__ == '__main__':
    global totalDocumentsMigrated
    now = datetime.now()
    print(" ----- Data Migration Started   at - {}  ------------".format(now.strftime("%Y-%m-%d %H:%M:%S")))

    tableName = cfg.moduurn_env["tempcompletedorders"]["dynameTableName"]
    processtempcompletedordersTable(tableName)

    now = datetime.now()
    print(" ----- {} Documents migrated to Postgres completed at - {}  ------------".format(totalDocumentsMigrated,now.strftime("%Y-%m-%d %H:%M:%S")))
