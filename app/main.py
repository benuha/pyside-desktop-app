import os
import sys

from PySide6.QtWidgets import QApplication

from app.view.MainView import MainView


def main():
    # Enable High DPI scaling for better visuals on high-res displays
    os.environ.setdefault("QT_ENABLE_HIGHDPI_SCALING", "1")
    os.environ.setdefault("QT_SCALE_FACTOR_ROUNDING_POLICY", "PassThrough")

    app = QApplication(sys.argv)
    win = MainView()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
