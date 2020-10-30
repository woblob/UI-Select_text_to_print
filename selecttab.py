from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys

class SelectTab(QWidget):
    def __init__(self, link):
        super().__init__()

        self.database = link.database
        self.tree_model = link.tree_model
        self.signal = link.send_signal
        self.tree_view = None
        self.signal.connect(self.update_tree)

        self.do_nothing = lambda: None

        self.initializeTab()

    def initializeTab(self):
        select_tab = QVBoxLayout()

        print_groupbox = self.initialize_print_box()
        tree_groupbox = self.make_select_tree_widget()
        buttons_groupbox = self.initialize_select_button_box()

        select_tab.addWidget(print_groupbox)
        select_tab.addWidget(tree_groupbox)
        select_tab.addWidget(buttons_groupbox)

        self.setLayout(select_tab)

    def initialize_print_box(self):
        hbox = QHBoxLayout()

        checkboxes = self.initialize_check_boxes()
        export_button = QPushButton("Eksportuj jako docx")
        export_button.clicked.connect(self.export_tree_as_docx)
        # export_button.setDisabled(True)

        hbox.addWidget(checkboxes)
        hbox.addWidget(export_button)

        print_box = QGroupBox()
        print_box.setLayout(hbox)
        return print_box

    def initialize_check_boxes(self):
        vbox = QVBoxLayout()
        checkbox1 = QCheckBox("checkbox 1")
        checkbox1.setChecked(True)
        checkbox2 = QCheckBox("checkbox 2")

        vbox.addWidget(checkbox1)
        vbox.addWidget(checkbox2)

        groupbox = QGroupBox()
        groupbox.setLayout(vbox)
        return groupbox

    def export_tree_as_docx(self):
        root = self.tree_model.invisibleRootItem()
        files = SelectTab.gather_files_from_tree(root)
        self.print_docx(files)

    def print_docx(self, file_list):
        print(len(file_list))
        print(file_list)

    @staticmethod
    def gather_files_from_tree(root):
        def children_of_(item):
            for index in range(item.rowCount()):
                name_col = item.child(index, 0)
                text_col = item.child(index, 1)
                yield name_col, text_col

        tristate = 1
        lst = []
        for name_item, text_item in children_of_(root):
            state = name_item.checkState()
            isChecked = state == Qt.Checked or \
                        state == tristate
            if isChecked:
                if name_item.hasChildren():
                    items = SelectTab.gather_files_from_tree(name_item)
                    lst.extend(items)
                else:
                    lst.append(text_item.text())
        return lst

    def make_select_tree_widget(self):
        tree_view = QTreeView()
        tree_view.setModel(self.tree_model)
        tree_view.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        tree_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        tree_view.hideColumn(1)
        tree_view.setHeaderHidden(True)
        tree_view.clicked.connect(self.on_item_clicked)
        self.tree_view = tree_view
        return tree_view

    def update_tree(self):
        self.tree_view.hideColumn(1)
        self.tree_view.expandAll()
        self.tree_view.setHeaderHidden(True)

    def on_item_clicked(self, index):
        item = self.tree_model.itemFromIndex(index)
        if item.checkState() == Qt.Checked:
            self.check_all_descendants(item)
            self.update_all_ancestors_Checked(item)
        elif item.checkState() == Qt.Unchecked:
            self.uncheck_all_descendants(item)
            self.update_all_ancestors_Unhecked(item)
            pass

    def update_all_ancestors_Checked(self, item):
        parent = item.parent()
        if parent is None:
            return

        tristate = 1
        for child in SelectTab.children_of_(parent):
            if not child.checkState() == Qt.Checked:
                parent.setCheckState(tristate)
                self.update_all_ancestors_Checked(parent)
                break
        else:
            parent.setCheckState(Qt.Checked)
            self.update_all_ancestors_Checked(parent)

    def update_all_ancestors_Unhecked(self, item):
        parent = item.parent()
        if parent is None:
            return

        tristate = 1
        for child in SelectTab.children_of_(parent):
            if not child.checkState() == Qt.Unchecked:
                parent.setCheckState(tristate)
                self.update_all_ancestors_Unhecked(parent)
                break
        else:
            parent.setCheckState(Qt.Unchecked)
            self.update_all_ancestors_Unhecked(parent)

    @staticmethod
    def children_of_(item):
        for index in range(item.rowCount()):
            child = item.child(index, 0)
            yield child

    def check_all_descendants(self, item):
        for child in SelectTab.children_of_(item):
            if not child.checkState() == Qt.Checked:
                child.setCheckState(Qt.Checked)
                self.check_all_descendants(child)

    def uncheck_all_descendants(self, item):
        for child in SelectTab.children_of_(item):
            if not child.checkState() == Qt.Unchecked:
                child.setCheckState(Qt.Unchecked)
                self.uncheck_all_descendants(child)

    def initialize_select_button_box(self):
        buttonBox = QDialogButtonBox()
        buttonBox.setObjectName(u"buttonBox")
        buttonBox.setOrientation(Qt.Horizontal)
        buttonBox.setStandardButtons(
            QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        # buttonBox.accepted.connect(self.update_tree)
        # buttonBox.accepted.connect(self.gather_files_from_tree)

        buttonBox.rejected.connect(sys.exit)
        return buttonBox

    def checkbox_summary(self):
        selected = []

        for checkbox in self.checkboxes:
            if checkbox.isChecked():
                selected.append(checkbox.text())

        print(" - ".join(selected))
