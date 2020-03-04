"""

copiato da

https://stackoverflow.com/questions/48036069/how-to-subclass-qsqltablemodel-in-pyqt5

"""


import sys

from PyQt5.QtCore import QVariant, Qt
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase, QSqlQueryModel
from PyQt5.QtWidgets import (QApplication, QTableView, QLabel, QItemDelegate,
                             QStyledItemDelegate, QStyle, QStyleOptionProgressBar,
                             QSpinBox)


class ImportSqlTableModel(QSqlTableModel):
    def __init__(self, *args, **kwargs):
        super(ImportSqlTableModel, self).__init__(*args, **kwargs)
        self.booleanSet = [4, 5, 6]  # column with checkboxes
        self.readOnlySet = [0]  # columns which must not be changed
        self.setTable("matricole")
        # self.setQuery("SELECT * FROM matricole")
        self.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.select()

    def data(self, index, role=Qt.DisplayRole):
        value = super(ImportSqlTableModel, self).data(index)
        if index.column() in self.booleanSet:
            if role == Qt.CheckStateRole:
                return Qt.Unchecked if value == 2 else Qt.Checked
            else:
                return QVariant()
        return QSqlTableModel.data(self, index, role)
        # return QSqlQueryModel.data(self, index)

    def setData(self, index, value, role=Qt.EditRole):
        print("setData method...")
        if not index.isValid():
            return False
        if index.column() in self.booleanSet:
            if role == Qt.CheckStateRole:
                val = 2 if value == Qt.Unchecked else 0
                return QSqlTableModel.setData(self, index, val, Qt.EditRole)
            else:
                return False
        else:
            return QSqlTableModel.setData(self, index, value, role)

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags
        if index.column() in self.booleanSet:
            return Qt.ItemIsUserCheckable | Qt.ItemIsEnabled | Qt.ItemIsEditable
        elif index.column() in self.readOnlySet:
            return Qt.ItemIsSelectable | Qt.ItemIsEnabled
        else:
            return QSqlTableModel.flags(self, index)


class CustomDelegate(QStyledItemDelegate):
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
        variant = QVariant(value)
        model.setData(index, variant)


class ReadOnlyDelegate(QItemDelegate):
    def createEditor(self, parent, option, index):
        lb = QLabel(parent)
        return lb


if __name__ == '__main__':
    app = QApplication(sys.argv)

    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName("db\database.db")
    if not db.open():
        sys.exit(-1)
    model = ImportSqlTableModel()
    delegate = CustomDelegate()

    w1 = QTableView()
    w1.setWindowTitle("QTableView #1")
    w1.setModel(model)
    w1.setItemDelegateForColumn(3, delegate)
    w1.show()

    w2 = QTableView()
    w2.setWindowTitle("QTableView #2")
    w2.setModel(model)
    w2.setItemDelegateForColumn(3, delegate)
    w2.show()

    for col in model.booleanSet:
        w1.setItemDelegateForColumn(col, ReadOnlyDelegate(w1))


    sys.exit(app.exec_())