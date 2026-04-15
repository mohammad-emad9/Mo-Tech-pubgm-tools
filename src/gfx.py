import json
from PyQt5.QtCore import QThread, pyqtSignal, QObject


class SubmitWorkerThread(QThread):
    task_completed = pyqtSignal()
    status_msg = pyqtSignal(str)

    def __init__(self, window, ui, gfx):
        super(SubmitWorkerThread, self).__init__()
        self.app = window
        self.ui = ui
        self.gfx = gfx
        
        self.selected_graphics = next((btn.text() for btn in self.gfx.graphics_buttons if btn.isChecked()), None)
        self.selected_fps = next((btn.text() for btn in self.gfx.fps_buttons if btn.isChecked()), None)
        self.selected_style_id = next((btn.property("styleId") for btn in self.gfx.style_buttons if btn.isChecked()), None)
        self.selected_shadow = next((btn.text() for btn in self.gfx.shadow_buttons if btn.isChecked()), None)
        self.is_kr = self.app.pubg_package == "com.pubg.krmobile"
        self.is_resolution_checked = self.ui.resolution_btn.isChecked()

    def run(self):
        self.status_msg.emit("Working on Graphics Settings ...")

        if self.selected_graphics:
            self.app.set_graphics_quality(self.selected_graphics)

        if self.selected_style_id:
            self.app.set_graphics_style(self.selected_style_id)

        # Shadow must run BEFORE FPS so that set_fps CVARs are not overwritten
        if self.selected_shadow:
            shadow_status = "ON" if self.selected_shadow == "Enable" else "OFF"
            self.app.set_shadow(shadow_status)

        if self.selected_fps:
            self.app.set_fps(self.selected_fps)

        self.app.save_graphics_file()
        self.app.push_active_shadow_file()

        if self.is_kr and self.is_resolution_checked:
            self.app.kr_fullhd()
        else:
            self.app.start_app()

        self.task_completed.emit()



class ConnectWorkerThread(QThread):
    task_completed = pyqtSignal()
    status_msg = pyqtSignal(str, int)
    conn_error = pyqtSignal(str)
    pubg_choose = pyqtSignal(list)
    conn_success = pyqtSignal(str)

    def __init__(self, window, ui):
        super(ConnectWorkerThread, self).__init__()
        self.app = window
        self.ui = ui

    def get_active_file(self, pubg_version):
        """ Get the active file for the given PUBG version """
        pubg_package = next(key for key, value in self.app.pubg_versions.items() if value == pubg_version)
        self.app.get_graphics_file(pubg_package)

    def show_connection_error(self, message):
        self.conn_error.emit(message)
        self.task_completed.emit()

    def run(self):
        try:
            self.status_msg.emit("Initializing ADB connection...", 3)
            self.app.check_adb_status()

            if not self.app.adb_enabled:
                self.status_msg.emit("ADB was disabled. Enabling now. Please Restart GameLoop.", 5)
                self.show_connection_error("Restart GameLoop and Try Again.")
                return

            if not self.app.is_gameloop_running():
                self.show_connection_error("GameLoop is not running. Please open it first.")
                return

            self.status_msg.emit("Searching for Emulator...", 3)
            self.app.check_adb_connection()

            if not self.app.is_adb_working:
                self.show_connection_error("Failed to find Emulator via ADB. Check GameLoop settings.")
                return

            self.status_msg.emit("Finding PUBG versions...", 3)
            self.app.pubg_version_found()
            num_found = len(self.app.PUBG_Found)

            if num_found == 0:
                self.status_msg.emit("No PUBG versions found on Emulator.", 5)
                self.task_completed.emit()
                return
            elif num_found > 1:
                self.status_msg.emit("Multiple versions found. Select one.", 5)
                self.pubg_choose.emit(self.app.PUBG_Found)
                self.task_completed.emit()
                return

            self.status_msg.emit(f"Connected! Using {self.app.PUBG_Found[0]}", 3)
            self.conn_success.emit(self.app.PUBG_Found[0])
            self.task_completed.emit()

        except Exception as e:
            self.app.logger.error(f"Fatal error in ConnectWorkerThread: {e}", exc_info=True)
            self.show_connection_error(f"Fatal Error: {e}")


