# import PyQt5
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

CONNECTION = QSqlDatabase.addDatabase('QODBC')
query = QSqlQuery(CONNECTION)

def DBConnection():
    DATA = {'dbms': 'SQL Server', 'server': 'LAPTOP-32MVAP54\SQLEXPRESS', 'db': 'RRTF'}
    DETAILS = f"DRIVER={DATA['dbms']}; SERVER={DATA['server']}; DATABASE={DATA['db']}"

    CONNECTION.setDatabaseName(DETAILS)

    if not CONNECTION.open():
        QMessageBox.critical(None, 'Error', f'Database Error: {CONNECTION.lastError().databaseText()}')
        sys.exit(1)

def getValue(statement):
    query.exec(statement)
    query.next()
    return query.value(0)

def getTableStack(statement, columns, span):
    query.exec(statement)
    query.last()
    rowVals = []

    for i in range(span):
        colVals = []
        for j in range(columns):
            colVals.append(query.value(j))
        rowVals.append(colVals)
        query.previous()

    return rowVals

if __name__ == "__main__":
    import sys

    try:
        DBConnection()

    except Exception as exception:
        QMessageBox.critical(None, 'Error', f'The following error occurred {exception}')
        sys.exit(1)
