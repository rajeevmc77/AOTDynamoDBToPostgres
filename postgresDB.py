from datetime import datetime

import psycopg2
import psycopg2.extras
import psycopg2.extensions

from configparser import ConfigParser
import json

import appConfig

conn = None
cur = None

tableColumns = {}

def cleanupDB():
    if conn is not None:
        conn.close()

def config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db

def getCursor():
    global conn
    global cur
    try:
        if conn is not None:
            return conn.cursor()
        params = config()
        conn = psycopg2.connect(**params)
        conn.autocommit=True
        cur = conn.cursor()
        return cur
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def getTableColumns(tableName='tempcompletedorders'):
    cursor = None
    columns = None
    global tableColumns
    global conn
    try:
        if tableName in tableColumns:
            return tableColumns[tableName]
        sql = 'SELECT column_name, data_type  FROM INFORMATION_SCHEMA.COLUMNS where table_name = \'{}\''.format(tableName)
        cursor = getCursor()
        cursor.execute(sql)
        columns = cursor.fetchall()
        tableColumns[tableName] = columns
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return columns

def prepareDataForTableInsert(tableName='tempcompletedorders', data= []):
    preparedData = {}
    preparedData['data'] = json.dumps(data)
    try:
        columns = getTableColumns(tableName)
        for column in appConfig.mappedColumns[tableName]:
            dataItem = data.get(column)
            if dataItem:
                dataType = [item for item in columns if item[0] == column]
                if dataType[0][1].startswith('time'):
                    dataItem = datetime.strptime(dataItem, '%Y-%m-%d %H:%M:%S.%f')
                preparedData[column] = dataItem
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return  preparedData

def executeInsert(statement='', data=[]):
    global conn
    cursor = None
    try:
        cursor = getCursor()
        psycopg2.extras.execute_values(cursor, statement, data, template=None, page_size=200)
        cursor.close()
        print ("Migrated {} documents to Postgres".format(len(data)))
        return len(data)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        cursor.close()



