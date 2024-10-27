from .Functions import stretch_table_widget_colums_size, select_combo_box_data, get_logical_table_row_list, clear_table_widget, list_widget_contains_item, get_sender_table_row, set_layout_enabled
from PyQt6.QtWidgets import QWidget, QComboBox, QTableWidgetItem, QInputDialog, QMessageBox, QPushButton, QColorDialog
from .ui_compiled.AdvancedWidget import Ui_AdvancedWidget
from typing import Optional, TYPE_CHECKING
from PyQt6.QtCore import QCoreApplication
from PyQt6.QtGui import QColor
from lxml import etree
import traceback
import sys
import re


if TYPE_CHECKING:
    from .MainWindow import MainWindow


class AdvancedWidget(QWidget, Ui_AdvancedWidget):
    def __init__(self, main_window: "MainWindow") -> None:
        super().__init__()

        self.setupUi(self)

        self._main_window = main_window

        stretch_table_widget_colums_size(self.translation_table)
        stretch_table_widget_colums_size(self.tags_table)
        stretch_table_widget_colums_size(self.custom_table)

        self.translation_table.verticalHeader().setSectionsMovable(True)
        self.tags_table.verticalHeader().setSectionsMovable(True)
        self.custom_table.verticalHeader().setSectionsMovable(True)

        self._update_suggests_edit_remove_button()
        self._update_replaces_edit_remove_button()

        self.translation_table.verticalHeader().sectionMoved.connect(main_window.set_file_edited)
        self.translation_add_button.clicked.connect(lambda: self._add_translation_row())

        self.suggests_add_button.clicked.connect(self._add_suggests_clicked)
        self.suggests_edit_button.clicked.connect(self._edit_suggests_clicked)
        self.suggests_remove_button.clicked.connect(self._remove_suggests_clicked)
        self.suggests_list.itemSelectionChanged.connect(self._update_suggests_edit_remove_button)

        self.replaces_add_button.clicked.connect(self._add_replaces_clicked)
        self.replaces_edit_button.clicked.connect(self._edit_replaces_clicked)
        self.replaces_remove_button.clicked.connect(self._remove_replaces_clicked)
        self.replaces_list.itemSelectionChanged.connect(self._update_replaces_edit_remove_button)

        self.tags_table.verticalHeader().sectionMoved.connect(main_window.set_file_edited)
        self.tags_add_button.clicked.connect(lambda: self._add_tags_row())

        self.branding_colors_check_box.stateChanged.connect(self._branding_colors_check_box_changed)
        self.light_branding_color_button.clicked.connect(self._light_branding_color_button_clicked)
        self.dark_branding_color_button.clicked.connect(self._dark_branding_color_button_clicked)

        self.custom_table.verticalHeader().sectionMoved.connect(main_window.set_file_edited)
        self.custom_add_button.clicked.connect(lambda: self._add_custom_row())

        self.tab_widget.setCurrentIndex(0)

    # Translation

    def _add_translation_row(self, translation_type: Optional[str] = None, domain: Optional[str] = None) -> None:
        row = self.translation_table.rowCount()
        self.translation_table.insertRow(row)

        type_box = QComboBox()
        type_box.addItem("gettext", "gettext")
        type_box.addItem("qt", "qt")
        type_box.currentIndexChanged.connect(self._main_window.set_file_edited)
        if translation_type is not None:
            select_combo_box_data(type_box, translation_type)
        self.translation_table.setCellWidget(row, 0, type_box)

        domain_item = QTableWidgetItem()
        if domain is not None:
            domain_item.setText(domain)
        self.translation_table.setItem(row, 1, domain_item)

        remove_button = QPushButton(QCoreApplication.translate("AdvancedWidget", "Remove"))
        remove_button.clicked.connect(self._remove_translation_clicked)
        self.translation_table.setCellWidget(row, 2, remove_button)

        self._main_window.set_file_edited()

    def _remove_translation_clicked(self) -> None:
        row = get_sender_table_row(self.translation_table, 2, self.sender())
        self.translation_table.removeRow(row)
        self._main_window.set_file_edited()

    # Suggests

    def _add_suggests_clicked(self) -> None:
        text = QInputDialog.getText(self, QCoreApplication.translate("AdvancedWidget", "New Suggestion"), QCoreApplication.translate("AdvancedWidget", "Please enter a new ID"))[0]
        if text == "":
            return
        if list_widget_contains_item(self.suggests_list, text):
            QMessageBox.critical(self, QCoreApplication.translate("AdvancedWidget", "ID in List"), QCoreApplication.translate("AdvancedWidget", "This ID is already in the List"))
            return
        self.suggests_list.addItem(text)
        self._update_suggests_edit_remove_button()
        self._main_window.set_file_edited()

    def _edit_suggests_clicked(self) -> None:
        if self.suggests_list.currentRow() == -1:
            return
        old_text = self.suggests_list.currentItem().text()
        new_text, ok = QInputDialog.getText(self, QCoreApplication.translate("AdvancedWidget", "Edit Suggestion"), QCoreApplication.translate("AdvancedWidget", "Please edit the ID"), text=old_text)
        if not ok or old_text == new_text:
            return
        if list_widget_contains_item(self.suggests_list, new_text):
            QMessageBox.critical(self, QCoreApplication.translate("AdvancedWidget", "ID in List"), QCoreApplication.translate("AdvancedWidget", "This ID is already in the List"))
            return
        self.suggests_list.currentItem().setText(new_text)
        self._main_window.set_file_edited()

    def _remove_suggests_clicked(self) -> None:
        index = self.suggests_list.currentRow()
        if index != -1:
            self.suggests_list.takeItem(index)
            self._update_suggests_edit_remove_button()
            self._main_window.set_file_edited()

    def _update_suggests_edit_remove_button(self) -> None:
        if self.suggests_list.currentRow() == -1:
            self.suggests_edit_button.setEnabled(False)
            self.suggests_remove_button.setEnabled(False)
        else:
            self.suggests_edit_button.setEnabled(True)
            self.suggests_remove_button.setEnabled(True)

    # Replaces

    def _add_replaces_clicked(self) -> None:
        text = QInputDialog.getText(self, QCoreApplication.translate("AdvancedWidget", "New Replacement"), QCoreApplication.translate("AdvancedWidget", "Please enter a ID"))[0]
        if text == "":
            return
        if list_widget_contains_item(self.replaces_list, text):
            QMessageBox.critical(self, QCoreApplication.translate("AdvancedWidget", "ID in List"), QCoreApplication.translate("AdvancedWidget", "This ID is already in the List"))
            return
        self.replaces_list.addItem(text)
        self._update_replaces_edit_remove_button()
        self._main_window.set_file_edited()

    def _edit_replaces_clicked(self) -> None:
        if self.replaces_list.currentRow() == -1:
            return
        old_text = self.replaces_list.currentItem().text()
        new_text, ok = QInputDialog.getText(self, QCoreApplication.translate("AdvancedWidget", "Edit Replacement"), QCoreApplication.translate("AdvancedWidget", "Please edit the ID"), text=old_text)
        if not ok or old_text == new_text:
            return
        if list_widget_contains_item(self.replaces_list, new_text):
            QMessageBox.critical(self, QCoreApplication.translate("AdvancedWidget", "ID in List"), QCoreApplication.translate("AdvancedWidget", "This ID is already in the List"))
            return
        self.replaces_list.currentItem().setText(new_text)
        self._main_window.set_file_edited()

    def _remove_replaces_clicked(self) -> None:
        index = self.replaces_list.currentRow()
        if index != -1:
            self.replaces_list.takeItem(index)
            self._update_replaces_edit_remove_button()
            self._main_window.set_file_edited()

    def _update_replaces_edit_remove_button(self) -> None:
        if self.replaces_list.currentRow() == -1:
            self.replaces_edit_button.setEnabled(False)
            self.replaces_remove_button.setEnabled(False)
        else:
            self.replaces_edit_button.setEnabled(True)
            self.replaces_remove_button.setEnabled(True)

    # Tags

    def _add_tags_row(self, namespace: Optional[str] = None, value: Optional[str] = None) -> None:
        row = self.tags_table.rowCount()
        self.tags_table.insertRow(row)

        namespace_item = QTableWidgetItem()
        if namespace is not None:
            namespace_item.setText(namespace)
        self.tags_table.setItem(row, 0, namespace_item)

        value_item = QTableWidgetItem()
        if value is not None:
            value_item.setText(value)
        self.tags_table.setItem(row, 1, value_item)

        remove_button = QPushButton(QCoreApplication.translate("AdvancedWidget", "Remove"))
        remove_button.clicked.connect(self._remove_tags_clicked)
        self.tags_table.setCellWidget(row, 2, remove_button)

        self._main_window.set_file_edited()

    def _remove_tags_clicked(self) -> None:
        row = get_sender_table_row(self.tags_table, 2, self.sender())
        self.tags_table.removeRow(row)
        self._main_window.set_file_edited()

    # Branding

    def _update_branding_colors_layout_enabled(self) -> None:
        set_layout_enabled(self.branding_colors_layout, self.branding_colors_check_box.isChecked())

    def _branding_colors_check_box_changed(self) -> None:
        self._update_branding_colors_layout_enabled()
        self._main_window.set_file_edited()

    def _get_branding_color_style_sheet(self, color: QColor) -> str:
        return f"background-color: {color.name()}; border: 1px solid black;"

    def _light_branding_color_button_clicked(self) -> None:
        color = QColorDialog.getColor(parent=self)

        if not color.isValid():
            return

        self.light_branding_color_button.setStyleSheet(self._get_branding_color_style_sheet(color))
        self._main_window.set_file_edited()

    def _dark_branding_color_button_clicked(self) -> None:
        color = QColorDialog.getColor(parent=self)

        if not color.isValid():
            return

        self.dark_branding_color_button.setStyleSheet(self._get_branding_color_style_sheet(color))
        self._main_window.set_file_edited()

    # Custom

    def _add_custom_row(self, key: Optional[str] = None, value: Optional[str] = None) -> None:
        row = self.custom_table.rowCount()
        self.custom_table.insertRow(row)

        key_item = QTableWidgetItem()
        if key is not None:
            key_item.setText(key)
        self.custom_table.setItem(row, 0, key_item)

        value_item = QTableWidgetItem()
        if value is not None:
            value_item.setText(value)
        self.custom_table.setItem(row, 1, value_item)

        remove_button = QPushButton(QCoreApplication.translate("AdvancedWidget", "Remove"))
        remove_button.clicked.connect(self._remove_custom_clicked)
        self.custom_table.setCellWidget(row, 2, remove_button)

        self._main_window.set_file_edited()

    def _remove_custom_clicked(self) -> None:
        row = get_sender_table_row(self.custom_table, 2, self.sender())
        self.custom_table.removeRow(row)
        self._main_window.set_file_edited()

    # Other

    def reset_data(self) -> None:
        clear_table_widget(self.translation_table)
        self.suggests_list.clear()
        self.replaces_list.clear()
        clear_table_widget(self.tags_table)
        self.branding_colors_check_box.setChecked(False)
        self.light_branding_color_button.setStyleSheet(self._get_branding_color_style_sheet(QColor("white")))
        self.dark_branding_color_button.setStyleSheet(self._get_branding_color_style_sheet(QColor("black")))
        clear_table_widget(self.custom_table)

        self._update_suggests_edit_remove_button()
        self._update_branding_colors_layout_enabled()

    def load_data(self, root_tag: etree._Element) -> None:
        for i in root_tag.findall("translation"):
            self._add_translation_row(translation_type=i.get("type"), domain=i.text)

        suggests_tag = root_tag.find("suggests")
        if suggests_tag is not None:
            for i in suggests_tag.findall("id"):
                self.suggests_list.addItem(i.text)

        replaces_tag = root_tag.find("replaces")
        if replaces_tag is not None:
            for i in replaces_tag.findall("id"):
                self.replaces_list.addItem(i.text)

        tags_tag = root_tag.find("tags")
        if tags_tag is not None:
            for i in tags_tag.findall("tag"):
                self._add_tags_row(namespace=i.get("namespace"), value=i.text)

        if (branding_tag := root_tag.find("branding")) is not None:
            self.branding_colors_check_box.setChecked(True)
            for color_tag in branding_tag.findall("color"):
                if color_tag.get("scheme_preference") == "light":
                    self.light_branding_color_button.setStyleSheet(self._get_branding_color_style_sheet(QColor(color_tag.text)))
                elif color_tag.get("scheme_preference") == "dark":
                    self.dark_branding_color_button.setStyleSheet(self._get_branding_color_style_sheet(QColor(color_tag.text)))

        custom_tag = root_tag.find("custom")
        if custom_tag is not None:
            for i in custom_tag.findall("value"):
                self._add_custom_row(key=i.get("key"), value=i.text)

    def _get_branding_tag(self) -> etree.Element:
        branding_tag = etree.Element("branding")

        light_color_tag = etree.SubElement(branding_tag, "color")
        light_color_tag.set("type", "primary")
        light_color_tag.set("scheme_preference", "light")
        light_color_tag.text = re.search("#([0-9]|[a-f]){6}", self.light_branding_color_button.styleSheet()).group()

        dark_color_tag = etree.SubElement(branding_tag, "color")
        dark_color_tag.set("type", "primary")
        dark_color_tag.set("scheme_preference", "dark")
        dark_color_tag.text = re.search("#([0-9]|[a-f]){6}", self.dark_branding_color_button.styleSheet()).group()

        return branding_tag

    def save_data(self, root_tag: etree.Element) -> None:
        for i in get_logical_table_row_list(self.translation_table):
            translation_tag = etree.SubElement(root_tag, "translation")
            translation_tag.set("type", self.translation_table.cellWidget(i, 0).currentData())
            translation_tag.text = self.translation_table.item(i, 1).text().strip()

        if self.suggests_list.count() > 0:
            suggests_tag = etree.SubElement(root_tag, "suggests")
            for i in range(self.suggests_list.count()):
                id_tag = etree.SubElement(suggests_tag, "id")
                id_tag.text = self.suggests_list.item(i).text().strip()

        if self.replaces_list.count() > 0:
            replaces_tag = etree.SubElement(root_tag, "replaces")
            for i in range(self.replaces_list.count()):
                id_tag = etree.SubElement(replaces_tag, "id")
                id_tag.text = self.replaces_list.item(i).text().strip()

        if self.tags_table.rowCount() > 0:
            tags_tag = etree.SubElement(root_tag, "tags")
            for i in get_logical_table_row_list(self.tags_table):
                tag_tag = etree.SubElement(tags_tag, "tag")
                tag_tag.set("namespace", self.tags_table.item(i, 0).text())
                tag_tag.text = self.tags_table.item(i, 1).text().strip()

        if self.branding_colors_check_box.isChecked():
            try:
                root_tag.append(self._get_branding_tag())
            except Exception:
                print(traceback.format_exc(), file=sys.stderr)

        if self.custom_table.rowCount() > 0:
            custom_tag = etree.SubElement(root_tag, "custom")
            for i in get_logical_table_row_list(self.custom_table):
                value_tag = etree.SubElement(custom_tag, "value")
                value_tag.set("key", self.custom_table.item(i, 0).text().strip())
                value_tag.text = self.custom_table.item(i, 1).text().strip()
