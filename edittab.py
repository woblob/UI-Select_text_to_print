from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import sip
from lxml import etree as et
import datetime


class EditTab(QWidget):
    def __init__(self, link):
        super().__init__()

        self.helper_counter = 0
        self.currently_selected_tree_item = None
        self.add_subitem_button = None
        self.edit_button = None
        self.remove_button = None
        self.database = link.database
        self.signal = link.send_signal
        self.tree_q = link.Qtree
        self.file_dialog = CustomFileDialog()

        self.initialize_tab()

    def initialize_tab(self):
        edit_tab = QVBoxLayout()

        buttons_groupbox = self.initialize_edit_button_boxes()
        tree_groupbox = self.make_edit_tree()
        IO_buttons_groupbox = self.initialize_IO_button_box()

        edit_tab.addWidget(buttons_groupbox)
        edit_tab.addWidget(tree_groupbox)
        edit_tab.addWidget(IO_buttons_groupbox)

        self.setLayout(edit_tab)

    def initialize_edit_button_boxes(self):
        hbox = QHBoxLayout()
        add_item_button = QPushButton("Dodaj Element")
        add_subitem_button = QPushButton("Dodaj podElement")
        # edit_button = QPushButton("Edytuj")
        remove_button = QPushButton("Usuń")

        add_subitem_button.setDisabled(True)
        # edit_button.setDisabled(True)
        remove_button.setDisabled(True)

        add_item_button.clicked.connect(self.add_tree_item)
        add_subitem_button.clicked.connect(self.add_subitem_tree_item)
        # edit_button.clicked.connect(self.edit_tree_item)
        remove_button.clicked.connect(self.remove_tree_item)

        self.add_subitem_button = add_subitem_button
        # self.edit_button = edit_button
        self.remove_button = remove_button

        hbox.addWidget(add_item_button)
        hbox.addWidget(add_subitem_button)
        # hbox.addWidget(edit_button)
        hbox.addWidget(remove_button)

        groupbox = QGroupBox()
        groupbox.setLayout(hbox)
        return groupbox

    def make_edit_tree(self):


        tree_view = QTreeView()
        model =  QStandardItemModel()

        root = model.invisibleRootItem()

        self.populate_root()

        tree_view.setModel(model)


        print(tree_view.geometry())
        # tree_view.
        # tree_view.hideColumn()

        # self.tree_q.itemClicked.connect(self.select_item)
        # self.tree_q.itemDoubleClicked.connect(self.edit_tree_item)
        # self.tree_q.itemSelectionChanged.connect(self.update_tree_item_selection)

        # return self.tree_q
        return tree_view

    def populate_root(self):
        pass

    def add_tree_item(self):
        if self.currently_selected_tree_item is None:
            parent = self.tree_q
        else:
            parent = self.currently_selected_tree_item.parent()
            if parent is None:
                parent = self.tree_q

        new_item = QTreeWidgetItem(parent)
        new_item.setText(0, f"Element {self.helper_counter}")
        self.helper_counter += 1

    def add_subitem_tree_item(self):
        parent = self.currently_selected_tree_item
        parent.setExpanded(True)

        new_item = QTreeWidgetItem(parent)
        new_item.setText(0, f"Element {self.helper_counter}")
        self.helper_counter += 1

    # def edit_tree_item(self):
    #     # lol = QInputDialog
    #     # lol.setLayout()
    #     # lol.getMultiLineText(self, "Edycja Elementu", "Nazwa Elementu", "abaoaf")
    #     pass

    @pyqtSlot(QTreeWidgetItem, int)
    def edit_tree_item(self, item, column):
        tmp = item.flags()
        item.setFlags(tmp | Qt.ItemIsEditable)
        if tmp & Qt.ItemIsEditable:
            item.setFlags(tmp ^ Qt.ItemIsEditable)

    def remove_tree_item(self):
        item = self.currently_selected_tree_item
        self.currently_selected_tree_item = None
        sip.delete(item)

    @pyqtSlot(QTreeWidgetItem)
    def select_item(self, item):
        self.currently_selected_tree_item = item

    def update_tree_item_selection(self):
        items = self.tree_q.selectedItems()
        item_is_selected = items != []
        if item_is_selected:
            self.currently_selected_tree_item = items[0]
        else:
            self.currently_selected_tree_item = None

        self.add_subitem_button.setDisabled(not item_is_selected)
        # self.edit_button.setDisabled(not item_is_selected)
        self.remove_button.setDisabled(not item_is_selected)

    def initialize_IO_button_box(self):
        hbox = QHBoxLayout()
        save_button = QPushButton("Zapisz")
        load_button = QPushButton("Ładuj")

        # save_button.setDisabled(True)
        # load_button.setDisabled(True)

        save_button.clicked.connect(self.save_database)
        load_button.clicked.connect(self.load_database)

        hbox.addWidget(save_button)
        hbox.addWidget(load_button)

        groupbox = QGroupBox()
        groupbox.setLayout(hbox)
        return groupbox

    def save_database(self):
        filename = self.file_dialog.save()
        if not filename:
            return

        xml_tree = self.lxml_get_all_items()
        xml_tree.write(filename,
                       pretty_print=True,
                       xml_declaration=True,
                       encoding="utf-8")

        message = f"Zapisano plik {filename}"
        EditTab.display_message(message)

    @staticmethod
    def display_message(message):
        msgBox = QMessageBox()
        msgBox.setText(message)
        # msgbox_format = QTextCharFormat()
        # msgbox_format.setFontPointSize(20)
        # msgBox.setTextFormat(msgbox_format)
        msgBox.exec_()

    def lxml_get_subtree_nodes(self, tree_widget_item):
        name, inside = tree_widget_item.text(0), tree_widget_item.text(1)
        element = et.Element("Element", Name=name, Text=inside)
        for i in range(tree_widget_item.childCount()):
            child = tree_widget_item.child(i)
            subelement = self.lxml_get_subtree_nodes(child)
            element.append(subelement)
        return element

    def lxml_get_all_items(self):
        timestamp = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        root = et.Element("root", timestamp=timestamp)
        for i in range(self.tree_q.topLevelItemCount()):
            top_item = self.tree_q.topLevelItem(i)
            element = self.lxml_get_subtree_nodes(top_item)
            root.append(element)

        tree = et.ElementTree(root)
        return tree

    def load_database(self):
        filename = self.file_dialog.open()
        if not filename:
            return

        message = ''
        try:
            root = et.parse(filename).getroot()
        except et.XMLSyntaxError as e:
            message = f"Plik źle sformatowany.\n{e}"
        except OSError as e:
            message = f"Nie udało się otworzyć pliku.\n{e}"
        except BaseException as e:
            message = f"Nie obsługiwany błąd.\nError: {e}, {type(e)}"
        finally:
            if message:
                EditTab.display_message(message)
                return

        self.database._setroot(root)
        self.update_tree()
        self.signal.emit()

    def update_tree(self):
        self.tree_q.clear()

        def help_rec(xlm_tree, qroot):
            for child in xlm_tree.getroot():
                rec(child, qroot)

        def rec(elem, root):
            item = QTreeWidgetItem(root)
            item.setText(0, elem.get("Name"))
            item.setText(1, elem.get("Text"))
            for child in elem:
                rec(child, item)

        help_rec(self.database, self.tree_q)
        self.tree_q.expandAll()


