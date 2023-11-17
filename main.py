import sys

from PyQt5 import uic
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import QMainWindow, QApplication


class Suprematism(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Coffees')
        self.show_db()

    def show_db(self):
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('coffee.sqlite')
        db.open()

        model = QSqlTableModel(self, db)
        model.setTable('coffees')
        model.select()

        self.CoffeTable.setModel(model)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Suprematism()
    ex.show()
    sys.exit(app.exec())
