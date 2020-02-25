from PyQt5 import QtCore, QtGui, QtSql, QtWidgets
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from gui_file.v0 import MyForm
import sys

def createConnection():
    print("Creazione connessione...")
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName("db\database.db")
    if not db.open():
        QtWidgets.QMessageBox.critical(None, "Cannot open database ")
        return False
    return True


class Matricole(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Matricole, self).__init__(parent)
        model = QtSql.QSqlTableModel(self)
        model.setTable("matricole")
        model.select()
        MyForm.tableView1.setModel(model)

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)

    if not createConnection():
        sys.exit(-1)

    Form = QtWidgets.QWidget()

    ui = MyForm()
    ui.setupUi(Form)

    Form.show()
    sys.exit(app.exec_())
