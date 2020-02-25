import json
from pyjsonq import JsonQ
from gui_file.v0 import MyForm
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtSql import *

# qe = JsonQ('json_file\info.json')
# res = qe.at('Matricole').where('Codice', '=', '138').get()
# print(res)
# qe = JsonQ("json_file\data.json").at("users").where("id", "<", 3).get()
#
# qe = JsonQ("json_file\data.json").at('users.0.visits').where('year', '=', 2011).get()
# print("result", qe)
#
# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     Form = QtWidgets.QWidget()
#     ui = MyForm()
#     ui.setupUi(Form)
#     Form.show()
#     sys.exit(app.exec_())


# with open('json_file\info.json', 'r') as f:
#     distro = json.load(f)
#
# print(json.dumps(distro, indent=6))
#
# list_values = [ v for v in distro.values() ]
# print(type(distro.keys()))
# print(distro["Name"])

def my_decorator(func):
    def wrapper():
        print("Something is happening before the function is called.")
        func()
        print("Something is happening after the function is called.")
    return wrapper

def say_whee():
    print("Whee!")

say_whee = my_decorator(say_whee)

say_whee()

