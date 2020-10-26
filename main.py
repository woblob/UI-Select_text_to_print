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
# TODO: zmienic database etree -> Qtree (połączone z następnym) treeview
# TODO: update zmian drzewa edit -> select
# TODO: drukowanie
# TODO: które texty zaznaczyć aka profil domyślny
# TODO: jak drukowac, checkbox'y
# TODO: Autoload database
# TODO: wyciagnac drzewo edit i zrobic nowa klase
# TODO: zapis zmian przed wyjściem
# TODO: zmienic zapis do XML'a


class ConnectionBetweenTabs(QObject):
    Qtree = None
    database = et.ElementTree()
    send_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        ConnectionBetweenTabs.func()

    @classmethod
    def func(cls):
        cls.Qtree = cls.make_tree()

    @staticmethod
    def make_tree():
        treeWidget = QTreeWidget()

        treeWidget.setObjectName(u"treeWidget")
        treeWidget.setGeometry(QRect(0, 0, 500, 500))
        treeWidget.setUniformRowHeights(True)

        elements_column = QTreeWidgetItem()
        elements_column.setTextAlignment(0, Qt.AlignCenter)
        elements_column.setText(0, "Pliki")
        elements_column.setText(1, "Treść")

        treeWidget.setHeaderItem(elements_column)

        header = treeWidget.header()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        # header.hideSection(1)
        # header.showSection(1)

        column = 0

        for i in range(2):
            treeitem_1 = QTreeWidgetItem(treeWidget)
            treeitem_1.setText(column, f"Rodzaj{i}")
            treeitem_1.setCheckState(Qt.Unchecked, column)
            for j in range(2):
                treeitem_2 = QTreeWidgetItem(treeitem_1)
                treeitem_2.setText(column, f"Rodzaj{i}_{j}")
                treeitem_2.setCheckState(Qt.Unchecked, column)
                for k in range(2):
                    treeitem_3 = QTreeWidgetItem(treeitem_2)
                    treeitem_3.setText(column, f"Rodzaj{i}_{j}_{k}")
                    treeitem_3.setCheckState(Qt.Unchecked, column)

        return treeWidget


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

        self.tab_bar.currentChanged.connect(self.on_change_tab)

        main_h_box = QHBoxLayout()
        main_h_box.addWidget(self.tab_bar)
        # main_h_box.setAlignment(Qt.AlignCenter)
        self.setLayout(main_h_box)

    def on_change_tab(self):
        print(self.tab_bar.currentIndex())

if __name__ == "__main__":
    app = QApplication([])
    screen = Window()
    sys.exit(app.exec_())