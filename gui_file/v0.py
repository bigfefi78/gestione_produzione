# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'v0.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class MyForm(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(754, 659)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter = QtWidgets.QSplitter(Form)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.tableView1 = QtWidgets.QTableView(self.splitter)
        self.tableView1.setEditTriggers(QtWidgets.QAbstractItemView.CurrentChanged|QtWidgets.QAbstractItemView.DoubleClicked|QtWidgets.QAbstractItemView.EditKeyPressed|QtWidgets.QAbstractItemView.SelectedClicked)
        self.tableView1.setAlternatingRowColors(True)
        self.tableView1.setIconSize(QtCore.QSize(10, 10))
        self.tableView1.setObjectName("tableView1")
        self.pushButton1 = QtWidgets.QPushButton(self.splitter)
        self.pushButton1.setObjectName("pushButton1")
        self.verticalLayout.addWidget(self.splitter)
        self.splitter_2 = QtWidgets.QSplitter(Form)
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setObjectName("splitter_2")
        self.tableView2 = QtWidgets.QTableView(self.splitter_2)
        self.tableView2.setEditTriggers(QtWidgets.QAbstractItemView.CurrentChanged|QtWidgets.QAbstractItemView.DoubleClicked|QtWidgets.QAbstractItemView.EditKeyPressed|QtWidgets.QAbstractItemView.SelectedClicked)
        self.tableView2.setAlternatingRowColors(True)
        self.tableView2.setObjectName("tableView2")
        self.pushButton2 = QtWidgets.QPushButton(self.splitter_2)
        self.pushButton2.setCheckable(False)
        self.pushButton2.setFlat(False)
        self.pushButton2.setObjectName("pushButton2")
        self.verticalLayout.addWidget(self.splitter_2)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton1.setText(_translate("Form", "PushButton1"))
        self.pushButton2.setText(_translate("Form", "PushButton2"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = MyForm()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
