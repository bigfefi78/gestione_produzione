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

        # if index.row() == 0:
        #     self.intestazione = []
        #     for i in range(model.columnCount()):
        #         self.intestazione.append(model.headerData(i, Qt.Horizontal))
        #
        #     # print(model.headerData(i, Qt.Horizontal))
        #     print(self.intestazione)

        if value is not None and role == QtCore.Qt.DisplayRole:
            return value

        if role == QtCore.Qt.TextColorRole and index.row() % 2:
            return QtGui.QColor(QtCore.Qt.darkBlue)

        if role == QtCore.Qt.FontRole:
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


class MyCustomDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        item_data = index.data(Qt.DisplayRole)  # QVariant corrispondente
        opts = QStyleOptionProgressBar()
        opts.rect = option.rect
        opts.minimum = 0  # limite minimo progress bar
        opts.maximum = 100  # limite massimo progress bar
        # opts.text = "{}/{} [{}%]".format(item_data, 100, int(item_data))
        opts.text = "{}%".format(int(item_data))
        opts.textAlignment = Qt.AlignCenter
        opts.textVisible = True
        opts.progress = int(item_data)
        QApplication.style().drawControl(QStyle.CE_ProgressBar, opts, painter)

    def createEditor(self, parent, option, index):
        print("[DELEGATE] Creating editor for index %s..." % index.row())
        editor = QSpinBox(parent)
        editor.setRange(0, 100)
        return editor

    def setEditorData(self, editor, index):
        print("[DELEGATE] Updating view for index %s..." % index.row())
        value = index.data(Qt.DisplayRole)
        editor.setValue(int(value))

    def setModelData(self, editor, model, index):
        print("[DELEGATE] Setting data to model at index %s..." % index.row())
        value = editor.value()
        variant = QtCore.QVariant(value)
        model.setData(index, variant)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MyCustomConnection()
    win = MyCustomWindow()
    model = MyCustomQSqlModel()
    model.setQuery("SELECT * FROM tableView1")
    win.widget.tableView1.setModel(model)

    for column in range(model.columnCount(QtCore.QModelIndex())-1):
        win.widget.tableView1.resizeColumnToContents(column)
        size = win.widget.tableView1.columnWidth(column)
        print(size)
        win.widget.tableView1.setColumnWidth(column, size+50)

    win.widget.tableView1.setColumnWidth(model.columnCount(QtCore.QModelIndex())-1, 650)

    delegate = MyCustomDelegate()
    win.widget.tableView1.setItemDelegateForColumn(5, delegate)
    win.showMaximized()
    sys.exit(app.exec_())
