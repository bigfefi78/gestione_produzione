from PyQt5 import QtCore, QtGui, QtSql, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
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


def getHeaders():
    query = QtSql.QSqlQuery()
    query.exec_('SELECT *  FROM tableView1')
    head = []
    i = 0
    while i < query.record().count():
        head.append(query.record().fieldName(i))
        i += 1
    return head


class MySignal(QtCore.QObject):

    trigger = QtCore.pyqtSignal(str)

    def connect_and_emit_trigger(self, pro):
        # Connect the trigger signal to a slot.
        self.trigger.connect(self.handle_trigger)
        self.trigger.connect(pro.setFilterRegExp)

        # Emit the signal.
        self.trigger.emit('30')

    def handle_trigger(self, stringa):
        # Show that the slot has been called.

        print("trigger signal received with parameter -->", stringa)


class MyCustomQSqlModel(QtSql.QSqlQueryModel):
    """
    QSqlModel based model. We need to re-implement setData() and flags()
    to make it read/write
    """

    def flags(self, index):
        flags = super(MyCustomQSqlModel, self).flags(index)

        if index.column() is not None:
            flags |= QtCore.Qt.ItemIsEditable

        return flags

    def data(self, index, role):
        value = super(MyCustomQSqlModel, self).data(index, role)

        if value is not None and role == QtCore.Qt.DisplayRole:
            return value

        if role == QtCore.Qt.TextColorRole and index.row() % 2:
            return QtGui.QColor(QtCore.Qt.blue)

        if role == QtCore.Qt.TextAlignmentRole:
            return QtCore.Qt.AlignCenter

        if role == QtCore.Qt.FontRole:
            font = QtGui.QFont('Courier new')
            font.setPixelSize(16)
            font.setCapitalization(QtGui.QFont.AllUppercase)
            return QtCore.QVariant(font)

        return value

    def setData(self, index, value, role):
        print("setData method...")
        if index.column() != 5:
            print("False, index column = ", index.column())
            return False
        else:
            print("modificata colonna 6")
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
        # model.clear()
        # model.setQuery("SELECT * FROM tableView1")
        model.setData(index, variant, Qt.DisplayRole)
        return


class MyCustomProxyFilter(QtCore.QSortFilterProxyModel):
    def __init__(self):
        super(MyCustomProxyFilter, self).__init__()
        self.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.setDynamicSortFilter(True)
        self.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)

    @QtCore.pyqtSlot(str)
    def regularFilterFormat(self, value):
        regstring = value.replace(" ", "|")
        self.setFilterRegExp(regstring)


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

        self.pushBtn = QtWidgets.QPushButton('Clear')

        self.clearButton = QtWidgets.QPushButton()
        self.filterLine = QtWidgets.QLineEdit()

        self.pushBtn.clicked.connect(self.filterLine.clear)
        self.tableView1.setAlternatingRowColors(True)
        self.tableView1.resizeColumnsToContents()
        self.tableView1.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.tableView2.setAlternatingRowColors(True)

        self.HLayout = QtWidgets.QHBoxLayout()
        self.HLayout1 = QtWidgets.QHBoxLayout()
        self.VLayout = QtWidgets.QVBoxLayout()

        self.HLayout1.addWidget(self.filterLine)
        self.HLayout1.addWidget(self.pushBtn)

        self.VLayout.addLayout(self.HLayout1)
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

        self.model_1 = MyCustomQSqlModel()
        self.model_1.setQuery("SELECT * FROM tableView1")

        self.proxy = MyCustomProxyFilter()
        self.proxy.setFilterKeyColumn(6)
        self.proxy.setSourceModel(self.model_1)

        self.widget = MyCustomWidget()
        self.widget.filterLine.textChanged.connect(self.proxy.regularFilterFormat)
        self.widget.tableView1.setModel(self.proxy)

        self.delegate = MyCustomDelegate()
        self.widget.tableView1.setItemDelegateForColumn(5, self.delegate)

        self.widget.tableView1.clicked.connect(self.view1Selection)
        self.push = QtWidgets.QPushButton()
        self.setWindowTitle("My custom MVC implementation")
        self.setCentralWidget(self.widget)

    def view1Selection(self, index):
        print(self.model_1.columnCount())
        print(self.model_1.data(index, QtCore.Qt.DisplayRole))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MyCustomConnection()

    win = MyCustomWindow()

    headers = getHeaders()
    print(headers)

    for column in range(win.widget.tableView1.model().columnCount(QtCore.QModelIndex())-1):
        win.widget.tableView1.resizeColumnToContents(column)
        size = win.widget.tableView1.columnWidth(column)
        win.widget.tableView1.setColumnWidth(column, size+50)

    win.widget.tableView1.setColumnWidth(win.widget.tableView1.model().columnCount(QtCore.QModelIndex())-1, 650)

    win.show()
    sys.exit(app.exec_())
