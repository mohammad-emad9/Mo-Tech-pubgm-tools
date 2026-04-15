import ctypes
import os
import sys
from datetime import datetime
from pathlib import Path

from PyQt5 import QtCore, QtWidgets

from src.ui_functions import Window
from src.update import UpdateWindow

APP_NAME = "Mo-Tech"
APP_VERSION = "v1.0.8"
FULL_APP_NAME = f"{APP_NAME} {APP_VERSION}"
ctypes.windll.kernel32.SetConsoleTitleW(FULL_APP_NAME)

# Set AppUserModelID to ensure taskbar icon displays correctly
try:
    myappid = f"com.mkvip.pubgtool.{APP_VERSION}"
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except Exception:
    pass


def run_application(app):
    """
    Run the main GUI application.
    """
    ui = Window(APP_NAME, APP_VERSION)
    ui.show()
    return app.exec_()


if __name__ == "__main__":
    print("[#] Starting the GUI app")

    def suppress_qt_warnings():
        max_scale = "1.5"

        scale_factor = str(ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100)
        if float(scale_factor) > float(max_scale):
            scale_factor = max_scale

        os.environ["QT_DEVICE_PIXEL_RATIO"] = "0"
        os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "0"
        os.environ["QT_SCALE_FACTOR"] = "1"
        os.environ["QT_SCREEN_SCALE_FACTORS"] = scale_factor


    suppress_qt_warnings()

    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    try:
        app = QtWidgets.QApplication(sys.argv)
        app.setStyle("Fusion")
        app.setStyleSheet("""
            QWidget { background-color: #1e1e2e; color: #cdd6f4; font-family: 'Segoe UI', Arial, sans-serif; }
            QPushButton { background-color: #313244; border: 1px solid #45475a; border-radius: 6px; padding: 6px 14px; font-weight: bold; color: #cdd6f4; }
            QPushButton:hover { background-color: #45475a; border: 1px solid #cba6f7; color: #cba6f7; }
            QPushButton:pressed { background-color: #585b70; }
            QPushButton:checked { background-color: #cba6f7; color: #11111b; }
            QComboBox { background-color: #313244; border: 1px solid #45475a; border-radius: 4px; padding: 4px; color: #cdd6f4; }
            QComboBox QAbstractItemView { background-color: #313244; selection-background-color: #45475a; }
            QCheckBox::indicator { width: 16px; height: 16px; }
            QCheckBox::indicator:unchecked { background-color: #313244; border: 1px solid #45475a; }
            QCheckBox::indicator:checked { background-color: #cba6f7; border: 1px solid #cba6f7; }
            QRadioButton::indicator { width: 16px; height: 16px; border-radius: 8px; }
            QRadioButton::indicator:unchecked { background-color: #313244; border: 1px solid #45475a; }
            QRadioButton::indicator:checked { background-color: #cba6f7; border: 1px solid #cba6f7; }
            QGroupBox { border: 1px solid #45475a; border-radius: 6px; margin-top: 2ex; }
            QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 3px; color: #cba6f7; }
            QLineEdit { background-color: #313244; border: 1px solid #45475a; border-radius: 4px; padding: 4px; color: #cdd6f4; }
        """)

        update = UpdateWindow()
        update.check_for_updates(APP_VERSION)

        if update.is_update_available():
            update.show()
            app.exec_()
        
        # Always run the main application after update check
        run_application(app)
    except Exception as e:
        with open(f"{Path.cwd()}/error.log", "a") as f:
            f.write(f"-------------------{datetime.now()}-------------------\n")
            f.write(f"CRASH_ERR: {e}\n")
