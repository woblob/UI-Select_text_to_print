from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
# import lxml.etree as et

class SelectTab(QWidget):
    def __init__(self, link):
        super().__init__()

        self.tree = None
        self.database = link.database
        self.tree_q = link.Qtree
        self.signal = link.send_signal
        # self.signal.connect(self.update_tree)
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
        files = self.gather_files_from_tree()
        self.print_docx(files)

    def gather_files_from_tree(self):
        lst = []
        for item in self.iter_tree():
            if item.childCount() == 0:
               lst.append(item.text(1))
        return lst

    def print_docx(self, file_list):
        print(file_list)

    def iter_tree(self, flags=QTreeWidgetItemIterator.Checked):
        iterator = QTreeWidgetItemIterator(self.tree_q, flags=flags)
        while iterator.value():
            item = iterator.value()
            yield item
            iterator += 1


    def make_select_tree_widget(self):
        # treeWidget = QTreeWidget()
        #
        # treeWidget.setObjectName(u"treeWidget")
        # treeWidget.setGeometry(QRect(0, 0, 500, 500))
        # treeWidget.setUniformRowHeights(True)
        #
        # Elements_column = QTreeWidgetItem()
        # Elements_column.setTextAlignment(0, Qt.AlignCenter)
        # Elements_column.setText(0, "Elements")
        # Elements_column.setText(1, "Treść")
        #
        # treeWidget.setHeaderItem(Elements_column)

        # header = self.tree_q.header()
        # # header.setSectionResizeMode(QHeaderView.ResizeToContents)
        # header.hideSection(1)

        # column = 0
        #
        # for i in range(2):
        #     treeitem_1 = QTreeWidgetItem(treeWidget)
        #     treeitem_1.setText(column, f"Rodzaj{i}")
        #     treeitem_1.setCheckState(Qt.Unchecked, column)
        #     for j in range(2):
        #         treeitem_2 = QTreeWidgetItem(treeitem_1)
        #         treeitem_2.setText(column, f"Rodzaj{i}_{j}")
        #         treeitem_2.setCheckState(Qt.Unchecked, column)
        #         for k in range(2):
        #             treeitem_3 = QTreeWidgetItem(treeitem_2)
        #             treeitem_3.setText(column, f"Rodzaj{i}_{j}_{k}")
        #             treeitem_3.setCheckState(Qt.Unchecked, column)
        #
        # self.tree = treeWidget
        # self.tree_q.itemClicked.connect(self.on_item_clicked)

        # treeWidget.expandAll()
        tree_view = QTreeView(self.tree_q)
        return tree_view

        # return self.tree_q

    @pyqtSlot(QTreeWidgetItem, int)
    def on_item_clicked(self, it, col):
        if it.checkState(col) == Qt.Checked:
            self.check_all_descendants(it)
            self.update_all_ancestors_Checked(it)
        elif it.checkState(col) == Qt.Unchecked:
            self.uncheck_all_descendants(it)
            self.update_all_ancestors_Unhecked(it)

    def update_all_ancestors_Checked(self, item):
        parent = item.parent()
        if parent is None:
            return

        col = 0
        tristate = 1
        for child in SelectTab.children_of_(parent):
            if not child.checkState(col) == Qt.Checked:
                parent.setCheckState(col, tristate)
                self.update_all_ancestors_Checked(parent)
                break
        else:
            parent.setCheckState(col, Qt.Checked)
            self.update_all_ancestors_Checked(parent)

    def update_all_ancestors_Unhecked(self, item):
        parent = item.parent()
        if parent is None:
            return

        col = 0
        tristate = 1
        for child in SelectTab.children_of_(parent):
            if not child.checkState(col) == Qt.Unchecked:
                parent.setCheckState(col, tristate)
                self.update_all_ancestors_Unhecked(parent)
                break
        else:
            parent.setCheckState(col, Qt.Unchecked)
            self.update_all_ancestors_Unhecked(parent)

    @staticmethod
    def top_children_of_(tree):
        for index in range(tree.topLevelItemCount()):
            child = tree.topLevelItem(index)
            yield child

    @staticmethod
    def children_of_(item):
        for index in range(item.childCount()):
            child = item.child(index)
            yield child

    def check_all_descendants(self, item):
        for child in SelectTab.children_of_(item):
            if not child.checkState(0) == Qt.Checked:
                child.setCheckState(0, Qt.Checked)
                self.check_all_descendants(child)

    def uncheck_all_descendants(self, item):
        for child in SelectTab.children_of_(item):
            if not child.checkState(0) == Qt.Unchecked:
                child.setCheckState(0, Qt.Unchecked)
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

    # def update_tree(self):
    #     self.tree_q.clear()
    #
    #     def help_rec(xlm_tree, qroot):
    #         for child in xlm_tree.getroot():
    #             rec(child, qroot)
    #
    #     def rec(elem, root):
    #         item = QTreeWidgetItem(root)
    #
    #         name_column = (0, elem.get("Name"))
    #         item.setText(*name_column)
    #         item.setCheckState(Qt.Unchecked, 0)
    #
    #         text_column = (1, elem.get("Text"))
    #         item.setText(*text_column)
    #
    #         for child in elem:
    #             rec(child, item)
    #
    #     help_rec(self.database, self.tree)
    #     self.tree.expandAll()