import json
from PyQt5.QtCore import QObject, QTimer, QThread, pyqtSignal

class AIOptimizeThread(QThread):
    """Worker thread for AI-based optimization to avoid blocking the UI."""
    task_completed = pyqtSignal(dict, dict)   # settings, specs
    task_failed = pyqtSignal(str)             # error message

    def __init__(self, app):
        super(AIOptimizeThread, self).__init__()
        self.app = app

    def run(self):
        import pythoncom
        try:
            pythoncom.CoInitialize()
            settings, specs = self.app.ai_smart_optimize()
            self.task_completed.emit(settings, specs)
        except Exception as e:
            self.task_failed.emit(str(e))
        finally:
            try:
                pythoncom.CoUninitialize()
            except Exception:
                pass


class GameloopSettingsUI(QObject):
    ENGINE_PROFILE_KEY = "engine/last_profile"

    def __init__(self, window):
        super(GameloopSettingsUI, self).__init__()
        self.app = window
        self.ui = window.ui

        self.checkboxes = {
            "LocalShaderCacheEnabled": self.ui.gl_cb_render_cache,
            "ShaderCacheEnabled": self.ui.gl_cb_force_global,
            "GraphicsCardEnabled": self.ui.gl_cb_prioritize_gpu,
            "RenderOptimizeEnabled": self.ui.gl_cb_render_opt,
            "VSyncEnabled": self.ui.gl_cb_vsync,
            "AdbDisable": self.ui.gl_cb_adb,       # 0 means Enable adb Debugging, 1 means disabled
            "RootAuthority": self.ui.gl_cb_root
        }

        self.mem_map = {0: "Auto", 1: "1024M", 2: "1536M", 3: "2048M", 4: "4096M", 5: "8192M"}
        self.cpu_map = {0: "Auto", 1: "1", 2: "2", 3: "4", 4: "8"}
        self.res_map = {
            0: "1024x576", 1: "1280x720", 2: "1366x768", 
            3: "1600x900", 4: "1920x1080", 5: "2560x1440"
        }
        self.dpi_map = {0: "120", 1: "160", 2: "240", 3: "320", 4: "480"}
        
        # Connect Actions
        self.ui.gameloop_save_btn.clicked.connect(self.save_settings)
        self.ui.gameloop_smart_btn.clicked.connect(self.smart_optimize)
        
        # Populate values when initialized
        self.load_settings()
        self.auto_restore_saved_profile()

    def _save_profile(self, profile):
        self.app.settings.setValue(self.ENGINE_PROFILE_KEY, json.dumps(profile))

    def _load_profile(self):
        raw = self.app.settings.value(self.ENGINE_PROFILE_KEY)
        if not raw:
            return None
        try:
            return json.loads(raw)
        except (TypeError, ValueError, json.JSONDecodeError):
            return None

    def _profile_from_registry(self):
        return {
            "GraphicsRenderAuto": int(self.app.get_reg("GraphicsRenderAuto") or 0),
            "ForceDirectX": int(self.app.get_reg("ForceDirectX") or 0),
            "LocalShaderCacheEnabled": int(self.app.get_reg("LocalShaderCacheEnabled") or 0),
            "ShaderCacheEnabled": int(self.app.get_reg("ShaderCacheEnabled") or 0),
            "GraphicsCardEnabled": int(self.app.get_reg("GraphicsCardEnabled") or 0),
            "RenderOptimizeEnabled": int(self.app.get_reg("RenderOptimizeEnabled") or 0),
            "VSyncEnabled": int(self.app.get_reg("VSyncEnabled") or 0),
            "AdbDisable": int(self.app.get_reg("AdbDisable") or 0),
            "RootAuthority": int(self.app.get_reg("RootAuthority") or 0),
            "FxaaQuality": int(self.app.get_reg("FxaaQuality") or 0),
            "VMMemorySizeInMB": int(self.app.get_reg("VMMemorySizeInMB") or 0),
            "VMCpuCount": int(self.app.get_reg("VMCpuCount") or 0),
            "VMDPI": int(self.app.get_reg("VMDPI") or 160),
            "VMResWidth": int(self.app.get_reg("VMResWidth") or 1280),
            "VMResHeight": int(self.app.get_reg("VMResHeight") or 720),
        }

    def _apply_profile(self, profile):
        for key, value in profile.items():
            self.app.set_dword(key, int(value))

    def auto_restore_saved_profile(self):
        saved_profile = self._load_profile()
        if not saved_profile:
            return

        current_profile = self._profile_from_registry()
        if saved_profile != current_profile:
            self._apply_profile(saved_profile)
            self.load_settings()
            self.app.show_status_message("Saved engine profile auto-restored.")

    def smart_optimize(self):
        """Start AI-powered optimization in a background thread."""
        self.ui.gameloop_smart_btn.setEnabled(False)
        self.ui.gameloop_smart_btn.setText("\U0001f916 Analyzing System with AI...")
        self.app.show_status_message("Sending system specs to AI for analysis...", 60)

        self._ai_worker = AIOptimizeThread(self.app)
        self._ai_worker.task_completed.connect(self._ai_optimize_done)
        self._ai_worker.task_failed.connect(self._ai_optimize_failed)
        self._ai_worker.start()

    def _ai_optimize_done(self, settings, specs):
        """Apply settings returned by the AI model."""
        try:
            for key, value in settings.items():
                self.app.set_dword(key, int(value))

            self.load_settings()
            self._save_profile(self._profile_from_registry())

            specs_summary = (
                f"CPU: {specs.get('cpu_cores_physical', '?')} cores | "
                f"RAM: {specs.get('ram_total_gb', '?')} GB | "
                f"GPU: {specs.get('gpu_name', 'Unknown')}"
            )
            self.app.show_status_message(
                f"AI Optimization Complete! ({specs_summary})"
            )
            self.ui.gameloop_smart_btn.setText("AI Optimized! \u2713")
        except Exception as e:
            self.app.logger.error(f"AI optimization apply failed: {e}")
            self.app.show_status_message(f"Failed to apply AI settings: {e}")
            self.ui.gameloop_smart_btn.setText("Failed! \u2717")

        QTimer.singleShot(3000, self.reset_smart_btn)

    def _ai_optimize_failed(self, error):
        """Fall back to the local hardware-based optimizer when AI fails."""
        self.app.logger.error(f"AI optimization failed: {error}")
        self.app.show_status_message(
            "AI unavailable \u2014 falling back to local optimization...", 5
        )

        try:
            self.app.gameloop_settings()
            self.load_settings()
            self._save_profile(self._profile_from_registry())
            self.app.show_status_message(
                "Local optimization applied (AI was unavailable)."
            )
            self.ui.gameloop_smart_btn.setText("Optimized (Local) \u2713")
        except Exception as e:
            self.app.show_status_message(f"Optimization failed: {e}")
            self.ui.gameloop_smart_btn.setText("Failed! \u2717")

        QTimer.singleShot(3000, self.reset_smart_btn)

    def reset_smart_btn(self):
        self.ui.gameloop_smart_btn.setText("Smart Optimize")
        self.ui.gameloop_smart_btn.setEnabled(True)

    def get_index_by_val(self, mapping, value):
        if value is None:
            return 0
        for index, item in mapping.items():
            if str(item) == str(value):
                return index
        return 0

    def get_res_index(self, width, height):
        res_str = f"{width}x{height}"
        return self.get_index_by_val(self.res_map, res_str)

    def load_settings(self):
        # 1. Screen Rendering Mode
        auto_render = self.app.get_reg("GraphicsRenderAuto")
        if auto_render == 1:
            self.ui.gl_render_auto.setChecked(True)
        else:
            render_mode = self.app.get_reg("ForceDirectX")
            if render_mode == 1:
                self.ui.gl_render_directx.setChecked(True)
            else:
                self.ui.gl_render_opengl.setChecked(True)

        # 2. Checkboxes
        for key, cb in self.checkboxes.items():
            val = self.app.get_reg(key)
            if val is None:
                val = 0  # Default value if registry key not found
            if key == "AdbDisable":  # AdbDisable=0 means ADB is Enabled
                cb.setChecked(val == 0)
            else:
                cb.setChecked(val == 1)

        # 3. Dropdowns
        aa_val = self.app.get_reg("FxaaQuality")
        if aa_val is None:
            aa_val = 0
        self.ui.gl_combo_aa.setCurrentIndex(aa_val if aa_val in [0, 1, 2] else 0)

        mem_val = self.app.get_reg("VMMemorySizeInMB")
        mem_str = "Auto" if (mem_val is None or mem_val == 0) else f"{mem_val}M"
        self.ui.gl_combo_mem.setCurrentIndex(self.get_index_by_val(self.mem_map, mem_str))

        cpu_val = self.app.get_reg("VMCpuCount")
        cpu_str = "Auto" if (cpu_val is None or cpu_val == 0) else str(cpu_val)
        self.ui.gl_combo_cpu.setCurrentIndex(self.get_index_by_val(self.cpu_map, cpu_str))

        dpi_val = self.app.get_reg("VMDPI")
        if dpi_val is None:
            dpi_val = 160
        self.ui.gl_combo_dpi.setCurrentIndex(self.get_index_by_val(self.dpi_map, str(dpi_val)))

        width = self.app.get_reg("VMResWidth")
        height = self.app.get_reg("VMResHeight")
        if width is None:
            width = 1280
        if height is None:
            height = 720
        self.ui.gl_combo_res.setCurrentIndex(self.get_res_index(width, height))

    def save_settings(self):
        self.ui.gameloop_save_btn.setEnabled(False)
        original_text = "Save Engine Settings"
        self.ui.gameloop_save_btn.setText("Saving Engine...")
        
        try:
            # Screen rendering mode
            if self.ui.gl_render_auto.isChecked():
                self.app.set_dword("GraphicsRenderAuto", 1)
                self.app.set_dword("ForceDirectX", 0)
            elif self.ui.gl_render_directx.isChecked():
                self.app.set_dword("GraphicsRenderAuto", 0)
                self.app.set_dword("ForceDirectX", 1)
            else:
                self.app.set_dword("GraphicsRenderAuto", 0)
                self.app.set_dword("ForceDirectX", 0)
                
            # Checkboxes
            for key, cb in self.checkboxes.items():
                if key == "AdbDisable":  # AdbDisable=0 means ADB is Enabled
                    self.app.set_dword(key, 0 if cb.isChecked() else 1)
                else:
                    self.app.set_dword(key, 1 if cb.isChecked() else 0)
                    
            # Dropdowns
            self.app.set_dword("FxaaQuality", self.ui.gl_combo_aa.currentIndex())
            
            mem_str = self.ui.gl_combo_mem.currentText()
            mem_val = 0 if mem_str == "Auto" else int(mem_str.replace("M", ""))
            self.app.set_dword("VMMemorySizeInMB", mem_val)
            
            cpu_str = self.ui.gl_combo_cpu.currentText()
            cpu_val = 0 if cpu_str == "Auto" else int(cpu_str)
            self.app.set_dword("VMCpuCount", cpu_val)
            
            dpi_str = self.ui.gl_combo_dpi.currentText()
            self.app.set_dword("VMDPI", int(dpi_str))
            
            res_str = self.ui.gl_combo_res.currentText()
            width, height = map(int, res_str.split("x"))
            self.app.set_dword("VMResWidth", width)
            self.app.set_dword("VMResHeight", height)
            self._save_profile(self._profile_from_registry())
            
            self.app.show_status_message("Engine Settings Applied! Restart Gameloop.")
            self.ui.gameloop_save_btn.setText("Success! ✓")
            
        except Exception as e:
            self.app.logger.error(f"Error saving engine settings: {e}")
            self.app.show_status_message("Failed to save settings!")
            self.ui.gameloop_save_btn.setText("Error! ✗")

        # Reset button after 2 seconds
        QTimer.singleShot(2000, lambda: self.reset_save_btn(original_text))

    def reset_save_btn(self, text):
        self.ui.gameloop_save_btn.setText(text)
        self.ui.gameloop_save_btn.setEnabled(True)