class CustomFileDialog(QFileDialog):
    def __init__(self):
        super().__init__()

        self.filename = "database {}.xml"

        # self.setParent(parent, Qt.Widget)
        self.setViewMode(QFileDialog.List)
        self.setNameFilter("XML Files (*.xml)")
        self.setDirectory(QDir.currentPath())
        self.setLabelText(QFileDialog.Reject, "Anuluj")
        self.setLabelText(QFileDialog.LookIn, "Foldery")
        self.setLabelText(QFileDialog.FileType, "Format pliku")
        self.setLabelText(QFileDialog.FileName, "Nazwa pliku")
        self.setWindowModality(Qt.ApplicationModal)

        options = self.Options()
        options |= self.DontUseNativeDialog
        self.setOptions(options)

    def save(self):
        time_format = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        default_filename = self.filename.format(time_format)

        self.setFileMode(QFileDialog.AnyFile)
        self.setWindowTitle("Zapisz baze danych")
        self.setLabelText(QFileDialog.Accept, "Zapisz")
        self.selectFile(default_filename)
        self.setAcceptMode(QFileDialog.AcceptSave)

        filename = ""
        if self.exec_():
            filename = self.selectedFiles()[0]

        return filename

    def open(self):
        self.setFileMode(QFileDialog.ExistingFile)
        self.setWindowTitle("Załaduj baze danych")
        self.setLabelText(QFileDialog.Accept, "Otwórz")

        filename = ""
        if self.exec_():
            filename = self.selectedFiles()[0]

        return filename