from ping3 import ping as ping3_ping
from PyQt5.QtCore import QThread, pyqtSignal, QObject
from PyQt5.QtWidgets import QMessageBox
import re
import pythoncom


class DnsPingThread(QThread):
    """Worker thread for DNS ping testing to avoid blocking UI."""
    ping_result = pyqtSignal(str)

    def __init__(self, dns_servers, dns_name):
        super(DnsPingThread, self).__init__()
        self.dns_servers = dns_servers
        self.dns_name = dns_name

    def run(self):
        if not self.dns_servers:
            return
            
        server = self.dns_servers[0]
        try:
            pings = []
            for _ in range(5):
                result = ping3_ping(server, timeout=1, unit='ms', size=56)
                if result is not None:
                    pings.append(result)
            
            if pings:
                lowest_ping = min(pings)
                ping_result = f"{str(self.dns_name).split(' -')[0]} Ping: {int(lowest_ping)}ms"
            else:
                ping_result = "No response from DNS servers"
        except Exception:
            ping_result = "Ping error"
        
        self.ping_result.emit(ping_result)


class SuperWorkerThread(QThread):
    """Worker thread for Gameloop Super button to avoid freezing the UI."""
    task_completed = pyqtSignal(bool, str)  # success, message

    def __init__(self, window):
        super(SuperWorkerThread, self).__init__()
        self.app = window

    def run(self):
        try:
            pythoncom.CoInitialize()
            self.app.kill_gameloop()
            self.app.gameloop_settings()
            self.app.add_to_windows_defender_exclusion()
            self.app.optimize_gameloop_registry()
            self.app.force_dedicated_gpu()
            self.app.optimize_for_nvidia()
            self.task_completed.emit(True, "Gameloop Super mode optimizations applied successfully ⚡")
        except Exception as e:
            self.app.logger.error(f"Exception occurred: {str(e)}", exc_info=True)
            self.task_completed.emit(False, f"Error: {str(e)}")
        finally:
            pythoncom.CoUninitialize()


class OtherWorkerThread(QThread):
    task_completed = pyqtSignal(bool, str)

    def __init__(self, app, task_type, args=None):
        super(OtherWorkerThread, self).__init__()
        self.app = app
        self.task_type = task_type
        self.args = args

    def run(self):
        try:
            pythoncom.CoInitialize()
            if self.task_type == "temp_cleaner":
                self.app.temp_cleaner()
                self.task_completed.emit(True, "System performance improved (Temp files cleaned).")
            elif self.task_type == "optimizer":
                self.app.add_to_windows_defender_exclusion()
                self.app.optimize_gameloop_registry()
                self.app.optimize_for_nvidia()
                self.task_completed.emit(True, "Gameloop optimizer applied successfully.")
            elif self.task_type == "all_recommended":
                self.app.gameloop_settings()
                self.app.add_to_windows_defender_exclusion()
                self.app.optimize_gameloop_registry()
                self.app.optimize_for_nvidia()
                self.app.temp_cleaner()
                self.task_completed.emit(True, "All recommended settings applied successfully.")
            elif self.task_type == "dns_changer":
                if self.app.change_dns_servers(self.args):
                    self.task_completed.emit(True, "DNS changed successfully.")
                else:
                    self.task_completed.emit(False, "Failed to change DNS.")
            elif self.task_type == "shortcut":
                self.app.gen_game_icon(self.args)
                self.task_completed.emit(True, f"Shortcut for {self.args} created on Desktop.")
            elif self.task_type == "ipad_view":
                self.app.ipad_settings(*self.args)
                self.task_completed.emit(True, "iPad View resolution applied successfully.")
            elif self.task_type == "gpu_cpu_optimize":
                if self.app.force_gpu_and_optimize_cpu():
                    self.task_completed.emit(True, "GPU forced & CPU optimized! Restart GameLoop for changes to take effect.")
                else:
                    self.task_completed.emit(False, "Failed to optimize. Check error.log for details.")
            elif self.task_type == "install_drivers":
                result = self.app.install_essential_drivers()
                self.task_completed.emit(True, f"Drivers: {result}")
            elif self.task_type == "uninstall_gameloop":
                success, message = self.app.uninstall_gameloop()
                self.task_completed.emit(success, message)
        except Exception as e:
            self.task_completed.emit(False, f"Error: {str(e)}")
        finally:
            pythoncom.CoUninitialize()


