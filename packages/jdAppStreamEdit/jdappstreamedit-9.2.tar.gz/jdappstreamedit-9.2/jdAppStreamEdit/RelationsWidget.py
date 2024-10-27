from PyQt6.QtWidgets import QWidget, QComboBox, QLineEdit, QTableWidget, QTableWidgetItem, QPushButton, QHeaderView
from .Functions import select_combo_box_data, is_string_number, get_logical_table_row_list, clear_table_widget
from .ui_compiled.RelationsWidget import Ui_RelationsWidget
from typing import Optional, List, TYPE_CHECKING
from PyQt6.QtCore import QCoreApplication
from PyQt6.QtGui import QIntValidator
from lxml import etree
import sys


if TYPE_CHECKING:
    from .MainWindow import MainWindow


class RelationsWidget(QWidget, Ui_RelationsWidget):
    def __init__(self, main_window: "MainWindow") -> None:
        super().__init__()

        self.setupUi(self)

        self._main_window = main_window

        for key, value in vars(self).items():
            if key.startswith("edit_screen_custom_") or key.startswith("edit_internet_bandwidth_"):
                value.setValidator(QIntValidator())
            elif key.startswith("box_internet_"):
                value.addItem(QCoreApplication.translate("RelationsWidget", "Not specified"), "none")
                value.addItem(QCoreApplication.translate("RelationsWidget", "Never uses the internet, even if it’s available"), "offline-only")
                value.addItem(QCoreApplication.translate("RelationsWidget", "Uses the internet only the first time the application is run"), "first-run")
                value.addItem(QCoreApplication.translate("RelationsWidget", "Needs internet connectivity to work"), "always")

            if isinstance(value, QComboBox):
                value.currentIndexChanged.connect(main_window.set_file_edited)
            elif isinstance(value, QLineEdit):
                value.textEdited.connect(main_window.set_file_edited)

        self.edit_memory_requires.setValidator(QIntValidator())
        self.edit_memory_recommends.setValidator(QIntValidator())

        self.modalias_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.hardware_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

        self.modalias_table.verticalHeader().setSectionsMovable(True)
        self.hardware_table.verticalHeader().setSectionsMovable(True)

        self.button_modalias_add.clicked.connect(self._add_modalias_row)
        self.button_hardware_add.clicked.connect(self._add_hardware_row)

        self._update_internet_bandwith_enabled()

        self.main_tab_widget.setCurrentIndex(0)

    # Screen

    def _load_screen_data(self, tag_list: List[etree.Element], relation: str) -> None:
        for i in tag_list:
            size = i.get("compare")
            if size is None:
                size = "ge"
            if size not in ("ge", "le"):
                print("Unsupported compare attribute " + size, file=sys.stderr)
                continue
            append_string = size + "_" + relation
            if is_string_number(i.text):
                getattr(self, "edit_screen_custom_" + append_string).setText(i.text)
            elif i.text == "xsmall":
                getattr(self, "edit_screen_custom_" + append_string).setText("360")
            elif i.text == "small":
                getattr(self, "edit_screen_custom_" + append_string).setText("420")
            elif i.text == "medium":
                getattr(self, "edit_screen_custom_" + append_string).setText("760")
            elif i.text == "large":
                getattr(self, "edit_screen_custom_" + append_string).setText("900")
            elif i.text == "xlarge":
                getattr(self, "edit_screen_custom_" + append_string).setText("1200")

    def _get_screen_save_data(self, parent_tag: etree.Element, relation: str) -> None:
        for size in ("ge", "le"):
            append_string = size + "_" + relation
            if getattr(self, "edit_screen_custom_" + append_string).text() != "":
                display_tag = etree.SubElement(parent_tag, "display_length")
                display_tag.set("compare", size)
                display_tag.text = getattr(self, "edit_screen_custom_" + append_string).text()

    # Internet

    def _update_internet_bandwith_enabled(self) -> None:
        for relation in ("supports", "requires", "recommends"):
            value = getattr(self, f"box_internet_{relation}").currentData()
            enabled = value in ("first-run", "always")
            getattr(self, f"label_internet_bandwidth_{relation}").setEnabled(enabled)
            getattr(self, f"edit_internet_bandwidth_{relation}").setEnabled(enabled)
            getattr(self, f"label_internet_mbit_{relation}").setEnabled(enabled)

    # Modalias

    def _add_modalias_row(self, relation: Optional[str] = None, chid: Optional[str] = None) -> None:
        row = self.modalias_table.rowCount()
        self.modalias_table.insertRow(row)

        relation_box = QComboBox()
        relation_box.addItem(QCoreApplication.translate("RelationsWidget", "Supported"), "supports")
        relation_box.addItem(QCoreApplication.translate("RelationsWidget", "Recommend"), "recommends")
        relation_box.addItem(QCoreApplication.translate("RelationsWidget", "Required"), "requires")
        if relation is not None:
            select_combo_box_data(relation_box, relation)
        relation_box.currentIndexChanged.connect(self._main_window.set_file_edited)
        self.modalias_table.setCellWidget(row, 0, relation_box)

        item = QTableWidgetItem()
        if chid is not None:
            item.setText(chid)
        self.modalias_table.setItem(row, 1, item)

        remove_button = QPushButton(QCoreApplication.translate("RelationsWidget", "Remove"))
        remove_button.clicked.connect(self._remove_modalias_clicked)
        self.modalias_table.setCellWidget(row, 2, remove_button)

        self._main_window.set_file_edited()

    def _remove_modalias_clicked(self) -> None:
        for i in range(self.modalias_table.rowCount()):
            if self.modalias_table.cellWidget(i, 2) == self.sender():
                self.modalias_table.removeRow(i)
                self._main_window.set_file_edited()
                return

    # Hardware

    def _add_hardware_row(self, relation: Optional[str] = None, chid: Optional[str] = None) -> None:
        row = self.hardware_table.rowCount()
        self.hardware_table.insertRow(row)

        relation_box = QComboBox()
        relation_box.addItem(QCoreApplication.translate("RelationsWidget", "Supported"), "supports")
        relation_box.addItem(QCoreApplication.translate("RelationsWidget", "Recommend"), "recommends")
        relation_box.addItem(QCoreApplication.translate("RelationsWidget", "Required"), "requires")
        if relation is not None:
            select_combo_box_data(relation_box, relation)
        relation_box.currentIndexChanged.connect(self._main_window.set_file_edited)
        self.hardware_table.setCellWidget(row, 0, relation_box)

        item = QTableWidgetItem()
        if chid is not None:
            item.setText(chid)
        self.hardware_table.setItem(row, 1, item)

        remove_button = QPushButton(QCoreApplication.translate("RelationsWidget", "Remove"))
        remove_button.clicked.connect(self._remove_hardware_clicked)
        self.hardware_table.setCellWidget(row, 2, remove_button)

        self._main_window.set_file_edited()

    def _remove_hardware_clicked(self) -> None:
        for i in range(self.hardware_table.rowCount()):
            if self.hardware_table.cellWidget(i, 2) == self.sender():
                self.hardware_table.removeRow(i)
                self._main_window.set_file_edited()
                return

    def reset_data(self) -> None:
        for key, value in vars(self).items():
            if key.startswith("rad_screen_device_class_"):
                value.setChecked(True)
            elif isinstance(value, QComboBox):
                value.setCurrentIndex(0)
            elif isinstance(value, QLineEdit):
                value.setText("")
            elif isinstance(value, QTableWidget):
                clear_table_widget(value)

    def load_data(self, relation_tag: etree.Element) -> None:
        self._load_screen_data(relation_tag.findall("display_length"), relation_tag.tag)

        memory_tag = relation_tag.find("memory")
        if memory_tag is not None:
            if relation_tag.tag == "requires":
                self.edit_memory_requires.setText(memory_tag.text)
            elif relation_tag.tag == "recommends":
                self.edit_memory_recommends.setText(memory_tag.text)
            else:
                print("memory tag is only allowd in requires and recommends", file=sys.stderr)

        internet_tag = relation_tag.find("internet")
        if internet_tag is not None:
            select_combo_box_data(getattr(self, f"box_internet_{relation_tag.tag}"), internet_tag.text)
            if "bandwidth_mbitps" in internet_tag.attrib and internet_tag.text in ("first-run", "always"):
                getattr(self, f"edit_internet_bandwidth_{relation_tag.tag}").setText(internet_tag.get("bandwidth_mbitps"))

        for i in relation_tag.findall("modalias"):
            self._add_modalias_row(relation=relation_tag.tag, chid=i.text)

        for i in relation_tag.findall("hardware"):
            self._add_hardware_row(relation=relation_tag.tag, chid=i.text)

    def get_save_data(self, parent_tag: etree.Element, relation: str) -> None:
        if relation == "requires" or relation == "recommends":
            self._get_screen_save_data(parent_tag, relation)

        if relation == "requires" and self.edit_memory_requires.text() != "":
            memory_tag = etree.SubElement(parent_tag, "memory")
            memory_tag.text = self.edit_memory_requires.text()
        elif relation == "recommends" and self.edit_memory_recommends.text() != "":
            memory_tag = etree.SubElement(parent_tag, "memory")
            memory_tag.text = self.edit_memory_recommends.text()

        internet_value = getattr(self, f"box_internet_{relation}").currentData()
        if internet_value != "none":
            internet_tag = etree.SubElement(parent_tag, "internet")
            internet_tag.text = internet_value
            if internet_value in ("first-run", "always"):
                bandwidth = getattr(self, f"edit_internet_bandwidth_{relation}").text()
                if bandwidth != "":
                    internet_tag.set("bandwidth_mbitps", bandwidth)

        for i in get_logical_table_row_list(self.modalias_table):
            if self.modalias_table.cellWidget(i, 0).currentData() == relation:
                modalias_tag = etree.SubElement(parent_tag, "modalias")
                modalias_tag.text = self.modalias_table.item(i, 1).text().strip()

        for i in get_logical_table_row_list(self.hardware_table):
            if self.hardware_table.cellWidget(i, 0).currentData() == relation:
                hardware_tag = etree.SubElement(parent_tag, "hardware")
                hardware_tag.text = self.hardware_table.item(i, 1).text().strip()
