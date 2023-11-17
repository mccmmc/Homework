import sys
import sqlite3

from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget

from UI.main_ui import Ui_MainWindow
from UI.addEditCoffeeForm import Ui_Form


class Suprematism(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.settings = None
        self.data_base = r'data\coffee.sqlite'

        self.setupUi(self)

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Coffees')

        self.CoffeTable.clicked.connect(self.change)
        self.AddButthon.clicked.connect(self.change)
        self.show_db()

    def show_db(self):
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(self.data_base)
        db.open()

        model = QSqlTableModel(self, db)
        model.setTable('coffees')
        model.select()

        self.CoffeTable.setModel(model)

    def change(self, index):
        try:
            row = self.sender().text()
        except AttributeError:
            row = index.row()
        self.settings = Settings(row, self)
        self.settings.show()


class Settings(QWidget, Ui_Form):
    def __init__(self, index, parent):
        super().__init__()
        self.setupUi(self)

        self.index = index
        self.parent = parent

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Settings')
        self.ConfirmButton.clicked.connect(self.edit)

    def edit(self):
        variety = self.Varienty.text()
        degree = self.Degree.text()
        ground_grains = self.Ground_grains.text()
        description = self.Description.text()
        price = self.Price.text()
        volume = self.Volume.text()

        conn = sqlite3.connect(self.parent.data_base)
        cursor = conn.cursor()

        try:
            cursor.execute(f"""UPDATE coffees
                                                    SET "variety "      = '{variety}',
                                                        degree          = '{degree}',
                                                        "ground/grains" = '{ground_grains}',
                                                        description     = '{description}',
                                                        price           = '{price}',
                                                        volume          = '{volume}'
                                                    WHERE ID = '{self.index + 1}'""")

        except TypeError:
            cursor.execute(f"""INSERT OR IGNORE INTO coffees("variety ", degree, 
            "ground/grains", description, price, volume)
                                                    VALUES ('{variety}', '{degree}', '{ground_grains}', 
                                                    '{description}', '{price}', '{volume}');""")

        conn.commit()
        self.parent.show_db()
        self.close()


def except_hooks(cls, exception, traceback):
    sys.excepthook(cls, exception, traceback)


if __name__ == '__main__':
    sys.excepthook = except_hooks
    app = QApplication(sys.argv)
    ex = Suprematism()
    ex.show()
    sys.exit(app.exec())
