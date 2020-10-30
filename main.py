from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import lxml.etree as et
from selecttab import SelectTab
from edittab import EditTab

# Edycja elementu: zrobione jako klikanie
# zebranie info co drukowac: zrobione
# zapis do pliku: zrobione
# potwierdzenie zapisu: zrobione
# zaladowanie pliku do edit: zrobione
# zaladowanie pliku do select: zrobione
# wyswietlenie drzewa edit: zrobione
# wyswietlenie drzewa select, sygnal: zrobione
# zmienic database etree -> Qtree (połączone z następnym) treeview: zrobione
# update zmian drzewa edit -> select: zrobione
# zmiana aplikacji na bardziej elastyczną: zrobione
# drukowanie: zrobione
# jak drukowac, checkbox'y/ checkAll: zrobione
# TODO: które texty zaznaczyć aka profil domyślny
# TODO: jak drukowac, checkbox'y/ printAll
# TODO: Autoload database
# TODO: wyciagnac drzewo edit i zrobic nowa klase
# TODO: zapis zmian przed wyjściem
# TODO: ?zmienic zapis do XML'a
# TODO: ?ładne drukowanie


class ConnectionBetweenTabs(QObject):
    database = et.ElementTree()
    send_signal = pyqtSignal()
    tree_model = QStandardItemModel()
    tree_model.setObjectName(u"treeModel")
    tree_model.setColumnCount(2)
    tree_model.setHorizontalHeaderItem(0, QStandardItem("Name"))
    tree_model.setHorizontalHeaderItem(1, QStandardItem("Text"))


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.link = ConnectionBetweenTabs()

        self.initializeWindow()
        self.combine_tabs()
        self.show()

    def initializeWindow(self):
        self.setWindowTitle(QCoreApplication.translate("Okienko", u"Okienko"))
        self.setGeometry(QRect(100, 100, 520, 640))

    def combine_tabs(self):
        self.tab_bar = QTabWidget()

        self.select_tab = SelectTab(self.link)
        self.edit_tab = EditTab(self.link)

        self.tab_bar.addTab(self.select_tab, "Wybór tekstów")
        self.tab_bar.addTab(self.edit_tab, "Edycja tekstów")

        main_h_box = QHBoxLayout()
        main_h_box.addWidget(self.tab_bar)
        self.setLayout(main_h_box)


if __name__ == "__main__":
    app = QApplication([])
    screen = Window()
    sys.exit(app.exec_())