class GFX(QObject):
    GFX_PROFILE_KEY = "gfx/last_profile"

    def __init__(self, window):
        super(GFX, self).__init__()
        self.ui = window.ui
        self.app = window

        self.call_app()

    def call_app(self):
        # Hide Labels and Buttons in UI
        self.ui.ResolutionkrFrame.hide()
        self.ui.PubgchooseFrame.hide()

        self.graphics_buttons_func()
        self.fps_buttons_func()
        self.style_buttons_func()
        self.shadow_buttons_func()

        self.gfx_buttons(enabled=False)

        # Button connections
        self.ui.connect_gameloop_btn.clicked.connect(self.connect_gameloop_button_click)
        self.ui.submit_gfx_btn.clicked.connect(self.gfx_submit_button_click)

    def gfx_submit_button_click(self):
        self.save_user_profile()
        self.ui.submit_gfx_btn.setEnabled(False)
        self.worker_submit = SubmitWorkerThread(self.app, self.ui, self)
        self.worker_submit.status_msg.connect(lambda msg: self.app.show_status_message(msg))
        self.worker_submit.task_completed.connect(self.submit_gfx_done)
        self.worker_submit.start()

    def submit_gfx_done(self):
        self.ui.submit_gfx_btn.setEnabled(True)
        self.save_user_profile()
        if self.app.pubg_package == "com.pubg.krmobile" and self.ui.resolution_btn.isChecked():
            status_message = "Graphics settings applied, resolution set to 1080p."
        else:
            status_message = "Graphics settings applied successfully."
        self.app.show_status_message(status_message)

    def connect_gameloop_button_click(self, checked: bool):
        if checked:
            self.ui.connect_gameloop_btn.setEnabled(False)
            self.ui.connect_gameloop_btn.setText("Connecting...")
            self.app.show_status_message("Connecting to Gameloop...", 3)
            self.worker = ConnectWorkerThread(self.app, self.ui)
            self.worker.status_msg.connect(lambda msg, dur: self.app.show_status_message(msg, dur))
            self.worker.conn_error.connect(self.handle_conn_error)
            self.worker.pubg_choose.connect(self.handle_pubg_choose)
            self.worker.conn_success.connect(self.handle_conn_success)
            self.worker.task_completed.connect(self.connect_gameloop_task_completed)
            self.worker.start()
        else:
            self.gfx_buttons(enabled=checked)
            self.ui.disable_shadow_btn.setChecked(False)
            self.ui.enable_shadow_btn.setChecked(False)
            self.ui.ResolutionkrFrame.hide()
            self.ui.PubgchooseFrame.hide()
            self.app.kill_adb()
            self.ui.connect_gameloop_btn.setText("Connect to GameLoop")
            self.app.show_status_message("Disconnected from GameLoop", 3)

    def handle_conn_error(self, message):
        self.ui.connect_gameloop_btn.setChecked(False)
        self.ui.connect_gameloop_btn.setText("Connect to GameLoop")
        self.app.show_status_message(message)

    def handle_pubg_choose(self, pubg_found):
        self.ui.pubgchoose_dropdown.clear()
        self.ui.pubgchoose_dropdown.addItems(pubg_found)
        self.ui.pubgchoose_dropdown.setCurrentText(pubg_found[0])
        self.ui.PubgchooseFrame.setVisible(True)
        try:
            self.ui.pubgchoose_btn.clicked.disconnect()
        except TypeError:
            pass
        self.ui.pubgchoose_btn.clicked.connect(self.use_pubg_version)

    def handle_conn_success(self, version):
        pubg_package = next(key for key, value in self.app.pubg_versions.items() if value == version)
        self.app.get_graphics_file(pubg_package)
        self.ui.connect_gameloop_btn.setText("Connected")

    def use_pubg_version(self):
        val = self.ui.pubgchoose_dropdown.currentText()
        pubg_package = next(k for k, v in self.app.pubg_versions.items() if v == val)
        self.app.get_graphics_file(pubg_package)
        self.ui.connect_gameloop_btn.setText("Connected")
        self.app.show_status_message(f"Using version {val}", 3)
        self.ui.PubgchooseFrame.hide()
        self.connect_gameloop_task_completed(checked=False)

    def connect_gameloop_task_completed(self, checked: bool = True):
        if not self.app.is_adb_working:
            self.ui.connect_gameloop_btn.setEnabled(True)
            self.ui.connect_gameloop_btn.setText("Connect to Gameloop")
            self.app.show_status_message("Connection Failed: Emulator not found.", 10)
            return
        
        if checked:
            self.app.show_status_message("Connected to Emulator Successfully ✅", 5)
            if len(self.app.PUBG_Found) > 1:
                self.ui.pubgchoose_btn.clicked.connect(self.use_pubg_version)
                return
        self.ui.connect_gameloop_btn.setEnabled(True)
        self.ui.connect_gameloop_btn.setText("Connected")

        self.graphics_buttons = [
            self.ui.supersmooth_graphics_btn,
            self.ui.smooth_graphics_btn,
            self.ui.balanced_graphics_btn,
            self.ui.hd_graphics_btn,
            self.ui.hdr_graphics_btn,
            self.ui.ultrahd_graphics_btn,
            self.ui.uhd_graphics_btn,
        ]
        self.graphics_value = self.app.get_graphics_setting()

        for button in self.graphics_buttons:
            if button.text() == self.graphics_value:
                button.setChecked(True)
                break

        self.fps_buttons = [
            self.ui.low_fps_btn,
            self.ui.medium_fps_btn,
            self.ui.high_fps_btn,
            self.ui.ultra_fps_btn,
            self.ui.extreme_fps_btn,
            self.ui.fps90_fps_btn,
            self.ui.fps120_fps_btn
        ]
        self.fps_value = self.app.get_fps()

        for button in self.fps_buttons:
            if button.text() == self.fps_value:
                button.setChecked(True)
                break

        self.style_buttons = [
            self.ui.classic_style_btn,
            self.ui.colorful_style_btn,
            self.ui.realistic_style_btn,
            self.ui.soft_style_btn,
            self.ui.movie_style_btn
        ]
        battle_style_dict = {
            b'\x01': "Classic",
            b'\x02': "Colorful",
            b'\x03': "Realistic",
            b'\x04': "Soft",
            b'\x06': "Movie"
        }

        for button, style_id in zip(self.style_buttons, battle_style_dict.values()):
            button.setProperty("styleId", style_id)

        self.style_value = self.app.get_graphics_style()

        for button in self.style_buttons:
            if self.style_value.lower() in button.objectName():
                button.setChecked(True)
                break

        self.shadow_buttons = [
            self.ui.disable_shadow_btn,
            self.ui.enable_shadow_btn
        ]
        self.shadow_value = self.app.get_shadow()

        for button in self.shadow_buttons:
            if button.text() == self.shadow_value:
                button.setChecked(True)
                break

        if self.app.pubg_package == "com.pubg.krmobile":
            self.ui.ResolutionkrFrame.setVisible(True)
            self.ui.resolution_btn.setChecked(True)

        # Restore user's last chosen profile so they don't need to re-select each time.
        self.apply_saved_profile()
        self.gfx_buttons(enabled=True)

    def save_user_profile(self):
        profile = {
            "graphics": next((btn.text() for btn in self.graphics_buttons if btn.isChecked()), None),
            "fps": next((btn.text() for btn in self.fps_buttons if btn.isChecked()), None),
            "style": next((btn.property("styleId") for btn in self.style_buttons if btn.isChecked()), None),
            "shadow": next((btn.text() for btn in self.shadow_buttons if btn.isChecked()), None),
            "kr_resolution_1080p": bool(self.ui.resolution_btn.isChecked()),
        }
        self.app.settings.setValue(self.GFX_PROFILE_KEY, json.dumps(profile))

    def apply_saved_profile(self):
        raw_profile = self.app.settings.value(self.GFX_PROFILE_KEY)
        if not raw_profile:
            return
        try:
            profile = json.loads(raw_profile)
        except (TypeError, ValueError, json.JSONDecodeError):
            return

        graphics = profile.get("graphics")
        if graphics:
            for btn in self.graphics_buttons:
                if btn.text() == graphics:
                    btn.setChecked(True)
                    break

        fps = profile.get("fps")
        if fps:
            for btn in self.fps_buttons:
                if btn.text() == fps:
                    btn.setChecked(True)
                    break

        style = profile.get("style")
        if style:
            for btn in self.style_buttons:
                if btn.property("styleId") == style:
                    btn.setChecked(True)
                    break

        shadow = profile.get("shadow")
        if shadow:
            for btn in self.shadow_buttons:
                if btn.text() == shadow:
                    btn.setChecked(True)
                    break

        if self.app.pubg_package == "com.pubg.krmobile":
            self.ui.resolution_btn.setChecked(bool(profile.get("kr_resolution_1080p", True)))

    def graphics_buttons_func(self):
        self.graphics_buttons = [
            self.ui.supersmooth_graphics_btn,
            self.ui.smooth_graphics_btn,
            self.ui.balanced_graphics_btn,
            self.ui.hd_graphics_btn,
            self.ui.hdr_graphics_btn,
            self.ui.ultrahd_graphics_btn,
            self.ui.uhd_graphics_btn
        ]
        for button in self.graphics_buttons:
            button.clicked.connect(lambda checked, btn=button: self.check_button_selected(self.graphics_buttons, btn))

    def fps_buttons_func(self):
        self.fps_buttons = [
            self.ui.low_fps_btn,
            self.ui.medium_fps_btn,
            self.ui.high_fps_btn,
            self.ui.ultra_fps_btn,
            self.ui.extreme_fps_btn,
            self.ui.fps90_fps_btn,
            self.ui.fps120_fps_btn
        ]
        for button in self.fps_buttons:
            button.clicked.connect(lambda checked, btn=button: self.check_button_selected(self.fps_buttons, btn))

    def style_buttons_func(self):
        self.ui.classic_style_btn.setProperty("styleId", "Classic")
        self.ui.colorful_style_btn.setProperty("styleId", "Colorful")
        self.ui.realistic_style_btn.setProperty("styleId", "Realistic")
        self.ui.soft_style_btn.setProperty("styleId", "Soft")
        self.ui.movie_style_btn.setProperty("styleId", "Movie")
        
        self.style_buttons = [
            self.ui.classic_style_btn,
            self.ui.colorful_style_btn,
            self.ui.realistic_style_btn,
            self.ui.soft_style_btn,
            self.ui.movie_style_btn
        ]
        for button in self.style_buttons:
            button.clicked.connect(lambda checked, btn=button: self.check_button_selected(self.style_buttons, btn))

    def shadow_buttons_func(self):
        self.shadow_buttons = [
            self.ui.disable_shadow_btn,
            self.ui.enable_shadow_btn
        ]
        for button in self.shadow_buttons:
            button.clicked.connect(lambda checked, btn=button: self.check_button_selected(self.shadow_buttons, btn))

    @staticmethod
    def check_button_selected(buttons, clicked_button):
        for button in buttons:
            button.setChecked(button is clicked_button)

    def gfx_buttons(self, enabled: bool):
        buttons = [
            self.ui.supersmooth_graphics_btn,
            self.ui.smooth_graphics_btn,
            self.ui.balanced_graphics_btn,
            self.ui.hd_graphics_btn,
            self.ui.hdr_graphics_btn,
            self.ui.ultrahd_graphics_btn,
            self.ui.uhd_graphics_btn,
            self.ui.low_fps_btn,
            self.ui.medium_fps_btn,
            self.ui.high_fps_btn,
            self.ui.ultra_fps_btn,
            self.ui.extreme_fps_btn,
            self.ui.fps90_fps_btn,
            self.ui.fps120_fps_btn,
            self.ui.classic_style_btn,
            self.ui.colorful_style_btn,
            self.ui.realistic_style_btn,
            self.ui.soft_style_btn,
            self.ui.movie_style_btn,
            self.ui.disable_shadow_btn,
            self.ui.enable_shadow_btn,
            self.ui.submit_gfx_btn
        ]

        for button in buttons:
            button.setEnabled(enabled)
            if not enabled:
                button.setChecked(enabled)
