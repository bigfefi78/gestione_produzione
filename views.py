from PyQt5 import QtWidgets, QtSql, QtGui

class PersonWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(PersonWidget, self).__init__(parent)
        lay = QtWidgets.QVBoxLayout(self)
        view = QtWidgets.QTableView()
        lay.addWidget(view)
        model = QtSql.QSqlTableModel(self)
        model.setTable("person")
        model.select()
        view.setModel(model)

class ItemsWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ItemsWidget, self).__init__(parent)
        lay = QtWidgets.QVBoxLayout(self)
        view = QtWidgets.QTableView()
        lay.addWidget(view)
        model = QtSql.QSqlTableModel(self)
        model.setTable("items")
        model.select()
        view.setModel(model)