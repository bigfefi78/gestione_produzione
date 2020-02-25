# import sys
# import json
# from PyQt5.QtWidgets import (QApplication, QListView, QMainWindow, QVBoxLayout,
#                              QWidget)
# from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt, QVariant
#
#
# class MainWindow(QMainWindow):
#     def __init__(self, parent=None, model=None):
#         super(MainWindow, self).__init__(parent)
#         self.setWindowTitle("Custom ListView Example")
#         self.central_widget = FormWidget(self, model)
#         self.setCentralWidget(self.central_widget)
#         self.resize(300, 200)
#
#
# class FormWidget(QWidget):
#     def __init__(self, parent, model=None):
#         super(FormWidget, self).__init__(parent)
#         layout = QVBoxLayout()
#         self.setLayout(layout)
#         self.view = QListView()
#         self.view.setAlternatingRowColors(True)
#         self.view.setModel(model)
#         layout.addWidget(self.view)
#
#
# class CustomListModel(QAbstractListModel):
#     def __init__(self, parent=None, valori=[]):
#         super(CustomListModel, self).__init__(parent)
#         self._data = valori
#
#     def rowCount(self, parent=QModelIndex()):
#         return len(self._data)
#
#     def data(self, index, role=Qt.DisplayRole):
#         if not index.isValid() or not 0 <= index.row() < self.rowCount():
#             return QVariant()
#         row = index.row()
#         if role == Qt.DisplayRole:
#             return str(self._data[row])
#         return QVariant()
#
#
# if __name__ == "__main__":
#
#     app = QApplication([sys.argv])
#
#     with open('json_file\info.json', 'r') as f:
#         distro = json.load(f)
#
#     print(json.dumps(distro, indent=4))
#
#     # iterable = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
#     iterable = ["1", "a"]
#     print(type(distro))
#     print(type(iterable))
#     print(type(list(distro.keys())))
#
#     model = CustomListModel(None, list(distro["1"]["1.2"].keys()))
#     main_window = MainWindow(None, model)
#     main_window.show()
#     sys.exit(app.exec_())

from PyQt5 import QtWidgets, QtSql, QtGui

from connection import createConnection
from views import PersonWidget, ItemsWidget


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.mdiarea = QtWidgets.QMdiArea()
        self.setCentralWidget(self.mdiarea)
        # self.setWindowIcon(QtGui.QIcon('images\marposs.png'))

        sub1 = QtWidgets.QMdiSubWindow()
        sub1.setWidget(PersonWidget())
        # sub1.setWindowIcon(QtGui.QIcon('images\marposs.png'))
        self.mdiarea.addSubWindow(sub1)
        sub1.show()

        sub2 = QtWidgets.QMdiSubWindow()
        sub2.setWidget(ItemsWidget())
        # sub2.setWindowIcon(QtGui.QIcon('images\marposs.png'))
        self.mdiarea.addSubWindow(sub2)
        sub2.show()

if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)

    if not createConnection():
        sys.exit(-1)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())