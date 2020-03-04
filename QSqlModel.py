from PyQt4 import QtCore, QtGui, QtSql
from PyQt4.QtCore import QVariant, Qt
from PyQt4.QtSql import QSqlTableModel, QSqlDatabase, QSqlQueryModel
from PyQt4.QtGui import (QApplication, QTableView, QLabel, QItemDelegate,
                        QStyledItemDelegate, QStyle, QStyleOptionProgressBar,
                        QSpinBox)

# from PyQt4 import QtSql, QtGui


def createConnection():
    db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName(":memory:")
    if not db.open():
        QtGui.QMessageBox.critical(None, QtGui.qApp.tr("Cannot open database"),
                                   QtGui.qApp.tr("Unable to establish a database connection.\n"
                                                 "This example needs SQLite support. Please read "
                                                 "the Qt SQL driver documentation for information "
                                                 "how to build it.\n\nClick Cancel to exit."),
                                   QtGui.QMessageBox.Cancel, QtGui.QMessageBox.NoButton)
        return False

    query = QtSql.QSqlQuery()
    query.exec_("create table person(id int primary key, "
                "firstname varchar(20), lastname varchar(20))")
    query.exec_("insert into person values(101, 'Danny', 'Young')")
    query.exec_("insert into person values(102, 'Christine', 'Holand')")
    query.exec_("insert into person values(103, 'Lars', 'Gordon')")
    query.exec_("insert into person values(104, 'Roberto', 'Robitaille')")
    query.exec_("insert into person values(105, 'Maria', 'Papadopoulos')")
    return True


class CustomSqlModel(QtSql.QSqlQueryModel):
    def data(self, index, role):
        print("Model data!!!!!")
        value = super(CustomSqlModel, self).data(index, role)
        if value is not None and role == QtCore.Qt.DisplayRole:
            if index.column() == 0:
                return '#%d' % value
            elif index.column() == 2:
                return value.upper()

        if role == QtCore.Qt.TextColorRole and index.column() == 1:
            return QtGui.QColor(QtCore.Qt.blue)

        return value


class EditableSqlModel(QtSql.QSqlQueryModel):
    def flags(self, index):
        flags = super(EditableSqlModel, self).flags(index)

        if index.column() in (1, 2):
            flags |= QtCore.Qt.ItemIsEditable

        return flags

    def setData(self, index, value, role):
        if index.column() not in (1, 2):
            return False

        primaryKeyIndex = self.index(index.row(), 0)
        id = self.data(primaryKeyIndex)

        self.clear()

        if index.column() == 1:
            ok = self.setFirstName(id, value)
        else:
            ok = self.setLastName(id, value)

        self.refresh()
        print("Esito : ", ok)
        return ok

    def refresh(self):
        print("refreshing...")
        initializeModel(plainModel)
        self.setQuery('select * from person')
        self.setHeaderData(0, QtCore.Qt.Horizontal, "ID")
        self.setHeaderData(1, QtCore.Qt.Horizontal, "First name")
        self.setHeaderData(2, QtCore.Qt.Horizontal, "Last name")

    def setFirstName(self, personId, firstName):
        query = QtSql.QSqlQuery()
        query.prepare('update person set firstname = ? where id = ?')
        query.addBindValue(firstName)
        query.addBindValue(personId)
        return query.exec_()

    def setLastName(self, personId, lastName):
        query = QtSql.QSqlQuery()
        query.prepare('update person set lastname = ? where id = ?')
        query.addBindValue(lastName)
        query.addBindValue(personId)
        return query.exec_()


class CustomDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        item_data = index.data(Qt.DisplayRole)  # QVariant corrispondente
        opts = QStyleOptionProgressBar()
        opts.rect = option.rect
        opts.minimum = 0  # limite minimo progress bar
        opts.maximum = 100  # limite massimo progress bar
        # opts.text = "{}/{} [{}%]".format(item_data, 100, int(item_data))
        # opts.text = "{}%".format(int(item_data))
        opts.textAlignment = Qt.AlignCenter
        opts.textVisible = True
        opts.progress = 50 #int(item_data)
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


def initializeModel(model):
    model.setQuery('select * from person')
    model.setHeaderData(0, QtCore.Qt.Horizontal, "ID")
    model.setHeaderData(1, QtCore.Qt.Horizontal, "First name")
    model.setHeaderData(2, QtCore.Qt.Horizontal, "Last name")


offset = 0
views = []


def createView(title, model, delegate=None):
    global offset, views

    view = QtGui.QTableView()
    views.append(view)
    view.setModel(model)
    view.setWindowTitle(title)
    view.setItemDelegateForColumn(2, delegate)
    view.move(100 + offset, 100 + offset)
    offset += 20
    view.show()


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    a = createConnection()
    if not a: #connection.createConnection():
        sys.exit(1)

    plainModel = QtSql.QSqlQueryModel()
    editableModel = EditableSqlModel()
    customModel = CustomSqlModel()

    delegate = CustomDelegate()


    initializeModel(plainModel)
    initializeModel(editableModel)
    initializeModel(customModel)

    createView("Plain Query Model", plainModel)
    createView("Editable Query Model", editableModel)
    createView("Custom Query Model", customModel, delegate)

    sys.exit(app.exec_())