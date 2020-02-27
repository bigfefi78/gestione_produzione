from PyQt5 import QtCore, QtGui, QtSql, QtWidgets
from PyQt5.QtWidgets import *
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


class MyCustomWidget(QtWidgets.QWidget):
    """
    Base widget definition
    that acts as a MVC view
    """
    def __init__(self, parent=None):
        super(MyCustomWidget, self).__init__(parent)

        self.tableView1 = QtWidgets.QTableView()
        self.tableView2 = QtWidgets.QTableView()
        self.columnView = QtWidgets.QColumnView()
        self.pushBtn = QtWidgets.QPushButton()

        self.tableView1.setAlternatingRowColors(True)
        self.tableView1.resizeColumnsToContents()

        self.tableView2.setAlternatingRowColors(True)

        self.HLayout = QtWidgets.QHBoxLayout()
        self.VLayout = QtWidgets.QVBoxLayout()

        self.VLayout.addWidget(self.tableView1)
        self.VLayout.addWidget(self.tableView2)
        self.VLayout.addWidget(self.columnView)

        self.HLayout.addLayout(self.VLayout)
        self.HLayout.addWidget(self.pushBtn)

        self.setLayout(self.HLayout)


class MyCustomWindow(QtWidgets.QMainWindow):
    """
    Main window definition
    """
    def __init__(self, parent=None):
        super(MyCustomWindow, self).__init__(parent)

        self.model = MyCustomQSqlModel()

        self.widget = MyCustomWidget()
        # self.widget.tableView1.setModel(self.model.model)
        self.push = QtWidgets.QPushButton()
        self.setWindowTitle("My custom MVC implementation")
        self.setCentralWidget(self.widget)


class MyCustomQSqlModel(QtSql.QSqlQueryModel):
    """
    QSqlModel based model. We need to re-implement setData() and flags()
    to make it read/write
    """

    def flags(self, index):
        flags = super(MyCustomQSqlModel, self).flags(index)

        if index.column() in (0, 1):
            flags |= QtCore.Qt.ItemIsEditable

        return flags

    def data(self, index, role):
        value = super(MyCustomQSqlModel, self).data(index, role)
        if value is not None and role == QtCore.Qt.DisplayRole:
            return value

        if role == QtCore.Qt.TextColorRole and index.row() % 2:
            return QtGui.QColor(QtCore.Qt.darkBlue)

        if role == QtCore.Qt.FontRole:
            print("Qfont")
            font = QtGui.QFont('Courier new')
            font.setPixelSize(14)
            # font.setWeight(75)
            font.setCapitalization(QtGui.QFont.AllUppercase)
            return QtCore.QVariant(font)
            # return QtGui.QFont.Bold

        return value

    def setData(self, index, value, role):
        print("setData method...")
        if index.column() != 1:
            print("False, index column = ", index.column())
            return False
        else:
            print("Colonna: ", index.column(), " valore:", value)
            return True


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MyCustomConnection()
    win = MyCustomWindow()
    model = MyCustomQSqlModel()
    model.setQuery("SELECT * FROM matricole")
    win.widget.tableView1.setModel(model)
    win.show()
    sys.exit(app.exec_())