class Other(QObject):
    def __init__(self, window):
        super(Other, self).__init__()
        self.ui = window.ui
        self.app = window
        self.dns_servers = {
            "Google DNS - 8.8.8.8": ['8.8.8.8', '8.8.4.4'],
            "Cloudflare DNS - 1.1.1.1": ['1.1.1.1', '1.0.0.1'],
            "Quad9 DNS - 9.9.9.9": ['9.9.9.9', '149.112.112.112'],
            "Cisco Umbrella - 208.67.222.222": ['208.67.222.222', '208.67.220.220'],
            "Yandex DNS - 77.88.8.1": ['77.88.8.1', '77.88.8.8']
        }
        self.function()

    def function(self):
        ui = self.ui

        ui.tempcleaner_other_btn.clicked.connect(self.temp_cleaner_button_click)
        ui.gloptimizer_other_btn.clicked.connect(self.gameloop_optimizer_button_click)
        ui.all_other_btn.clicked.connect(self.all_recommended_button_click)
        ui.forceclosegl_other_btn.clicked.connect(self.kill_gameloop_processes_button_click)
        ui.uninstallgl_other_btn.clicked.connect(self.uninstall_gameloop_click)
        ui.gameloopsuper_other_btn.clicked.connect(self.gameloop_super_button_click)
        ui.gpuforce_other_btn.clicked.connect(self.gpu_force_button_click)
        ui.drivers_other_btn.clicked.connect(self.drivers_button_click)
        ui.shortcut_other_btn.clicked.connect(self.shortcut_submit_button_click)
        ui.dns_dropdown.currentTextChanged.connect(self.on_dns_dropdown_change)
        ui.dns_other_btn.clicked.connect(self.dns_submit_button_click)
        ui.ipad_other_btn.clicked.connect(self.ipad_submit_button_click)
        ui.ipad_rest_btn.clicked.connect(self.ipad_reset_button_click)

        ui.ipad_code.hide()
        ui.ipad_code_label.hide()

        _width = self.app.settings.value("VMResWidth")
        _height = self.app.settings.value("VMResHeight")

        if _width is None or _height is None:
            ui.ipad_rest_btn.hide()

    def _start_worker(self, task_type, args=None, btn=None, initial_msg=""):
        if btn:
            btn.setEnabled(False)
        if initial_msg:
            self.app.show_status_message(initial_msg, 30)
            
        self._generic_worker = OtherWorkerThread(self.app, task_type, args)
        self._generic_worker.task_completed.connect(lambda success, msg: self._worker_done(success, msg, btn))
        self._generic_worker.start()

    def _worker_done(self, success, message, btn=None):
        if btn:
            btn.setEnabled(True)
        self.app.show_status_message(message, 5)

    def temp_cleaner_button_click(self, e):
        self._start_worker("temp_cleaner", btn=self.ui.tempcleaner_other_btn, initial_msg="Cleaning temp files...")

    def gameloop_optimizer_button_click(self, e):
        self._start_worker("optimizer", btn=self.ui.gloptimizer_other_btn, initial_msg="Optimizing Gameloop...")

    def all_recommended_button_click(self, e):
        self._start_worker("all_recommended", btn=self.ui.all_other_btn, initial_msg="Applying all recommendations...")

    def kill_gameloop_processes_button_click(self, e):
        """Terminates Gameloop processes when the button is clicked."""
        if self.app.kill_gameloop():
            message = "All Gameloop processes terminated."
        else:
            message = "No processes found to terminate."
        self.app.show_status_message(message)

    def uninstall_gameloop_click(self, e):
        """Gameloop Uninstall Button On Click Function"""
        msg_box = QMessageBox(self.ui.centralwidget)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Confirm Uninstall")
        msg_box.setText("Are you sure you want to completely uninstall GameLoop?")
        msg_box.setInformativeText("This will forcefully remove GameLoop, all its data, settings, and registries. This action cannot be undone.")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)
        
        reply = msg_box.exec_()
        
        if reply == QMessageBox.Yes:
            self._start_worker("uninstall_gameloop", btn=self.ui.uninstallgl_other_btn, initial_msg="Uninstalling GameLoop... This may take a minute.")

    def gameloop_super_button_click(self, e):
        """ Gameloop Super Button On Click Function """
        self.ui.gameloopsuper_other_btn.setEnabled(False)
        self.app.show_status_message("Applying Super mode settings, please wait...", 60)
        self._super_worker = SuperWorkerThread(self.app)
        self._super_worker.task_completed.connect(self._gameloop_super_done)
        self._super_worker.start()

    def _gameloop_super_done(self, success, message):
        self.ui.gameloopsuper_other_btn.setEnabled(True)
        self.app.show_status_message(message, 5)

    def gpu_force_button_click(self, e):
        """Force GPU and Optimize CPU Button On Click Function"""
        self.ui.gpuforce_other_btn.setEnabled(False)
        self.app.show_status_message("Forcing dedicated GPU and optimizing CPU...", 60)
        self._gpu_worker = OtherWorkerThread(self.app, "gpu_cpu_optimize")
        self._gpu_worker.task_completed.connect(self._gpu_force_done)
        self._gpu_worker.start()

    def _gpu_force_done(self, success, message):
        self.ui.gpuforce_other_btn.setEnabled(True)
        self.app.show_status_message(message, 10)

    def drivers_button_click(self, e):
        """Essential Drivers Button On Click — downloads VC++ runtimes and opens GPU driver page."""
        self.ui.drivers_other_btn.setEnabled(False)
        self.app.show_status_message("Downloading & installing essential drivers, please wait...", 120)
        self._drivers_worker = OtherWorkerThread(self.app, "install_drivers")
        self._drivers_worker.task_completed.connect(self._drivers_done)
        self._drivers_worker.start()

    def _drivers_done(self, success, message):
        self.ui.drivers_other_btn.setEnabled(True)
        self.app.show_status_message(message, 10)

    def shortcut_submit_button_click(self, e):
        game_name = self.ui.shortcut_dropdown.currentText()
        if game_name:
            self._start_worker("shortcut", args=game_name, btn=self.ui.shortcut_other_btn, initial_msg=f"Creating shortcut for {game_name}...")

    def dns_submit_button_click(self, e):
        dns_key = self.ui.dns_dropdown.currentText()
        dns_server = self.dns_servers.get(dns_key)
        if dns_server:
            self._start_worker("dns_changer", args=dns_server, btn=self.ui.dns_other_btn, initial_msg="Changing DNS settings...")

    def on_dns_dropdown_change(self, value):
        if not value or value not in self.dns_servers:
            return
            
        # Run DNS ping test in background thread to avoid blocking UI
        self._dns_ping_worker = DnsPingThread(self.dns_servers.get(value), value)
        self._dns_ping_worker.ping_result.connect(self.ui.dns_status_label.setText)
        self._dns_ping_worker.start()

    def ipad_submit_button_click(self, e):
        if self.app.is_gameloop_running():
            self.app.show_status_message("Close Gameloop to use this button. (Force Close Gameloop)", 5)
            return

        resolution = self.ui.ipad_dropdown.currentText()
        if not resolution:
            self.app.show_status_message("Please select a resolution first", 5)
            return
            
        try:
            match = re.search(r'(\d+)\s*x\s*(\d+)', resolution)
            if not match:
                self.app.show_status_message("Invalid resolution format", 5)
                return
            width, height = map(int, match.groups())
            self._start_worker("ipad_view", args=(width, height), btn=self.ui.ipad_other_btn, initial_msg="Applying iPad view...")
        except Exception:
            self.app.show_status_message("Invalid resolution format", 5)

    def ipad_reset_button_click(self, e):
        if self.app.is_gameloop_running():
            self.app.show_status_message(f"Close Gameloop to use this button. (Force Close Gameloop)", 5)
            return
            
        width, height = self.app.reset_ipad()
        if width:
            self.ui.ipad_rest_btn.hide()
            self.app.show_status_message(f"iPad view reset. Original resolution {width}x{height} restored.")
        else:
            self.app.show_status_message("No iPad view backup found to reset.")