import os
import sys
from pathlib import Path
import json

sys.path.append(os.path.join(os.getcwd(), "./*"))

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QLayout,
    QVBoxLayout,
)
from PySide6.QtGui import QBrush, QColor
from PySide6.QtCore import Qt


class MainView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main View")
        # Setup UI from generated Python class instead of loading .ui at runtime
        try:
            from app._ui.MainWindow_ui import Ui_MainWindow
        except Exception as e:
            QMessageBox.critical(
                self, "Missing UI", f"Failed to import generated MainWindow_ui.py: {e}"
            )
            raise SystemExit(1)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Preserve the base stylesheet defined by the .ui so we can extend/restore it per theme
        self._base_stylesheet = self.styleSheet() or ""
        self.apply_theme("light")

    def apply_theme(self, theme_name):
        """Apply the specified theme to the application."""
        if theme_name == "dark":
            dark_stylesheet = """
                QMainWindow {
                    background-color: #2b2b2b;
                    color: #ffffff;
                }
                /* Add more dark theme styles here */
            """
            self.setStyleSheet(self._base_stylesheet + dark_stylesheet)
        else:
            # Restore base stylesheet for light theme
            self.setStyleSheet(self._base_stylesheet)
