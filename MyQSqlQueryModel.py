import sys
import os
from PyQt5.QtCore import QVariant, Qt
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase, QSqlQueryModel
from PyQt5.QtWidgets import (QApplication, QTableView, QLabel, QItemDelegate,
                             QStyledItemDelegate, QStyle, QStyleOptionProgressBar,
                             QSpinBox)
from gui_file.QTableView import *

ui = Ui_Form()
ui.setupUi()

if __name__ == "__main__":
    app = QApplication(sys.argvar)
    ui.show()
    sys.exit(app.exec())
