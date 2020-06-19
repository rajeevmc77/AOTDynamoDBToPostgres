#env = "dev"
env = "prod"

moduurn_prod = {
    "tempcompletedorders": {"dynameTableName": "tempcompletedorders", "cleanPeriodInDays": 183}
}

moduurn_dev = {
    "tempcompletedorders": {"dynameTableName": "tempcompletedorders_dev", "cleanPeriodInDays": 182}
}

moduurn_db_prod = {
    "host": "portal-ssl1530-2.moduurn-prod.2473306818.composedb.com",
    "port": 18134,
    "user": "app",
    "password": "XAd123#21#",
    "db": "moduurndb_prod",
    "authSource": "moduurndb_prod",
    "ssl": "true"
}

moduurn_db_dev = {
    "host": "portal-ssl1276-1.moduurn-dev.2473306818.composedb.com",
    "port": 18130,
    "user": "appdev",
    "password": "XAd123#21#",
    "db": "coredb",
    "authSource": "coredb",
    "ssl": "true"
}

mappedColumns = {
    'tempcompletedorders': ['organizationId',
                            'orderNumber',
                            'locationId',
                            'totalPrice',
                            'orderVia',
                            'subTotal',
                            'orderedDate',
                            'data']
}

if env == "dev":
    moduurn_db = moduurn_db_dev
    moduurn_env = moduurn_dev

else:
    moduurn_db = moduurn_db_prod
    moduurn_env = moduurn_prod
