from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from lxml import etree as et
import datetime


class NameItem(QStandardItem):
    def __init__(self, txt):
        super().__init__()
        self.setEditable(True)
        self.setText(txt)
        self.setCheckState(Qt.Unchecked)
        self.setCheckable(True)
        # self.setAutoTristate(True)


class TextItem(QStandardItem):
    def __init__(self, txt=''):
        super().__init__()
        self.setEditable(True)
        self.setText(txt)


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
        self.tree_model = link.tree_model
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
        remove_button = QPushButton("Usuń")

        add_subitem_button.setDisabled(True)
        remove_button.setDisabled(True)

        add_item_button.clicked.connect(self.add_tree_item)
        add_subitem_button.clicked.connect(self.add_subitem_tree_item)
        remove_button.clicked.connect(self.remove_tree_item)

        self.add_subitem_button = add_subitem_button
        self.remove_button = remove_button

        hbox.addWidget(add_item_button)
        hbox.addWidget(add_subitem_button)
        hbox.addWidget(remove_button)

        groupbox = QGroupBox()
        groupbox.setLayout(hbox)
        return groupbox

    def make_edit_tree(self):
        tree_view = QTreeView()
        tree_view.setModel(self.tree_model)
        tree_view.setAlternatingRowColors(True)
        tree_view.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        # tree_view.clicked.connect(self.select_item)
        tree_view.selectionModel().selectionChanged.connect(self.update_tree_item_selection)

        self.tree_view = tree_view
        return tree_view

    def add_tree_item(self):
        if self.currently_selected_tree_item is None:
            parent = self.tree_model
        else:
            parent = self.currently_selected_tree_item.parent()
            if parent is None:
                parent = self.tree_model

        self.make_dummy_tree_item(parent)

    def make_dummy_tree_item(self, parent):
        new_item = NameItem(f"Element {self.helper_counter}")
        text_item = TextItem()
        parent.appendRow([new_item, text_item])
        self.helper_counter += 1

    def add_subitem_tree_item(self):
        parent = self.currently_selected_tree_item
        parent_index = parent.index()
        self.make_dummy_tree_item(parent)
        self.tree_view.expand(parent_index)

    def remove_tree_item(self):
        a = self.tree_view.selectionModel().currentIndex()
        p_index = a.parent()
        parent = self.tree_model.itemFromIndex(p_index) or self.tree_model
        parent.removeRow(a.row())

    # def select_item(self, item):
    #     self.currently_selected_tree_item = item

    def update_tree_item_selection(self, current, prev):
        indexes = current.indexes()
        disabled = True
        if indexes == []:
            self.currently_selected_tree_item = None
        else:
            nameindex, _ = indexes
            nameitem = self.tree_model.itemFromIndex(nameindex)
            print(f"update_tree_item_selection {nameitem}")  # , {textitem}")
            self.currently_selected_tree_item = nameitem
            disabled = False

        self.add_subitem_button.setDisabled(disabled)
        self.remove_button.setDisabled(disabled)

    def initialize_IO_button_box(self):
        hbox = QHBoxLayout()
        save_button = QPushButton("Zapisz")
        load_button = QPushButton("Ładuj")

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

    def lxml_get_all_items(self):
        def recursave(tree_node, root):
            for i in range(tree_node.rowCount()):
                name_node = tree_node.item(i, 0)
                name = name_node.text()
                text = tree_node.item(i, 1).text()
                element = et.SubElement(root, "Element", Name=name, Text=text)
                help_recursave(name_node, element)

        def help_recursave(tree_node, root):
            for i in range(tree_node.rowCount()):
                name_node = tree_node.child(i, 0)
                name = name_node.text()
                text = tree_node.child(i, 1).text()
                element = et.SubElement(root, "Element", Name=name, Text=text)
                help_recursave(name_node, element)

        timestamp = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        root = et.Element("root", timestamp=timestamp)
        recursave(self.tree_model, root)
        print(et.tostring(root))

        tree = et.ElementTree(root)
        return tree

    # def lxml_get_all_items2(self):
    #     def recursave(tree_node, root):
    #         for i in range(tree_node.rowCount()):
    #             name_node = tree_node.item(i, 0)
    #             name = name_node.text()
    #             text = tree_node.item(i, 1).text()
    #             element = et.SubElement(root, "Element")
    #             name_elem = et.SubElement(element, "Name")
    #             name_elem.text = name
    #             text_elem = et.SubElement(element, "Text")
    #             text_elem.text = text
    #             help_recursave(name_node, element)
    #
    #     def help_recursave(tree_node, root):
    #         for i in range(tree_node.rowCount()):
    #             name_node = tree_node.child(i)
    #             name = name_node.text()
    #             text = tree_node.child(i, 1).text()
    #             element = et.SubElement(root, "Element")
    #             name_elem = et.SubElement(element, "Name")
    #             name_elem.text = name
    #             text_elem = et.SubElement(element, "Text")
    #             text_elem.text = text
    #             help_recursave(name_node, element)
    #
    #     timestamp = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    #     root = et.Element("root", timestamp=timestamp)
    #     recursave(self.tree_model, root)
    #     print(et.tostring(root))
    #
    #     tree = et.ElementTree(root)
    #     return tree

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
        column_name0 = self.tree_model.headerData(0, Qt.Horizontal)
        column_name1 = self.tree_model.headerData(1, Qt.Horizontal)
        self.tree_model.clear()

        def help_rec(xlm_tree, qroot):
            for child in xlm_tree.getroot():
                n, t = rec(child)
                qroot.appendRow([n, t])

        def rec(elem):
            name = elem.get("Name")
            text = elem.get("Text")
            NAME, TEXT = NameItem(name), TextItem(text)
            for child in elem:
                n, t = rec(child)
                NAME.appendRow([n, t])
            return NAME, TEXT

        help_rec(self.database, self.tree_model)
        self.tree_view.expandAll()
        self.tree_model.setHorizontalHeaderItem(0, QStandardItem(column_name0))
        self.tree_model.setHorizontalHeaderItem(1, QStandardItem(column_name1))
        self.currently_selected_tree_item = None


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