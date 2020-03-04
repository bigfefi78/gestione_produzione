from PyQt5 import QtCore, QtGui, QtSql, QtWidgets
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from gui_file.v0 import MyForm
from PyQt5.QtCore import Qt
import sys


def MyCustomConnection():
    """ Connection to SQLite databse"""

    db = QSqlDatabase().addDatabase("QSQLITE")
    db.setDatabaseName("db\database.db")
    if db.open():
        print("Connection Opened...")
    else:
        sys.exit(-1234)

class MyCustomModel(QSqlTableModel):
    def __init__(self, parent=None):
        super(MyCustomModel, self).__init__(parent)

    def data(self, index, role=None):
        print(role)
        if role == Qt.DisplayRole:
            print("MyCustomModel instance created...")
            self.model = QSqlTableModel()
            self.model.setTable("matricole")
            self.model.select()
            return self.model

    def rowCount(self, index):
        return self.model.rowCount()


class MyCustomView(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(MyCustomView, self).__init__()

        print("MyCustomView instance created...")

        self.model = MyCustomModel()
        self.view = QtWidgets.QTableView(self)
        self.view.setAlternatingRowColors(True)
        self.view.setModel(self.model)


class MyCustomDelegate():
    pass


class MyCustomController():
    pass


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MyCustomConnection()
    # model  = MyCustomModel()
    Form = MyCustomView()
    Form.show()
    sys.exit(app.exec_())
