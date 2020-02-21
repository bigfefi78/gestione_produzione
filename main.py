import json
import sys
from PyQt5 import QtWidgets, QtGui

with open('json_file\info.json') as json_file:
    data = json.load(json_file)
    print(json.dumps(data, indent=6))

print(__name__)


if __name__ == "__main__":

    app = QtGui.QGuiApplication(sys.argv)

    wid = QtWidgets.QMainWindow()
    wid.setWindowTitle("Test")
    wid.show()

#     sys.exit(app.exec())
