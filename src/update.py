import os
import zipfile
from PyQt5.QtCore import QThread, QTimer, QSize, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtWidgets import QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget
import requests

from . import resource_path


class DownloadThread(QThread):
    download_progress = pyqtSignal(int)
    download_complete = pyqtSignal()
    download_failed = pyqtSignal(str)

    def __init__(self, url, filename):
        super().__init__()
        self.url = url
        self.filename = filename

    def run(self):
        try:
            response = requests.get(self.url, stream=True, timeout=30)
            if response.status_code == 200:
                total_size = int(response.headers.get("content-length", 0))
                bytes_downloaded = 0
                
                if not os.path.exists(self.filename):
                    with open(self.filename, "wb") as file:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                file.write(chunk)
                                bytes_downloaded += len(chunk)
                                if total_size > 0:
                                    progress = int((bytes_downloaded / total_size) * 100)
                                    self.download_progress.emit(progress)

                try:
                    with zipfile.ZipFile(self.filename, 'r') as zip_ref:
                        exe_file = next((name for name in zip_ref.namelist() if name.endswith(".exe")), None)
                        if exe_file:
                            # Extract to a known location first
                            zip_ref.extract(exe_file)
                            # Use absolute path for os.startfile
                            exe_path = os.path.abspath(exe_file)
                            os.startfile(exe_path, 'runas')
                            self.download_complete.emit()
                        else:
                            self.download_failed.emit("Failed to open update file.")
                except zipfile.BadZipFile:
                    if os.path.exists(self.filename):
                        os.remove(self.filename)
                    self.download_failed.emit("Corrupted update file, please try again.")
                except Exception as e:
                    self.download_failed.emit(f"Update error: {str(e)}")
            else:
                self.download_failed.emit("Failed to download the update.")
        except Exception as e:
            self.download_failed.emit(f"Download error: {str(e)}")


class UpdateWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        icon = QIcon()
        icon.addFile(resource_path(r"assets\icons\logo.ico"), QSize(), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        self.setWindowTitle("Update Available")
        self.resize(350, 200)
        # Center the window on the screen
        screen_geometry = QGuiApplication.primaryScreen().availableGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)

        self.label = QLabel("Checking for updates...")
        self.label.setMaximumHeight(20)

        self.check_button = QPushButton("Check for Updates")
        self.check_button.setMaximumHeight(35)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setMaximumHeight(35)

        self.change_log_label = QLabel()

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.change_log_label)
        layout.addWidget(self.check_button)
        layout.addWidget(self.cancel_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.check_button.clicked.connect(self.check_for_updates)
        self.cancel_button.clicked.connect(self.cancel_update)

        self.download_thread = None

    def download_update(self):
        self.check_button.setEnabled(False)
        self.cancel_button.setEnabled(False)

        self.download_thread = DownloadThread(self.download_url, self.asset_name)
        self.download_thread.download_progress.connect(self.update_download_progress)
        self.download_thread.download_complete.connect(self.complete_download)
        self.download_thread.download_failed.connect(self.fail_download)

        self.download_thread.start()

    def check_for_updates(self, current_version=None):
        url = "https://api.github.com/repos/MohamedKVIP/MK-PUBG-Mobile-Tool/releases/latest"
        self.current_version = current_version
        self.latest_version = current_version  # Default to current if check fails
        self.data = {}
        
        try:
            response = requests.get(url, timeout=10)
        except requests.RequestException:
            return

        if response.status_code == 200:
            self.data = response.json()
            self.latest_version = self.data.get("tag_name", "")

            assets = self.data.get("assets", [])
            if assets:
                asset = assets[0]
                self.asset_name = asset.get("name", "")
                self.download_url = asset.get("browser_download_url", "")

                if self.is_update_available():
                    self.show_update_available()
            else:
                self.show_no_assets_found()

    def is_update_available(self):
        try:
            return self.current_version != self.latest_version
        except TypeError:
            return False

    def show_update_available(self):
        self.label.setText(f"Latest version: {self.latest_version}")
        self.check_button.setText("Download Update")
        self.check_button.clicked.connect(self.download_update)
        change_log = self.get_change_log()
        self.change_log_label.setText(f"Change Log:\n{change_log}")

    def show_no_assets_found(self):
        self.label.setText("No assets found in the latest release.")
        self.change_log_label.clear()

    def show_failed_to_fetch_updates(self):
        self.label.setText("Failed to fetch updates.")
        self.change_log_label.clear()

    def get_change_log(self):
        return self.data.get("body", "No change log available.")

    def update_download_progress(self, progress):
        self.label.setText(f"Downloading update... {progress}%")

    def complete_download(self):
        self.label.setText("Update downloaded and extracted.")
        self.check_button.setEnabled(False)
        self.cancel_button.setEnabled(False)
        QTimer.singleShot(2000, self.close)

    def fail_download(self, error_message):
        self.label.setText(error_message)
        self.check_button.setEnabled(True)
        self.cancel_button.setEnabled(False)

    def cancel_update(self):
        try:
            if self.download_thread and self.download_thread.isRunning():
                self.download_thread.quit()
                self.download_thread.wait()

            self.label.setText("Update canceled.")
            self.change_log_label.clear()
            self.check_button.setEnabled(True)
            self.cancel_button.setEnabled(False)
        except Exception as e:
            self.label.setText(f"Error canceling update: {str(e)}")
        finally:
            self.close()
