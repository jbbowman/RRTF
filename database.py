# import PyQt5
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

CONNECTION = QSqlDatabase.addDatabase('QODBC')
query = QSqlQuery(CONNECTION)

def DBConnection():
    file = open('databaseserver.txt', 'r')
    server = file.read()

    DATA = {'dbms': 'SQL Server', 'server': server, 'db': 'RRTF'}
    DETAILS = f"DRIVER={DATA['dbms']}; SERVER={DATA['server']}; DATABASE={DATA['db']}"

    CONNECTION.setDatabaseName(DETAILS)

    if not CONNECTION.open():
        QMessageBox.critical(None, 'Error', f'Database Error: {CONNECTION.lastError().databaseText()}\n\n'
                                            f'Suggestion: Attach database and verify server name in databaseserver.txt')
        sys.exit(1)

def getValue(statement):
    query.exec(statement)
    query.next()
    return query.value(0)


def getTable(statement, columns):
    query.exec(statement)
    query.next()
    rowVals = []
    while query.value(0) is not None:
        colVals = []
        for i in range(columns):
            colVals.append(query.value(i))
        rowVals.append(colVals)
        query.next()
    return rowVals


def getTable1(statement):
    query.exec(statement)
    query.next()
    rowVals = []
    while query.value(0) is not None:
        rowVals.append(query.value(0))
        query.next()
    return rowVals


# def getTableStack(statement, columns, span):
#     query.exec(statement)
#     query.last()
#     rowVals = []
#
#     for i in range(span):
#         colVals = []
#         for j in range(columns):
#             colVals.append(query.value(j))
#         rowVals.append(colVals)
#         query.previous()
#
#     return rowVals


if __name__ == "__main__":
    import sys

    try:
        DBConnection()

    except Exception as exception:
        QMessageBox.critical(None, 'Error', f'The following error occurred {exception}')
        sys.exit(1)
