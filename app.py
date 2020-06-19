#!/usr/bin/python
import json

import dynamoDB
import postgresDB
from datetime import date, datetime
from pprint import pprint

import appConfig as cfg


def bulkInsertToinserttempcompletedorders(dataRows):
    insertColumns = '"' + '","'.join(cfg.mappedColumns['tempcompletedorders']) + '"'
    sql = 'insert into public.tempcompletedorders ({}) values %s'.format(insertColumns)
    # sql = 'insert into {} tempcompletedorders values '.format(insertColumns)
    postgresDB.executeInsert(sql,dataRows)


def processtempcompletedordersTable(tableName):
    for dataBlock in dynamoDB.scanTable(tableName):
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
        bulkInsertToinserttempcompletedorders(insertReadyTuples)


if __name__ == '__main__':
    now = datetime.now()
    print(" ----- Data Migration Started   at - {}  ------------".format(now.strftime("%Y-%m-%d %H:%M:%S")))

    tableName = cfg.moduurn_env["tempcompletedorders"]["dynameTableName"]
    insertData = processtempcompletedordersTable(tableName)
    print(insertData)
    # postgresDB.connect()
    # postgresDB.executeSQL()

    now = datetime.now()
    print(" ----- Data Migration completed at - {}  ------------".format(now.strftime("%Y-%m-%d %H:%M:%S")))
