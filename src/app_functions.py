import os
import shutil
import subprocess
import sys
import winreg
import xml.etree.ElementTree as ET
from shutil import copy
from time import sleep

import GPUtil
import adbutils
import psutil
import pythoncom
import tempfile
import winshell
import wmi
from PyQt5.QtCore import QSettings
from win32api import EnumDisplayDevices, EnumDisplaySettings
from win32com.client import Dispatch
from . import setup_logger


class Settings:
    def __init__(self):
        self.settings = QSettings("Mo-Tech", "Mo-Tech")
        self.REG_PATH = r'SOFTWARE\Tencent\MobileGamePC'
        self.pubg_versions = {
            "com.tencent.ig": "PUBG Mobile Global",
            "com.vng.pubgmobile": "PUBG Mobile VN",
            "com.rekoo.pubgm": "PUBG Mobile TW",
            "com.pubg.krmobile": "PUBG Mobile KR",
            "com.pubg.imobile": "Battlegrounds Mobile India"}
        self.logger = setup_logger('error_logger', 'error.log')

    @staticmethod
    def kill_adb():
        """
        Kills the ADB (Android Debug Bridge) process if it is currently running.
        """
        try:
            subprocess.run(["taskkill", "/F", "/IM", "adb.exe"], check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    # Get Script Run Location
    @staticmethod
    def resource_path(relative_path):
        base_path = getattr(sys, '_MEIPASS', os.path.abspath('.'))
        return os.path.join(base_path, relative_path)


class Registry(Settings):
    def get_reg(self, name):
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.REG_PATH, 0, winreg.KEY_READ) as registry_key:
                value, regtype = winreg.QueryValueEx(registry_key, name)
                return value
        except FileNotFoundError:
            return None

    @staticmethod
    def get_local_reg(name, path="AppMarket"):
        """
        Get the value of a registry key in the local machine.
        """
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                rf'SOFTWARE\WOW6432Node\Tencent\MobileGamePC\{path}') as registry_key:
                value, regtype = winreg.QueryValueEx(registry_key, name)
                return value
        except OSError:
            return None

    def set_dword(self, name, value):
        """
        Set the value of a DWORD in the Windows registry.
        """
        try:
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, self.REG_PATH) as registry_key:
                winreg.SetValueEx(registry_key, name, 0, winreg.REG_DWORD, value)
            return True
        except WindowsError:
            return False

    def set_string(self, name, value):
        """
        Set the value of a String in the Windows registry.
        """
        try:
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, self.REG_PATH) as registry_key:
                winreg.SetValueEx(registry_key, name, 0, winreg.REG_SZ, value)
            return True
        except WindowsError:
            return False


class Optimizer(Registry):

    def temp_cleaner(self):
        """
        Cleans temporary files and directories.

        Returns:
            bool: True if the function successfully cleans the temporary files and directories.
        """
        base_path = getattr(sys, '_MEIPASS', os.path.abspath('.'))

        def clear_files(directory):
            try:
                for root, dirs, files in os.walk(directory):
                    for name in files:
                        os.remove(os.path.join(root, name))
                    for name in dirs:
                        shutil.rmtree(os.path.join(root, name))
            except Exception:
                pass

        # Clean user-level temp files normally
        try:
            for folder in os.listdir(tempfile.gettempdir()):
                folder_path = os.path.join(tempfile.gettempdir(), folder)
                if folder_path != base_path:
                    if os.path.isdir(folder_path):
                        shutil.rmtree(folder_path, ignore_errors=True)
                    else:
                        try:
                            os.remove(folder_path)
                        except Exception:
                            pass
        except Exception:
            pass

        # Clean protected system folders using elevated shell commands
        protected_paths = [
            r"C:\Windows\Temp",
            os.path.expandvars(r'%windir%\Prefetch')
        ]
        
        for path in protected_paths:
            if os.path.exists(path):
                # /s deletes all files, /q is quiet mode, /f is force
                self._run_elevated("cmd.exe", fr'/c "del /q /f /s "{path}\*""')

        gameloop_ui_path = self.get_local_reg('InstallPath', path='UI')
        if gameloop_ui_path:
            shader_cache = os.path.join(gameloop_ui_path, 'ShaderCache')
            if os.path.exists(shader_cache):
                # Use elevation for shader cache as it's often in protected Program Files
                self._run_elevated("cmd.exe", f'/c "rd /s /q "{shader_cache}""')
                os.makedirs(shader_cache, exist_ok=True)

        return True

    def gameloop_settings(self):
        """
        Generates the game loop settings based on the system's hardware specifications.
        """

        def make_scale(value, low=False):
            for version_key in self.pubg_versions.keys():
                content_scale_key = f"{version_key}_ContentScale"
                render_quality_key = f"{version_key}_RenderQuality"
                fps_level_key = f"{version_key}_FPSLevel"

                reg_content_scale = self.get_reg(content_scale_key)
                if reg_content_scale is not None:
                    self.set_dword(content_scale_key, value)

                reg_fps_level = self.get_reg(fps_level_key)
                if reg_fps_level is not None:
                    self.set_dword(fps_level_key, 0)

                reg_render_quality = self.get_reg(render_quality_key)
                if reg_render_quality is not None:
                    render_value = value
                    if low:
                        # value = 0
                        render_value = 2
                    elif value == 1:
                        render_value = 2
                    self.set_dword(render_quality_key, render_value)

        ram_value = round((int(75) * psutil.virtual_memory().total / (1024 ** 3)) / 100) * 1024
        ram_value = min(ram_value, (8 * 1024))

        cpu_value = round((int(75) * psutil.cpu_count(logical=False)) / 100)
        cpu_value = min(cpu_value, 8)

        try:
            dc = EnumDisplayDevices(None, 0, 0)
            settings = EnumDisplaySettings(dc.DeviceName, -1)
            refresh_rate = settings.DisplayFrequency
            self.set_dword("VSyncEnabled", 1 if refresh_rate < 89 else 0)
        except Exception as e:
            self.logger.warning(f"Could not detect display refresh rate: {e}")
            self.set_dword("VSyncEnabled", 0)  # Default to off

        gpus = GPUtil.getGPUs()
        gpu = gpus[0] if gpus else None
        if gpu:
            gpu_memory = int(gpu.memoryTotal / 1024)
            self.set_dword("SetGraphicsCard", 1)
            if gpu_memory < 4:
                self.set_dword("VMDPI", 240)
                self.set_dword("FxaaQuality", 0)

                if gpu_memory <= 2:
                    self.set_dword("LocalShaderCacheEnabled", 0)
                    self.set_dword("ShaderCacheEnabled", 0)
                    make_scale(1, low=True)
                else:
                    self.set_dword("LocalShaderCacheEnabled", 1)
                    self.set_dword("ShaderCacheEnabled", 1)
                    make_scale(1)

            elif gpu_memory < 8 and cpu_value <= 4:
                self.set_dword("LocalShaderCacheEnabled", 1)
                self.set_dword("ShaderCacheEnabled", 1)
                self.set_dword("VMDPI", 480)
                self.set_dword("FxaaQuality", 2 if cpu_value == 4 else 1)
                make_scale(1)
            else:
                self.set_dword("LocalShaderCacheEnabled", 1)
                self.set_dword("ShaderCacheEnabled", 1)
                self.set_dword("VMDPI", 480)
                self.set_dword("FxaaQuality", 2)
                make_scale(2)

            self.set_dword("GraphicsCardEnabled", 1)

        else:
            self.set_dword("GraphicsCardEnabled", 0)
            self.set_dword("LocalShaderCacheEnabled", 0)
            self.set_dword("ShaderCacheEnabled", 0)
            self.set_dword("VMDPI", 240)
            self.set_dword("FxaaQuality", 0)
            make_scale(1, low=True)

        self.set_dword("ForceDirectX", 1)
        self.set_dword("RenderOptimizeEnabled", 1)
        self.set_dword("AdbDisable", 0)
        self.set_dword("VMMemorySizeInMB", ram_value)
        self.set_dword("VMCpuCount", cpu_value)

        self.set_string("VMDeviceManufacturer", "samsung")
        self.set_string("VMDeviceModel", "SM-S928B")
        self.set_dword("VMScreenFPS", 120)

    def add_to_windows_defender_exclusion(self):
        """
        Adds the directory of the game loop to the Windows Defender exclusion list.
        """
        try:
            install_path = self.get_local_reg("InstallPath")
            if not install_path:
                return False
            gameloop_path = os.path.dirname(install_path)
            # Add-MpPreference requires admin elevation
            ps_command = f"Add-MpPreference -ExclusionPath '{gameloop_path}' -Force"
            self._run_elevated("powershell.exe", f'-Command "{ps_command}"')
        except Exception:
            return False
        return True

    @staticmethod
    def _run_elevated(exe, params=""):
        """Run a command with admin privileges using ShellExecuteW runas."""
        import ctypes
        result = ctypes.windll.shell32.ShellExecuteW(
            None, "runas", exe, params, None, 0  # 0 = SW_HIDE
        )
        return result > 32  # ShellExecute returns > 32 on success

    def optimize_gameloop_registry(self):
        try:
            install_path = self.get_local_reg("InstallPath", path="UI")
            registry_keys = [
                'AndroidEmulator.exe',
                'AndroidEmulatorEn.exe',
                'AndroidEmulatorEx.exe',
                'aow_exe.exe',
            ]
            base_key = r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options'
            value_name = 'CpuPriorityClass'
            value_data = '3'

            # HKLM commands require elevation - run via ShellExecuteW runas
            for key in registry_keys:
                full_key = fr"{base_key}\{key}\PerfOptions"
                params = f'ADD "{full_key}" /v {value_name} /t REG_DWORD /d {value_data} /f'
                self._run_elevated("reg.exe", params)

            # HKCU commands don't need elevation - run normally
            registry_entries = [
                (
                    r'HKEY_CURRENT_USER\Software\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers',
                    '~ DISABLEDXMAXIMIZEDWINDOWEDMODE HIGHDPIAWARE'
                ),
                (
                    r'HKEY_CURRENT_USER\SOFTWARE\Microsoft\DirectX\UserGpuPreferences',
                    'GpuPreference=2;'
                )
            ]

            for registry_key, value in registry_entries:
                for key in registry_keys:
                    command = [
                        'reg', 'ADD', registry_key,
                        '/v', fr'{install_path}\{key}',
                        '/t', 'REG_SZ',
                        '/d', value,
                        '/f'
                    ]
                    subprocess.run(command, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception as e:
            self.logger.error(f"Exception occurred: {str(e)}", exc_info=True)

    def force_dedicated_gpu(self):
        """
        Forces Gameloop to use the dedicated GPU (NVIDIA/AMD) instead of integrated GPU.
        Uses multiple methods for maximum compatibility.
        """
        try:
            install_path = self.get_local_reg("InstallPath", path="UI")
            if not install_path:
                self.logger.warning("Gameloop install path not found")
                return False

            # --- Method 1: Windows Graphics Preferences (GpuPreference=2 = High Performance) ---
            # Scan ALL executables in the Gameloop directory
            gpu_pref_key = r'HKEY_CURRENT_USER\SOFTWARE\Microsoft\DirectX\UserGpuPreferences'
            exe_files = []
            for root, dirs, files in os.walk(install_path):
                for f in files:
                    if f.lower().endswith('.exe'):
                        exe_files.append(os.path.join(root, f))

            for exe_path in exe_files:
                command = [
                    'reg', 'ADD', gpu_pref_key,
                    '/v', exe_path,
                    '/t', 'REG_SZ',
                    '/d', 'GpuPreference=2;',
                    '/f'
                ]
                subprocess.run(command, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            # --- Method 2: Gameloop's own registry keys for GPU selection ---
            self.set_dword("SetGraphicsCard", 1)       # Force dedicated GPU
            self.set_dword("GraphicsCardEnabled", 1)    # Enable GPU acceleration
            self.set_dword("ForceDirectX", 1)           # Force DirectX rendering
            self.set_dword("RenderOptimizeEnabled", 1)  # Enable render optimization

            # Set GPU preference for each PUBG version
            for version_key in self.pubg_versions.keys():
                gpu_key = f"{version_key}_GPU"
                self.set_dword(gpu_key, 1)  # 1 = dedicated GPU

            # --- Method 3: NVIDIA Optimus & AMD PowerXpress settings ---
            # Force NVIDIA GPU as default for Gameloop executables
            try:
                optimus_key = r'HKEY_LOCAL_MACHINE\SOFTWARE\NVIDIA Corporation\Global\NVTweak'
                params = f'ADD "{optimus_key}" /v NvCplGlobalDisplayType /t REG_DWORD /d 1 /f'
                self._run_elevated("reg.exe", params)
            except Exception:
                pass  # Not an NVIDIA GPU

            # AMD PowerXpress setting (if AMD GPU)
            try:
                amd_key = r'HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}\0000'
                params = f'ADD "{amd_key}" /v PowerSavingPolicy /t REG_DWORD /d 2 /f'
                self._run_elevated("reg.exe", params)
            except Exception:
                pass  # Not an AMD GPU

            # --- Method 4: Windows AppCompat Layers - disable DWM and force GPU ---
            layers_key = r'HKEY_CURRENT_USER\Software\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers'
            core_exes = [
                'AndroidEmulator.exe', 'AndroidEmulatorEn.exe',
                'AndroidEmulatorEx.exe', 'aow_exe.exe',
            ]
            for exe_name in core_exes:
                full_path = os.path.join(install_path, exe_name)
                if os.path.exists(full_path):
                    command = [
                        'reg', 'ADD', layers_key,
                        '/v', full_path,
                        '/t', 'REG_SZ',
                        '/d', '~ DISABLEDXMAXIMIZEDWINDOWEDMODE HIGHDPIAWARE',
                        '/f'
                    ]
                    subprocess.run(command, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            self.logger.info("Successfully forced dedicated GPU")
            return True
        except Exception as e:
            self.logger.error(f"Exception occurred in force_dedicated_gpu: {str(e)}", exc_info=True)
            return False

    def optimize_cpu_usage(self):
        """
        Optimizes CPU usage for Gameloop by setting process priorities,
        affinity, and reducing unnecessary CPU overhead.
        """
        try:
            install_path = self.get_local_reg("InstallPath", path="UI")
            if not install_path:
                self.logger.warning("Gameloop install path not found")
                return False

            # --- Method 1: Set CPU priority to High (not Realtime to avoid system instability) ---
            registry_keys = [
                'AndroidEmulator.exe',
                'AndroidEmulatorEn.exe',
                'AndroidEmulatorEx.exe',
                'aow_exe.exe',
            ]
            base_key = r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options'
            value_name = 'CpuPriorityClass'
            value_data = '3'  # 3 = High priority (below Realtime)

            for key in registry_keys:
                full_key = fr"{base_key}\{key}\PerfOptions"
                params = f'ADD "{full_key}" /v {value_name} /t REG_DWORD /d {value_data} /f'
                self._run_elevated("reg.exe", params)

            # --- Method 2: Set IO Priority to High for better disk access ---
            for key in registry_keys:
                full_key = fr"{base_key}\{key}\PerfOptions"
                # IoPriority: 0=VeryLow, 1=Low, 2=Normal, 3=High
                params = f'ADD "{full_key}" /v IoPriority /t REG_DWORD /d 3 /f'
                self._run_elevated("reg.exe", params)

            # --- Method 3: Set Page Priority to High ---
            for key in registry_keys:
                full_key = fr"{base_key}\{key}\PerfOptions"
                # PagePriority: 0=Normal, 1=High
                params = f'ADD "{full_key}" /v PagePriority /t REG_DWORD /d 1 /f'
                self._run_elevated("reg.exe", params)

            # --- Method 4: Optimize Gameloop CPU allocation ---
            # Set CPU cores to 75% of available (prevents over-allocation)
            cpu_count = psutil.cpu_count(logical=False) or 4
            optimal_cores = max(2, int(cpu_count * 0.75))
            optimal_cores = min(optimal_cores, 8)  # Cap at 8 cores
            self.set_dword("VMCpuCount", optimal_cores)

            # --- Method 5: Disable unnecessary background features ---
            # Disable ADB when not in use (saves CPU cycles)
            # Note: We'll enable it temporarily when needed
            # self.set_dword("AdbDisable", 0)  # Keep enabled for tool functionality

            # Disable root authority (security + performance)
            self.set_dword("RootAuthority", 0)

            # --- Method 6: Optimize Windows for gaming performance ---
            # Set power plan to High Performance (requires elevation)
            try:
                # GUID for High Performance power plan: 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c
                ps_command = "powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"
                self._run_elevated("cmd.exe", f'/c "{ps_command}"')
            except Exception as e:
                self.logger.warning(f"Could not set power plan: {e}")

            # Disable Nagle's algorithm for lower latency (gaming optimization)
            try:
                nagle_key = r'HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces'
                # We'll skip this as it requires iterating all network adapters
                # and can cause network issues
            except Exception:
                pass

            self.logger.info(f"CPU optimized: {optimal_cores} cores allocated")
            return True
        except Exception as e:
            self.logger.error(f"Exception occurred in optimize_cpu_usage: {str(e)}", exc_info=True)
            return False

    def force_gpu_and_optimize_cpu(self):
        """
        Combined function that forces dedicated GPU and optimizes CPU usage.
        This is the recommended one-click solution.
        """
        try:
            # Step 1: Force dedicated GPU
            gpu_success = self.force_dedicated_gpu()
            
            # Step 2: Optimize CPU usage
            cpu_success = self.optimize_cpu_usage()
            
            # Step 3: Apply Gameloop settings for optimal performance
            self.gameloop_settings()
            
            # Step 4: Optimize registry for performance
            self.optimize_gameloop_registry()
            
            if gpu_success and cpu_success:
                return True
            return False
        except Exception as e:
            self.logger.error(f"Exception in force_gpu_and_optimize_cpu: {str(e)}", exc_info=True)
            return False

    def install_essential_drivers(self):
        """
        Downloads and installs essential drivers/runtimes required by the emulator:
        1. Visual C++ Redistributable 2015-2022 (x64)
        2. Visual C++ Redistributable 2015-2022 (x86)
        3. Opens the appropriate GPU driver download page based on detected GPU.
        """
        import urllib.request
        import webbrowser

        results = []
        temp_dir = os.path.join(tempfile.gettempdir(), "motech_drivers")
        os.makedirs(temp_dir, exist_ok=True)

        drivers = [
            {
                "name": "VC++ Redistributable x64",
                "url": "https://aka.ms/vs/17/release/vc_redist.x64.exe",
                "filename": "vc_redist.x64.exe",
                "args": "/install /quiet /norestart"
            },
            {
                "name": "VC++ Redistributable x86",
                "url": "https://aka.ms/vs/17/release/vc_redist.x86.exe",
                "filename": "vc_redist.x86.exe",
                "args": "/install /quiet /norestart"
            }
        ]

        for driver in drivers:
            try:
                filepath = os.path.join(temp_dir, driver["filename"])
                urllib.request.urlretrieve(driver["url"], filepath)
                self._run_elevated(filepath, driver["args"])
                sleep(8)  # Give the installer time to complete
                results.append(f'{driver["name"]} ✓')
            except Exception as e:
                results.append(f'{driver["name"]} ✗')
                self.logger.error(f'{driver["name"]} install failed: {e}', exc_info=True)

        # Open GPU driver download page based on detected GPU
        try:
            gpu_controllers = wmi.WMI().Win32_VideoController()
            gpu = gpu_controllers[0] if gpu_controllers else None
            if gpu:
                gpu_compat = (gpu.AdapterCompatibility or "").upper()
                if "NVIDIA" in gpu_compat:
                    webbrowser.open("https://www.nvidia.com/Download/index.aspx")
                    results.append("NVIDIA driver page opened")
                elif "AMD" in gpu_compat or "ATI" in gpu_compat:
                    webbrowser.open("https://www.amd.com/en/support")
                    results.append("AMD driver page opened")
                elif "INTEL" in gpu_compat:
                    webbrowser.open("https://www.intel.com/content/www/us/en/download-center/home.html")
                    results.append("Intel driver page opened")
        except Exception as e:
            self.logger.error(f"GPU driver page detection failed: {e}", exc_info=True)

        # Clean up temp files
        try:
            shutil.rmtree(temp_dir, ignore_errors=True)
        except Exception:
            pass

        return ", ".join(results) if results else "No drivers installed"

    def get_system_specs(self):
        """Collect detailed system hardware specifications for AI analysis."""
        specs = {}

        # CPU info
        specs['cpu_cores_physical'] = psutil.cpu_count(logical=False) or 2
        specs['cpu_cores_logical'] = psutil.cpu_count(logical=True) or 4
        try:
            cpu = wmi.WMI().Win32_Processor()[0]
            specs['cpu_name'] = cpu.Name.strip()
        except Exception:
            specs['cpu_name'] = 'Unknown CPU'

        # RAM
        ram = psutil.virtual_memory()
        specs['ram_total_gb'] = round(ram.total / (1024 ** 3), 1)

        # GPU
        gpus = GPUtil.getGPUs()
        if gpus:
            gpu = gpus[0]
            specs['gpu_name'] = gpu.name
            specs['gpu_memory_mb'] = int(gpu.memoryTotal)
        else:
            try:
                gpu_ctrl = wmi.WMI().Win32_VideoController()[0]
                specs['gpu_name'] = gpu_ctrl.Name or 'Unknown'
                specs['gpu_memory_mb'] = int((gpu_ctrl.AdapterRAM or 0) / (1024 * 1024))
            except Exception:
                specs['gpu_name'] = 'Integrated/Unknown'
                specs['gpu_memory_mb'] = 0

        # Display
        try:
            dc = EnumDisplayDevices(None, 0, 0)
            settings = EnumDisplaySettings(dc.DeviceName, -1)
            specs['display_refresh_rate'] = settings.DisplayFrequency
            specs['display_resolution'] = f"{settings.PelsWidth}x{settings.PelsHeight}"
        except Exception:
            specs['display_refresh_rate'] = 60
            specs['display_resolution'] = 'Unknown'

        return specs

    def ai_smart_optimize(self):
        """
        Use AI (via OpenRouter API) to analyze system specs and determine
        the optimal Gameloop emulator settings.
        Returns: (settings_dict, specs_dict)
        """
        import json
        import urllib.request
        import urllib.error

        specs = self.get_system_specs()

        prompt = (
            "You are an expert in Gameloop Android emulator optimization for PUBG Mobile gaming.\n"
            "Based on the following system specs, recommend the optimal emulator settings.\n\n"
            "System Specifications:\n"
            f"- CPU: {specs['cpu_name']} ({specs['cpu_cores_physical']} physical cores, "
            f"{specs['cpu_cores_logical']} logical cores)\n"
            f"- RAM: {specs['ram_total_gb']} GB total\n"
            f"- GPU: {specs['gpu_name']} ({specs['gpu_memory_mb']} MB VRAM)\n"
            f"- Display: {specs['display_resolution']} @ {specs['display_refresh_rate']}Hz\n\n"
            "Respond with ONLY a valid JSON object (no markdown, no explanation) with these keys:\n"
            "{\n"
            '  "GraphicsRenderAuto": 0 or 1,\n'
            '  "ForceDirectX": 0 or 1,\n'
            '  "LocalShaderCacheEnabled": 0 or 1,\n'
            '  "ShaderCacheEnabled": 0 or 1,\n'
            '  "GraphicsCardEnabled": 0 or 1,\n'
            '  "RenderOptimizeEnabled": 0 or 1,\n'
            '  "VSyncEnabled": 0 or 1,\n'
            '  "AdbDisable": 0 or 1,\n'
            '  "RootAuthority": 0 or 1,\n'
            '  "FxaaQuality": 0 or 1 or 2 (0=Off, 1=Balanced, 2=Ultra),\n'
            f'  "VMMemorySizeInMB": one of [0,1024,1536,2048,4096,8192] (max 75% of {int(specs["ram_total_gb"]*1024)}MB),\n'
            f'  "VMCpuCount": one of [0,1,2,4,8] (max 75% of {specs["cpu_cores_physical"]} cores),\n'
            '  "VMDPI": one of [120,160,240,320,480],\n'
            '  "VMResWidth": one of [1024,1280,1366,1600,1920,2560],\n'
            '  "VMResHeight": matching [576,720,768,900,1080,1440]\n'
            "}\n\n"
            "Rules:\n"
            "- GPU VRAM<2GB: VMDPI=240, FxaaQuality=0\n"
            "- GPU VRAM 2-4GB: VMDPI=320, FxaaQuality=1\n"
            "- GPU VRAM>=4GB: VMDPI=480, FxaaQuality=2\n"
            "- VSyncEnabled=1 only if refresh rate<90Hz\n"
            "- ForceDirectX=1 recommended\n"
            "- AdbDisable=0 (keep ADB enabled)\n"
            "- GraphicsCardEnabled=1 if dedicated GPU\n"
            "- Valid resolution pairs: 1024x576, 1280x720, 1366x768, 1600x900, 1920x1080, 2560x1440\n"
        )

        api_key = "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"

        payload = json.dumps({
            "model": "nvidia/nemotron-3-super-120b-a12b:free",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.1,
            "max_tokens": 2000
        }).encode('utf-8')

        req = urllib.request.Request(
            "https://openrouter.ai/api/v1/chat/completions",
            data=payload,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://motech-tools.app",
                "X-Title": "MO-TECH TOOLS"
            }
        )

        # Make the API call with full error handling
        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                response_body = response.read().decode('utf-8')
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8', errors='replace')
            self.logger.error(f"OpenRouter API HTTP {e.code}: {error_body}")
            raise Exception(f"API returned HTTP {e.code}: {error_body[:300]}")
        except urllib.error.URLError as e:
            raise Exception(f"Network error: {e.reason}")

        response_body = response_body.strip()
        if not response_body:
            raise Exception("API returned an empty response")

        result = json.loads(response_body)

        # Check for API-level errors
        if 'error' in result:
            err_msg = result['error'] if isinstance(result['error'], str) else result['error'].get('message', str(result['error']))
            raise Exception(f"API error: {err_msg}")

        if 'choices' not in result or not result['choices']:
            self.logger.error(f"Unexpected API response: {response_body[:500]}")
            raise Exception("API returned no choices")

        ai_text = result['choices'][0]['message']['content']
        if not ai_text or not ai_text.strip():
            raise Exception("AI returned empty content")

        ai_text = ai_text.strip()
        self.logger.info(f"AI raw response: {ai_text[:500]}")

        # Parse JSON from AI response, handling potential markdown code blocks
        if '```json' in ai_text:
            ai_text = ai_text.split('```json')[1].split('```')[0].strip()
        elif '```' in ai_text:
            ai_text = ai_text.split('```')[1].split('```')[0].strip()

        settings = json.loads(ai_text)

        # Validate and sanitize all values
        valid_mem = [0, 1024, 1536, 2048, 4096, 8192]
        valid_cpu = [0, 1, 2, 4, 8]
        valid_dpi = [120, 160, 240, 320, 480]
        valid_res = {1024: 576, 1280: 720, 1366: 768, 1600: 900, 1920: 1080, 2560: 1440}

        if settings.get('VMMemorySizeInMB') not in valid_mem:
            settings['VMMemorySizeInMB'] = 0
        if settings.get('VMCpuCount') not in valid_cpu:
            settings['VMCpuCount'] = 0
        if settings.get('VMDPI') not in valid_dpi:
            settings['VMDPI'] = 240
        if settings.get('VMResWidth') not in valid_res:
            settings['VMResWidth'] = 1280
            settings['VMResHeight'] = 720
        else:
            settings['VMResHeight'] = valid_res[settings['VMResWidth']]

        # Ensure binary values are strictly 0 or 1
        for key in ['GraphicsRenderAuto', 'ForceDirectX', 'LocalShaderCacheEnabled',
                     'ShaderCacheEnabled', 'GraphicsCardEnabled', 'RenderOptimizeEnabled',
                     'VSyncEnabled', 'AdbDisable', 'RootAuthority']:
            settings[key] = 1 if settings.get(key) else 0

        if settings.get('FxaaQuality') not in [0, 1, 2]:
            settings['FxaaQuality'] = 0

        return settings, specs

    def optimize_for_nvidia(self):
        def change_nvidia_profile(nvidia_profile_path, gameloop_ui_path):
            tree = ET.parse(nvidia_profile_path, parser=ET.XMLParser(encoding='utf-16'))
            root = tree.getroot()

            profilename = root.find('.//ProfileName')
            executeables = root.find('.//Executeables')
            path_elem = executeables.find('string')

            path_elem.text = f"{gameloop_ui_path}/androidemulatoren.exe".lower()
            profilename.text = path_elem.text.replace('/', '\\')

            gpus = GPUtil.getGPUs()
            gpu = gpus[0] if gpus else None

            filter_setting = tree.find(".//ProfileSetting[SettingNameInfo='Enable FXAA']")
            if gpu and gpu.memoryTotal / 1024 < 3:
                filter_setting.find('SettingValue').text = '0'
            else:
                filter_setting.find('SettingValue').text = '1'

            tree.write(nvidia_profile_path, encoding='utf-16')

        try:
            nvidia_profile_path = self.resource_path("assets/fptools.nip")
            gameloop_ui_path = self.get_local_reg("InstallPath", path="UI")
            
            if not gameloop_ui_path:
                self.logger.warning("Gameloop UI path not found, skipping NVIDIA optimization")
                return

            def is_gpu_nvidia() -> bool:
                try:
                    gpu_provider = wmi.WMI().Win32_VideoController()[0].AdapterCompatibility
                    return "NVIDIA" in gpu_provider
                except:
                    return False

            if is_gpu_nvidia():
                change_nvidia_profile(nvidia_profile_path, gameloop_ui_path)

                # nvidiaProfileInspector requires elevation
                inspector_path = self.resource_path("assets/nvidiaProfileInspector.exe")
                params = f'"{nvidia_profile_path}" -silent'
                self._run_elevated(inspector_path, params)
        except Exception as e:
            self.logger.error(f"Exception occurred: {str(e)}", exc_info=True)

    @staticmethod
    def kill_gameloop():
        """
        Kills a list of processes related to the gameloop.

        Returns:
            - True if at least one process was killed.
            - False if no process was killed.
        """
        # List of processes to be killed
        processes_to_kill = [
            'aow_exe.exe',  # Process 1
            'AndroidEmulatorEn.exe',  # Process 2
            'AndroidEmulator.exe',  # Process 3
            'AndroidEmulatorEx.exe',  # Process 4
            'TBSWebRenderer.exe',  # Process 5
            'syzs_dl_svr.exe',  # Process 6
            'AppMarket.exe',  # Process 7
            'QMEmulatorService.exe',  # Process 8
            'RuntimeBroker.exe',  # Process 9
            'GameLoader.exe',  # Process 10
            'TSettingCenter.exe',  # Process 11
            'Auxillary.exe',  # Process 12
            'TP3Helper.exe',  # Process 13
            'tp3helper.dat',  # Process 14
            'GameDownload.exe'  # Process 15
        ]

        processes_killed = 0

        for process in processes_to_kill:
            try:
                result = subprocess.run(['taskkill', '/F', '/IM', process, '/T'], 
                                      stdout=subprocess.DEVNULL,
                                      stderr=subprocess.DEVNULL,
                                      timeout=5)
                if result.returncode == 0:
                    processes_killed += 1
            except subprocess.TimeoutExpired:
                pass
            except Exception:
                pass

        return processes_killed >= 1

    def uninstall_gameloop(self):
        """
        Forcefully uninstalls Gameloop by terminating its processes, running the
        official uninstaller, and thoroughly cleaning leftover registry keys and
        directories.
        """
        import glob
        errors = []

        self.kill_gameloop()
        self.kill_adb()
        sleep(1)

        try:
            uninstaller_paths = []
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                    r'SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\MobileGamePC') as key:
                    uninst_path = winreg.QueryValueEx(key, 'UninstallString')[0]
                    if uninst_path and os.path.exists(uninst_path.strip('"')):
                        uninstaller_paths.append(uninst_path.strip('"'))
            except OSError:
                pass

            install_path = self.get_local_reg("InstallPath")
            ui_path = self.get_local_reg("InstallPath", path="UI")
            for path in [install_path, ui_path]:
                if path:
                    parent = os.path.dirname(path)
                    for name in ['Uninstall.exe', 'uninstall.exe', 'uninst.exe']:
                        uninst = os.path.join(parent, name)
                        if os.path.exists(uninst):
                            uninstaller_paths.append(uninst)

            for uninst in uninstaller_paths:
                try:
                    self._run_elevated(uninst, '/S')
                    sleep(5)
                except Exception:
                    pass
        except Exception as e:
            errors.append(f"Uninstaller error: {e}")

        # Kill remaining processes after uninstaller completes
        self.kill_gameloop()
        sleep(1)

        # Clean leftover files and directories
        dirs_to_delete = set()
        for path in [self.get_local_reg("InstallPath"),
                     self.get_local_reg("InstallPath", path="UI")]:
            if path:
                dirs_to_delete.add(os.path.dirname(path))
                dirs_to_delete.add(path)

        common_paths = [
            r"C:\Program Files\TxGameAssistant",
            r"C:\Program Files (x86)\TxGameAssistant",
            os.path.expandvars(r"%LOCALAPPDATA%\GameLoop"),
            os.path.expandvars(r"%APPDATA%\AndroidTbox"),
            os.path.expandvars(r"%APPDATA%\TxGameAssistant"),
            os.path.expandvars(r"%LOCALAPPDATA%\Tencent"),
            os.path.expandvars(r"%TEMP%\Tencent"),
            os.path.expandvars(r"%TEMP%\TxGameAssistant"),
        ]

        for drive in ['C', 'D', 'E', 'F', 'G']:
            path_1 = f"{drive}:\\Program Files\\TxGameAssistant"
            path_2 = f"{drive}:\\Program Files (x86)\\TxGameAssistant"
            if os.path.exists(path_1):
                dirs_to_delete.add(path_1)
            if os.path.exists(path_2):
                dirs_to_delete.add(path_2)

        for path in common_paths:
            if os.path.exists(path):
                dirs_to_delete.add(path)

        for dir_path in dirs_to_delete:
            if dir_path and os.path.exists(dir_path):
                try:
                    shutil.rmtree(dir_path, ignore_errors=True)
                except Exception:
                    self._run_elevated("cmd.exe", f'/c "rd /s /q "{dir_path}""')

        # Clean leftover registry keys
        registry_keys_to_delete = [
            (winreg.HKEY_CURRENT_USER, r'SOFTWARE\Tencent\MobileGamePC'),
            (winreg.HKEY_CURRENT_USER, r'SOFTWARE\Tencent'),
            (winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\WOW6432Node\Tencent\MobileGamePC'),
            (winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\MobileGamePC'),
        ]

        for hive, key_path in registry_keys_to_delete:
            try:
                if hive == winreg.HKEY_LOCAL_MACHINE:
                    self._run_elevated("reg.exe", f'DELETE "{self._reg_hive_name(hive)}\\{key_path}" /f')
                else:
                    self._delete_reg_key_recursive(hive, key_path)
            except Exception:
                pass

        # Stop and remove background services & scheduled tasks
        services_to_remove = ['QMEmulatorService', 'TxGameAssistant']
        for svc in services_to_remove:
            try:
                self._run_elevated("sc.exe", f'stop {svc}')
                sleep(1)
                self._run_elevated("sc.exe", f'delete {svc}')
            except Exception:
                pass

        try:
            self._run_elevated("schtasks.exe", '/delete /tn "TencentGameAssistant" /f')
            self._run_elevated("schtasks.exe", '/delete /tn "GameLoop" /f')
        except Exception:
            pass

        remaining = [d for d in dirs_to_delete if d and os.path.exists(d)]
        if remaining:
            return False, f"Partially removed. Could not delete: {', '.join(remaining)}"
        return True, "GameLoop has been completely removed from the system."

    @staticmethod
    def _reg_hive_name(hive):
        """Convert a winreg hive constant to its string name for reg.exe."""
        return {
            winreg.HKEY_LOCAL_MACHINE: "HKLM",
            winreg.HKEY_CURRENT_USER: "HKCU",
        }.get(hive, "HKCU")

    @staticmethod
    def _delete_reg_key_recursive(hive, key_path):
        """Recursively delete a registry key and all its subkeys."""
        try:
            with winreg.OpenKey(hive, key_path, 0,
                                winreg.KEY_ALL_ACCESS | winreg.KEY_WOW64_64KEY) as key:
                while True:
                    try:
                        subkey = winreg.EnumKey(key, 0)
                        full_subkey = f"{key_path}\\{subkey}"
                        Optimizer._delete_reg_key_recursive(hive, full_subkey)
                    except OSError:
                        break
            winreg.DeleteKey(hive, key_path)
        except OSError:
            pass

    def change_dns_servers(self, dns_servers):
        """
        Change the DNS servers for all network adapters using elevated netsh commands.
        """
        try:
            primary_dns = dns_servers[0]
            secondary_dns = dns_servers[1] if len(dns_servers) > 1 else None

            import pythoncom
            pythoncom.CoInitialize()
            try:
                wmi_api = wmi.WMI()
                # Get enabled network adapters
                adapters = wmi_api.Win32_NetworkAdapterConfiguration(IPEnabled=True)

                for adapter in adapters:
                    if not adapter.Description:
                        continue
                    interface_name = adapter.Description
                    # Setting DNS via netsh requires elevation
                    cmd = f'interface ip set dns name="{interface_name}" static {primary_dns}'
                    self._run_elevated("netsh.exe", cmd)

                    if secondary_dns:
                        cmd_alt = f'interface ip add dns name="{interface_name}" {secondary_dns} index=2'
                        self._run_elevated("netsh.exe", cmd_alt)

                # Flush DNS cache
                subprocess.run(['ipconfig', '/flushdns'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
                return True
            finally:
                pythoncom.CoUninitialize()
        except Exception as e:
            self.logger.error(f"Failed to change DNS: {str(e)}", exc_info=True)
            return False

    def ipad_layout_settings(self, reset=False):
        """
        Modify the layout of the XML file based on the edited values.

        Parameters:
            reset (bool): If True, the XML file will be reset to its original state by copying the backup file. If False, the layout will be modified based on the edited values.
        """
        appdata_folder = os.getenv('APPDATA')
        keymap_folder = os.path.join(appdata_folder, 'AndroidTbox')
        original_file = os.path.join(keymap_folder, 'TVM_100.xml')
        backup_file = os.path.join(keymap_folder, 'TVM_100.xml.mkbackup')

        def set_keymap_layout():
            """
            Modify the layout of the XML file based on the edited values.
            """

            def update_xml(ipad_keymap):
                with open(original_file, 'r', encoding='utf-8') as file:
                    xml_code = file.read()

                root = ET.fromstring(f'<root>{xml_code}</root>')
                for pubg_version in self.pubg_versions:
                    if root.find(f".//Item[@ApkName='{pubg_version}']") is not None:
                        for query, values in ipad_keymap.items():
                            for button_name, switches in values.items():
                                for switch_name, points in switches.items():
                                    item_elem = root.find(f".//Item[@ApkName='{pubg_version}'].//KeyMapMode[@Name='{query}']")
                                    if item_elem is not None:
                                        key_mapping_ex = item_elem.find(f'.//KeyMappingEx[@ItemName="{button_name}"]')
                                        key_mapping = item_elem.find(f'.//KeyMapping[@ItemName="{button_name}"]')
                                        if key_mapping_ex is not None:
                                            if key_mapping_ex.findall(f'.//SwitchOperation[@EnablePositionSwitch]'):
                                                old_x, old_x2 = None, None
                                                for (new_y1, new_y2), point_val in zip(points, key_mapping_ex.findall(
                                                        f'.//SwitchOperation[@Description="{switch_name}"]')):
                                                    texture, points = point_val.get(f'EnablePositionSwitch').split(":")
                                                    x1, y1, x2, y2 = points.split(",")
                                                    old_x = x1 if old_x is None else old_x
                                                    old_x2 = x2 if old_x2 is None else old_x2
                                                    point_val.set('EnablePositionSwitch',
                                                                  f'{texture}:{old_x},{new_y1},{old_x2},{new_y2}')
                                            else:
                                                for _ in key_mapping_ex.findall(
                                                        f'.//SwitchOperation[@EnableSwitch="{switch_name}"]'):
                                                    if len(key_mapping_ex.findall(".//Point") or key_mapping_ex.findall(
                                                            ".//DriveKey") or key_mapping_ex.findall(
                                                        ".//SwitchOperation")) < len(
                                                        points):
                                                        zz = key_mapping_ex.findall(".//Point")
                                                        for _ in range(len(points) - len(zz)):
                                                            zz.append(ET.Element("Point"))
                                                    else:
                                                        zz = key_mapping_ex.findall(".//Point")

                                                    for (x, y), point_val in zip(points, (
                                                            zz or key_mapping_ex.findall(
                                                        ".//DriveKey") or key_mapping_ex.findall(
                                                        f'.//SwitchOperation[@EnableSwitch="{switch_name}"]'))):
                                                        # if main_value is not None:
                                                        if button_name == "Click with Scroll Wheel" and switch_name == "Backpage":
                                                            key_mapping_ex.set('Click_X', str(float(x) + 0.1))
                                                            key_mapping_ex.set('Click_Y', str(y))

                                                        key_mapping_ex.set('Point_X', str(x))
                                                        key_mapping_ex.set('Point_Y', str(y))

                                                        if point_val.get('Point_X') is not None:
                                                            point_val.set('Point_X', str(x))
                                                            point_val.set('Point_Y', str(y))
                                        elif key_mapping is not None:
                                            try:
                                                x, y = points
                                            except ValueError:
                                                print(switch_name, points, "Wrong format")
                                                modified_xml_code = ET.tostring(root, encoding='utf-8').decode('utf-8')
                                                return modified_xml_code.replace("<root>", "").replace("</root>", "")
                                            if key_mapping.get('Point_X') is not None:
                                                key_mapping.set('Point_X', str(x))
                                                key_mapping.set('Point_Y', str(y))

                                            if isinstance(points, list):
                                                for (x, y), point_element in zip(points, key_mapping.findall(
                                                        f'.//SwitchOperation[@EnableSwitch="{switch_name}"]')):
                                                    point_element.set('Point_X', str(x))
                                                    point_element.set('Point_Y', str(y))
                                            else:
                                                for point_element in key_mapping.findall(
                                                        f'.//SwitchOperation[@EnableSwitch="{switch_name}"]'):
                                                    point_element.set('Point_X', str(x))
                                                    point_element.set('Point_Y', str(y))
                # print(ET.tostring(root, encoding='utf-8').decode('utf-8')[6:-7])
                with open(original_file, 'w', encoding='utf-8') as file:
                    file.write(ET.tostring(root, encoding='utf-8').decode('utf-8')[6:-7])

            ipad_keymap_values = {
                "Smart 720P": {
                    "B": {"Reload": [("0.537234", "0.880567"), ("0.406535", "0.880567")]},  # Main
                    "3": {"Jump": ("0.613222", "0.880567"), "GetOutCar": ("0.613222", "0.880567")},  # Main
                    "F3": {"SetUp": [("0.768997", "0.163968"), ("0.896657", "0.270243")]},
                    "F2": {"SetUp": [("0.781155", "0.144737"), ("0.960486", "0.270243")]},  # Main 2 >> 1
                    "Space": {"Jump": ("0.962006", "0.762146"), "Climb": ("0.962006", "0.762146"),
                              "Whistle": [("0.911094", "0.660931"), ("0.063070", "0.747976")],
                              "DriveMode1|DriveSpeed": ("0.063070", "0.747976"),
                              "DriveMode1|DriveSpeedPress": ("0.063070", "0.747976"),
                              "SwimUp": ("0.835106", "0.701417"), "SwimmingUp": ("0.835106", "0.701417"), },
                    "Shift": {"DriveMode1|DriveSpeed": ("0.076748", "0.555668"),
                              "DriveMode1|DriveSpeedPress": ("0.076748", "0.555668")},
                    "Right Click": {"Sniper": ("0.962006", "0.638664"), "Sniper2": ("0.962006", "0.638664"),
                                    "Reload": ("0.962006", "0.638664")},  # Main
                    "Z": {"Fall": ("0.942249", "0.949393"), "CancelFall": ("0.942249", "0.949393")},  # Main
                    "E": {"Sideways": ("0.221884", "0.522267"), "SidewaysCancel": ("0.221884", "0.522267"),
                          "Moto": ("0.806991", "0.637652"), "Moto2": ("0.806991", "0.637652")},  # Main
                    "Q": {"Sideways": ("0.141337", "0.520243"), "SidewaysCancel": ("0.141337", "0.520243"),
                          "Moto": ("0.713526", "0.635628"), "Moto2": ("0.713526", "0.635628")},
                    "Y": {"SetUp": [("0.794833", "0.161943"), ("0.753040", "0.161943"), ("0.844985", "0.157895")]},
                    "T": {"SetUp": [("0.780395", "0.092105"), ("0.732523", "0.092105"), ("0.847264", "0.097166")]},
                    "Alt": {"Eye": [("0.776596", "0.232794")]},
                    "Drive": {"DriveMode1": (("0.673252", "0.765182"), ("0.834347", "0.765182"),
                                             ("0.164894", "0.644737"), ("0.164894", "0.826923"))},  # ADWS
                    "F": {"Pickup|NineBlock": ("0.144377", "0.683198"), "Pickup|SixBlock": ("0.341945", "0.682186"),
                          "Pickup|XBtn": ("0.319909", "0.281377"), "Pickup": ("0.658055", "0.281377"),
                          "Pickup|SkyBoxFlag|XBtn": ("0.144377", "0.683198")},
                    "G": {"Pickup|NineBlock": ("0.303191", "0.683198"), "Pickup|SixBlock": ("0.484043", "0.682186"),
                          "Pickup|XBtn": ("0.319909", "0.354251"), "Pickup": ("0.658055", "0.354251"),
                          "Pickup|XBtn|SkyBoxFlag": ("0.303191", "0.683198"),
                          "Whistle": ("0.954407", "0.771255"),
                          "OutCarShoot": ("0.954407", "0.683198"), "OutCarShoot2": ("0.954407", "0.771255")},
                    "H": {"Pickup|NineBlock": ("0.144377", "0.769231"), "Pickup|SixBlock": ("0.649696", "0.682186"),
                          "Pickup|XBtn": ("0.319909", "0.429150"), "Pickup": ("0.658055", "0.429150"),
                          "Pickup|XBtn|SkyBoxFlag": ("0.144377", "0.769231")},
                    "Slide with Scroll Wheel": {"Pickup": [("0.658055", "0.374251")],
                                                "Pickup|XBtn": [("0.319909", "0.374251")],
                                                "Pickup|XBtn|SkyBoxFlag": [("0.319909", "0.723198")],
                                                "Pickup|SkyBoxFlag": [("0.658055", "0.723198")]},
                    "4": {"GrenadeArrowUp": [("0.863750", "0.926667"), ("0.202847", "0.863750")]},
                    "5": {"GrenadeArrowUp": [("0.863750", "0.926667"), ("0.202847", "0.863750")]},
                    "6": {"GrenadeArrowUp": [("0.863750", "0.926667"), ("0.202847", "0.863750")]},
                    "X": {"GrenadeArrowUp": [("0.863750", "0.926667"), ("0.202847", "0.863750")]},
                    "7": {"GrenadeArrowUp": [("0.863750", "0.926667"), ("0.202847", "0.863750")]},
                    "8": {"GrenadeArrowUp": [("0.863750", "0.926667"), ("0.202847", "0.863750")]},
                    "9": {"GrenadeArrowUp": [("0.863750", "0.926667"), ("0.202847", "0.863750")]},
                    "0": {"GrenadeArrowUp": [("0.863750", "0.926667"), ("0.202847", "0.863750")]},
                },
                "Smart 1080P": {
                    "B": {"Reload": [("0.542969", "0.910751"), ("0.437500", "0.910751")]},  # Main
                    "3": {"Jump": ("0.584347", "0.913793"), "GetOutCar": ("0.584347", "0.913793")},  # Main
                    "F3": {"SetUp": [("0.838146", "0.100406"), ("0.924012", "0.193712")]},
                    "F2": {"SetUp": [("0.838146", "0.100406"), ("0.971884", "0.193712")]},  # Main 2 >> 1
                    "Space": {"Jump": ("0.969605", "0.834686"), "Climb": ("0.969605", "0.834686"),
                              "Whistle": [("0.934650", "0.764706"), ("0.049392", "0.823529")],
                              "DriveMode1|DriveSpeed": ("0.049392", "0.823529"),
                              "DriveMode1|DriveSpeedPress": ("0.049392", "0.823529"),
                              "SwimUp": ("0.879518", "0.759036"), "SwimmingUp": ("0.879518", "0.759036"), },
                    "Shift": {"DriveMode1|DriveSpeed": ("0.053951", "0.683570"),
                              "DriveMode1|DriveSpeedPress": ("0.053951", "0.683570")},
                    "Right Click": {"Sniper": ("0.971125", "0.746450"), "Sniper2": ("0.971125", "0.746450"),
                                    "Reload": ("0.971125", "0.746450")},  # Main
                    "Z": {"Fall": ("0.961246", "0.967546"), "CancelFall": ("0.961246", "0.967546")},  # Main
                    "E": {"Sideways": ("0.155775", "0.658215"), "SidewaysCancel": ("0.155775", "0.658215"),
                          "Moto": ("0.857903", "0.738337"), "Moto2": ("0.857903", "0.738337")},  # Main
                    "Q": {"Sideways": ("0.101064", "0.656187"), "SidewaysCancel": ("0.101064", "0.656187"),
                          "Moto": ("0.791793", "0.736308"), "Moto2": ("0.791793", "0.736308")},
                    "Y": {"SetUp": [("0.852584", "0.118661"), ("0.823708", "0.118661"), ("0.892097", "0.108519")]},
                    "T": {"SetUp": [("0.841185", "0.064909"), ("0.809271", "0.064909"), ("0.888298", "0.073022")]},
                    "Alt": {"Eye": [("0.840426", "0.166329")]},
                    "Drive": {"DriveMode1": (("0.764438", "0.836714"), ("0.881459", "0.836714"),
                                             ("0.116261", "0.752535"), ("0.116261", "0.883367"))},  # ADWS
                    "F": {"Pickup|NineBlock": ("0.353906", "0.763889"), "Pickup|SixBlock": ("0.482031", "0.767206"),
                          "Pickup|XBtn": ("0.467187", "0.199393"), "Pickup": ("0.721094", "0.199393"),
                          "Pickup|SkyBoxFlag|XBtn": ("0.353906", "0.763889")},
                    "G": {"Pickup|NineBlock": ("0.732812", "0.767206"), "Pickup|SixBlock": ("0.607812", "0.767206"),
                          "Pickup|XBtn": ("0.467187", "0.251616"), "Pickup": ("0.721094", "0.251616"),
                          "Pickup|XBtn|SkyBoxFlag": ("0.476563", "0.763889"),
                          "Whistle": ("0.966565", "0.835700"),
                          "OutCarShoot": ("0.965625", "0.839167"), "OutCarShoot2": ("0.965625", "0.839167")},
                    "H": {"Pickup|NineBlock": ("0.353906", "0.847761"), "Pickup|SixBlock": ("0.732031", "0.767206"),
                          "Pickup|XBtn": ("0.467187", "0.303839"), "Pickup": ("0.721094", "0.303839"),
                          "Pickup|XBtn|SkyBoxFlag": ("0.353906", "0.847761")},
                    "1": {"Jump": ("0.453906", "0.947333"), "Climb": ("0.453906", "0.947333"),
                          "GetOutCar": ("0.453906", "0.947333")},
                    "2": {"Jump": ("0.544531", "0.947333"), "Climb": ("0.544531", "0.947333"),
                          "GetOutCar": ("0.544531", "0.947333")},
                    "Click with Scroll Wheel": {"Backpage": [("0.453906", "0.947333")]},
                    "Slide with Scroll Wheel": {"Pickup": [("0.739844", "0.199393")],
                                                "Pickup|XBtn": [("0.467187", "0.199393")]},
                    "4": {"GrenadeArrowUp": [("0.894750", "0.936667"), ("0.202847", "0.894750")]},
                    "5": {"GrenadeArrowUp": [("0.894750", "0.936667"), ("0.202847", "0.894750")]},
                    "6": {"GrenadeArrowUp": [("0.894750", "0.936667"), ("0.202847", "0.894750")]},
                    "X": {"GrenadeArrowUp": [("0.894750", "0.936667"), ("0.202847", "0.894750")]},
                    "7": {"GrenadeArrowUp": [("0.894750", "0.936667"), ("0.202847", "0.894750")]},
                    "8": {"GrenadeArrowUp": [("0.894750", "0.936667"), ("0.202847", "0.894750")]},
                    "9": {"GrenadeArrowUp": [("0.894750", "0.936667"), ("0.202847", "0.894750")]},
                    "0": {"GrenadeArrowUp": [("0.894750", "0.936667"), ("0.202847", "0.894750")]},
                },
                "Smart 2K": {
                    "B": {"Reload": [("0.542969", "0.910751"), ("0.437500", "0.910751")]},  # Main
                    "3": {"Jump": ("0.584347", "0.913793"), "GetOutCar": ("0.584347", "0.913793")},  # Main
                    "F3": {"SetUp": [("0.838146", "0.100406"), ("0.924012", "0.193712")]},
                    "F2": {"SetUp": [("0.838146", "0.100406"), ("0.971884", "0.193712")]},  # Main 2 >> 1
                    "Space": {"Jump": ("0.969605", "0.834686"), "Climb": ("0.969605", "0.834686"),
                              "Whistle": [("0.934650", "0.764706"), ("0.049392", "0.823529")],
                              "DriveMode1|DriveSpeed": ("0.049392", "0.823529"),
                              "DriveMode1|DriveSpeedPress": ("0.049392", "0.823529"),
                              "SwimUp": ("0.879518", "0.759036"), "SwimmingUp": ("0.879518", "0.759036"), },
                    "Shift": {"DriveMode1|DriveSpeed": ("0.053951", "0.683570"),
                              "DriveMode1|DriveSpeedPress": ("0.053951", "0.683570")},
                    "Right Click": {"Sniper": ("0.971125", "0.746450"), "Sniper2": ("0.971125", "0.746450"),
                                    "Reload": ("0.971125", "0.746450")},  # Main
                    "Z": {"Fall": ("0.961246", "0.967546"), "CancelFall": ("0.961246", "0.967546")},  # Main
                    "E": {"Sideways": ("0.155775", "0.658215"), "SidewaysCancel": ("0.155775", "0.658215"),
                          "Moto": ("0.857903", "0.738337"), "Moto2": ("0.857903", "0.738337")},  # Main
                    "Q": {"Sideways": ("0.101064", "0.656187"), "SidewaysCancel": ("0.101064", "0.656187"),
                          "Moto": ("0.791793", "0.736308"), "Moto2": ("0.791793", "0.736308")},
                    "Y": {"SetUp": [("0.852584", "0.118661"), ("0.823708", "0.118661"), ("0.892097", "0.108519")]},
                    "T": {"SetUp": [("0.841185", "0.064909"), ("0.809271", "0.064909"), ("0.888298", "0.073022")]},
                    "Alt": {"Eye": [("0.840426", "0.166329")]},
                    "Drive": {"DriveMode1": (("0.764438", "0.836714"), ("0.881459", "0.836714"),
                                             ("0.116261", "0.752535"), ("0.116261", "0.883367"))},  # ADWS
                    "F": {"Pickup|NineBlock": ("0.353906", "0.763889"), "Pickup|SixBlock": ("0.482031", "0.767206"),
                          "Pickup|XBtn": ("0.467187", "0.199393"), "Pickup": ("0.721094", "0.199393"),
                          "Pickup|SkyBoxFlag|XBtn": ("0.353906", "0.763889")},
                    "G": {"Pickup|NineBlock": ("0.732812", "0.767206"), "Pickup|SixBlock": ("0.607812", "0.767206"),
                          "Pickup|XBtn": ("0.467187", "0.251616"), "Pickup": ("0.721094", "0.251616"),
                          "Pickup|XBtn|SkyBoxFlag": ("0.476563", "0.763889"),
                          "Whistle": ("0.966565", "0.835700"),
                          "OutCarShoot": ("0.965625", "0.839167"), "OutCarShoot2": ("0.965625", "0.839167")},
                    "H": {"Pickup|NineBlock": ("0.353906", "0.847761"), "Pickup|SixBlock": ("0.732031", "0.767206"),
                          "Pickup|XBtn": ("0.467187", "0.303839"), "Pickup": ("0.721094", "0.303839"),
                          "Pickup|XBtn|SkyBoxFlag": ("0.353906", "0.847761")},
                    "1": {"Jump": ("0.453906", "0.947333"), "Climb": ("0.453906", "0.947333"),
                          "GetOutCar": ("0.453906", "0.947333")},
                    "2": {"Jump": ("0.544531", "0.947333"), "Climb": ("0.544531", "0.947333"),
                          "GetOutCar": ("0.544531", "0.947333")},
                    "Click with Scroll Wheel": {"Backpage": [("0.453906", "0.947333")]},
                    "Slide with Scroll Wheel": {"Pickup": [("0.739844", "0.199393")],
                                                "Pickup|XBtn": [("0.467187", "0.199393")]},
                    "4": {"GrenadeArrowUp": [("0.894750", "0.936667"), ("0.202847", "0.894750")]},
                    "5": {"GrenadeArrowUp": [("0.894750", "0.936667"), ("0.202847", "0.894750")]},
                    "6": {"GrenadeArrowUp": [("0.894750", "0.936667"), ("0.202847", "0.894750")]},
                    "X": {"GrenadeArrowUp": [("0.894750", "0.936667"), ("0.202847", "0.894750")]},
                    "7": {"GrenadeArrowUp": [("0.894750", "0.936667"), ("0.202847", "0.894750")]},
                    "8": {"GrenadeArrowUp": [("0.894750", "0.936667"), ("0.202847", "0.894750")]},
                    "9": {"GrenadeArrowUp": [("0.894750", "0.936667"), ("0.202847", "0.894750")]},
                    "0": {"GrenadeArrowUp": [("0.894750", "0.936667"), ("0.202847", "0.894750")]},
                }
            }


            update_xml(ipad_keymap_values)


        if reset:
            shutil.copy2(backup_file, original_file)
            os.remove(backup_file)
        else:
            if not os.path.exists(backup_file):
                shutil.copy2(original_file, backup_file)
            set_keymap_layout()


    def ipad_settings(self, width: int, height: int) -> None:
        """
        Update iPad settings with the given width and height.
        """
        _width = self.settings.value("VMResWidth")
        _height = self.settings.value("VMResHeight")

        if _width is None or _height is None:
            vm_res_width = self.get_reg("VMResWidth")
            vm_res_height = self.get_reg("VMResHeight")
            # Provide defaults if registry is also None
            if vm_res_width is None:
                vm_res_width = 1280
            if vm_res_height is None:
                vm_res_height = 720
            self.settings.setValue("VMResWidth", vm_res_width)
            self.settings.setValue("VMResHeight", vm_res_height)

        self.ipad_layout_settings()
        self.set_dword("VMResWidth", width)
        self.set_dword("VMResHeight", height)

    def reset_ipad(self):
        """
        Resets the resolution of the iPad to its default values.
        """
        width = self.settings.value("VMResWidth")
        height = self.settings.value("VMResHeight")

        if width and height:
            self.settings.setValue("VMResWidth", None)
            self.settings.setValue("VMResHeight", None)
            self.ipad_layout_settings(reset=True)
            self.set_dword("VMResWidth", width)
            self.set_dword("VMResHeight", height)
            return width, height
        else:
            return None, None


class Game(Optimizer):

    def __init__(self):
        super().__init__()
        self.is_adb_working = None

    def gen_game_icon(self, game_name):
        gameloop_market_path = self.get_local_reg("InstallPath") or r"C:\Program Files\TxGameAssistant\AppMarket"
        pythoncom.CoInitialize()
        desktop = winshell.desktop()

        version_id = next((key for key, value in self.pubg_versions.items() if value == game_name), None)
        path_icon = os.path.join(desktop, f"{game_name}.lnk")
        target = rf"{gameloop_market_path}\AppMarket.exe"

        # Use AppData folder for icons to avoid permission issues in Program Files
        appdata_icons_path = os.path.join(os.getenv('APPDATA'), 'FPTools', 'icons')
        os.makedirs(appdata_icons_path, exist_ok=True)
        icon_dest = os.path.join(appdata_icons_path, f"{version_id}.ico")
        
        icon_src = self.resource_path(fr"assets\icons\{version_id}.ico")
        if os.path.exists(icon_src):
            copy(icon_src, icon_dest)

        shortcut = Dispatch('WScript.Shell').CreateShortCut(path_icon)
        shortcut.Targetpath = target
        shortcut.Arguments = f"-startpkg {version_id}  -from DesktopLink"
        shortcut.Description = "Mo-Tech"
        shortcut.IconLocation = icon_dest
        shortcut.save()

    def check_adb_status(self):
        try:
            adb_status = self.get_reg("AdbDisable")

            if adb_status == 0:
                self.adb_enabled = True
                return
            elif adb_status == 1 or adb_status is None:
                # If registry key is missing or disabled, enable it
                self.set_dword("AdbDisable", 0)
                self.adb_enabled = False  # Still False because it needs a Gameloop restart
                return
        except Exception as e:
            self.logger.error(f"Error checking ADB status: {e}")
            self.adb_enabled = False

    @staticmethod
    def is_gameloop_running():
        emulator_processes = {"AndroidEmulatorEx.exe", "AndroidEmulatorEn.exe", "AndroidEmulator.exe"}
        try:
            for proc in psutil.process_iter(['name']):
                proc_name = proc.info.get('name')
                if proc_name and proc_name in emulator_processes:
                    return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess, Exception):
            pass
        return False

    def wait_for_device_boot(self, max_retries=30):
        for i in range(max_retries):
            try:
                # Check multiple boot indicators for different Android versions
                boot_complete = self.adb.shell("getprop dev.bootcomplete").strip()
                sys_boot = self.adb.shell("getprop sys.boot_completed").strip()
                
                if boot_complete == "1" or sys_boot == "1":
                    return True
                
                # Fallback: If we can execute a basic command, the device is "up enough" for our needs
                # We do this after a few retries to ensure the system is somewhat stable
                if i > 5:
                    res = self.adb.shell("id")
                    if res and "uid=" in res:
                        return True
            except Exception:
                pass
            sleep(1.0)
        return False

    def check_adb_connection(self, first_check=True):
        try:
            client = adbutils.AdbClient()

            # 1. Try to find existing connected devices
            devices = client.list()
            best_device = None

            # List of suspected Gameloop ports to try connecting to if nothing is found
            common_ports = ["5555", "5557", "5559", "5554", "5556", "5558"]

            if not devices and first_check:
                # Try connecting to local ports commonly used by Gameloop
                for port in common_ports:
                    try:
                        # Use shell command to connect as adbutils connect is sometimes flaky
                        subprocess.run(["adb", "connect", f"127.0.0.1:{port}"],
                                     capture_output=True, timeout=2)
                    except:
                        pass
                # Small delay for connections to establish
                sleep(0.5)
                devices = client.list()

            if devices:
                # Filter for emulators or pick the first available one
                for d in devices:
                    if d.serial.startswith("emulator-") or d.serial.startswith("127.0.0.1:"):
                        best_device = d
                        break
                if not best_device:
                    best_device = devices[0]
            else:
                # Fallback to default if nothing found
                best_device = client.device(serial="emulator-5554")

            self.adb = best_device

            # Verify if it's responding
            self.logger.info(f"Checking connection to device: {self.adb.serial}")
            if not self.wait_for_device_boot(max_retries=30):
                raise Exception(f"Device {self.adb.serial} not responding/bootcomplete timeout")

            # Final verify by pulling a small file
            self.adb.sync.pull("/default.prop", self.resource_path(r'assets\testADB.fptools'))
            self.is_adb_working = True

        except Exception as e:
            self.logger.error(f"ADB Connection Error: {e}")
            self.kill_adb()
            self.is_adb_working = False

            if first_check:
                sleep(1)
                self.check_adb_connection(False)


    def pubg_version_found(self):
        """
        Checks if any version of PUBG is installed on the device.
        """
        self.wait_for_device_boot(max_retries=5)
        self.PUBG_Found = [version_name for package_name, version_name in self.pubg_versions.items()
                           if self.adb.shell(f"pm list packages {package_name}")]

    def start_gameloop(self):
        """Starts Gameloop's emulator directly with elevation if needed."""
        gameloop_path = self.get_local_reg("InstallPath")
        if gameloop_path:
            exe_path = os.path.join(gameloop_path, "AppMarket.exe")
            if os.path.exists(exe_path):
                try:
                    subprocess.Popen([exe_path])
                    return True
                except OSError:
                    # Requires elevation - use ShellExecuteW runas
                    return self._run_elevated(exe_path)
        return False

    def get_graphics_file(self, package: str):
        active_savegames_path = f"/sdcard/Android/data/{package}/files/UE4Game/ShadowTrackerExtra/ShadowTrackerExtra/Saved/SaveGames/Active.sav"
        local_file_path = self.resource_path('assets/old.fptools')
        self.pubg_package = package
        self.adb.sync.pull(active_savegames_path, local_file_path)

        with open(local_file_path, 'rb') as file:
            self.active_sav_content = file.read()

    def save_graphics_file(self):
        file_path = self.resource_path("assets/new.fptools")
        with open(file_path, 'wb') as file:
            file.write(self.active_sav_content)

    def set_fps(self, val: str) -> None:
        """
        Updates the Active.sav file with the new FPS value.
        """
        fps_mapping = {
            "Power Saving": b"\x02",
            "Medium": b"\x03",
            "High": b"\x04",
            "Ultra": b"\x05",
            "Extreme": b"\x06",
            "Extreme+": b"\x07",
            "Ultra Extreme": b"\x08"
        }
        fps_value = fps_mapping.get(val)

        fps_properties = ["FPSLevel", "BattleFPS", "LobbyFPS"]
        if fps_value is not None:
            for prop in fps_properties:
                header = prop.encode(
                    'utf-8') + b'\x00\x0c\x00\x00\x00IntProperty\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00'
                if header in self.active_sav_content:
                    before, _, after = self.active_sav_content.partition(header)
                    if after:
                        after = fps_value + after[1:]
                        self.active_sav_content = before + _ + after

        # Force bypass PUBG limitation to guarantee 120/90/60 FPS with any graphics profile
        cvar_mapping = {
            "Power Saving": "2", "Medium": "3", "High": "4", "Ultra": "5",
            "Extreme": "6", "Extreme+": "7", "Ultra Extreme": "8" # 8 is for 120 FPS
        }
        fps_cvar = cvar_mapping.get(val)
        if fps_cvar:
            user_fptools = self.resource_path(r"assets\user.fptools")
            import os
            # Create file if it doesn't exist so CVARs can always be written
            if not os.path.exists(user_fptools):
                with open(user_fptools, "w") as file:
                    file.write("[/Script/ShadowTrackerExtra.ShadowTrackerExtraUserSettings]\n")

            lines = []
            with open(user_fptools, "r") as file:
                for line in file:
                    if not line.startswith("+CVars=r.PUBGDeviceFPS"):
                        lines.append(line)
            
            # Append CVARs that force raw device limits for each graphics layer
            lines.append(f"+CVars=r.PUBGDeviceFPSSuperSmooth={fps_cvar}\n")
            lines.append(f"+CVars=r.PUBGDeviceFPSLow={fps_cvar}\n")
            lines.append(f"+CVars=r.PUBGDeviceFPSMid={fps_cvar}\n")
            lines.append(f"+CVars=r.PUBGDeviceFPSHigh={fps_cvar}\n")
            lines.append(f"+CVars=r.PUBGDeviceFPSHDR={fps_cvar}\n")
            lines.append(f"+CVars=r.PUBGDeviceFPSUltraHD={fps_cvar}\n")
            lines.append(f"+CVars=r.PUBGDeviceFPSUltraHDR={fps_cvar}\n")
            
            with open(user_fptools, "w") as file:
                file.writelines(lines)

        # Ensure GameLoop engine's screen FPS matches the desired target
        if val == "Ultra Extreme":
            self.set_dword("VMScreenFPS", 120)
        elif val == "Extreme+":
            self.set_dword("VMScreenFPS", 90)
        else:
            # For 60 FPS and below, 90Hz engine is generally better for smoothness but 60 is fine
            # We will keep it at minimum 60Hz
            current_fps = self.get_reg("VMScreenFPS")
            if current_fps and current_fps < 60:
                self.set_dword("VMScreenFPS", 60)

    def read_hex(self, name):
        """
        Reads the value of the specified property from the Active.sav file.
        """
        header = name.encode('utf-8') + b'\x00\x0c\x00\x00\x00IntProperty\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00'
        _, _, content = self.active_sav_content.partition(header)
        return content[:1]

    def change_graphics_file(self, name, val):
        """
        Updates the Active.sav file with the new graphics setting value.
        """
        header = name.encode('utf-8') + b'\x00\x0c\x00\x00\x00IntProperty\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00'
        if header in self.active_sav_content:
            a, b, c = self.active_sav_content.partition(header)
            if c:
                c = val + c[1:]
                self.active_sav_content = a + b + c

    def get_graphics_setting(self):
        """
        Gets the graphics setting name from the hex value.
        """
        graphics_setting_hex = self.read_hex("BattleRenderQuality")
        graphics_setting_dict = {
            b'\x00': "Super Smooth (BETA)",
            b'\x01': "Smooth",
            b'\x02': "Balanced",
            b'\x03': "HD",
            b'\x04': "HDR",
            b'\x05': "Ultra HDR",
            b'\x06': "Extreme HDR"
        }
        return graphics_setting_dict.get(graphics_setting_hex, None)

    def get_fps(self):
        """
        Gets the FPS value from the Active.sav file.
        """
        fps_hex = self.read_hex("BattleFPS")
        fps_dict = {
            b"\x02": "Power Saving",
            b"\x03": "Medium",
            b"\x04": "High",
            b"\x05": "Ultra",
            b"\x06": "Extreme",
            b"\x07": "Extreme+",
            b"\x08": "Ultra Extreme",
        }
        return fps_dict.get(fps_hex, None)

    def get_shadow(self):
        """
        Gets the shadow value from the UserCustom.ini file.
        """
        shadow_name = None
        user_custom_ini_path = f"/sdcard/Android/data/{self.pubg_package}/files/UE4Game/ShadowTrackerExtra/ShadowTrackerExtra/Saved/Config/Android/UserCustom.ini"
        
        try:
            self.adb.sync.pull(user_custom_ini_path, self.resource_path(r'assets\user.fptools'))
        except Exception as e:
            self.logger.error(f"Failed to pull UserCustom.ini: {e}")
            return "Enable" # Default if file not found

        with open(self.resource_path(r"assets\user.fptools")) as file:
            for line in file:
                line = line.strip()
                if line.startswith("+CVars=0B572A11181D160E280C1815100D0044"):
                    if int(line[-2:]) == 49:
                        shadow_name = "Disable"
                    elif int(line[-2:]) == 48:
                        shadow_name = "Enable"
                    break

        return shadow_name

    # Todo: Make This Function Working
    def set_shadow(self, value):
        """
        Sets the shadow value in the Active.sav file.
        :param value: Shadow value to set ("ON" or "OFF")
        :return: True if successful, False otherwise
        """

        shadow_value = {"ON": 48, "OFF": 49}.get(value)
        if shadow_value is None:
            return False
        shadow_values = {"r.UserShadowSwitch": "1", "r.ShadowQuality": "1", "r.Mobile.DynamicObjectShadow": "1",
                         "r.Shadow.MaxCSMResolution": "1", "r.Shadow.DistanceScale": "1",
                         "r.Shadow.CSM.MaxMobileCascades": "1"}
        lines = []
        with open(self.resource_path(r"assets\user.fptools"), "r") as file:
            for line in file:
                if line.strip().startswith("+CVars=0B572A11181D160E280C1815100D0044"):
                    line = f"+CVars=0B572A11181D160E280C1815100D0044{shadow_value}\n"
                elif line.strip().startswith("+CVars=0B572C0A1C0B2A11181D160E2A0E100D1A1144"):
                    line = f"+CVars=0B572C0A1C0B2A11181D160E2A0E100D1A1144{shadow_value}\n"
                lines.append(line)

        with open(self.resource_path(r"assets\user.fptools"), "w") as file:
            file.writelines(lines)

        return True

    def get_graphics_style(self):
        """
        Gets the graphics style name from the hex value.
        :return: name of the graphics style
        """
        battle_style_hex = self.read_hex("BattleRenderStyle")
        battle_style_dict = {
            b'\x01': "Classic",
            b'\x02': "Colorful",
            b'\x03': "Realistic",
            b'\x04': "Soft",
            b'\x06': "Movie"
        }

        return battle_style_dict.get(battle_style_hex, "Not Found, It Will Be Added In The Next Update")

    def set_graphics_style(self, style):
        """
        Sets the graphics style.
        """
        battle_style_dict = {
            "Classic": b'\x01',
            "Colorful": b'\x02',
            "Realistic": b'\x03',
            "Soft": b'\x04',
            "Movie": b'\x06'
        }
        battle_style = battle_style_dict.get(style, "Not Found, It Will Be Added In The Next Update")
        self.change_graphics_file("BattleRenderStyle", battle_style)

    def set_graphics_quality(self, quality):
        """
        Sets the graphics quality for different game modes.
        """
        graphics_setting_dict = {
            "Super Smooth (BETA)": b'\x00',
            "Smooth": b'\x01',
            "Balanced": b'\x02',
            "HD": b'\x03',
            "HDR": b'\x04',
            "Ultra HDR": b'\x05',
            "Extreme HDR": b'\x06'
        }

        graphics_setting = graphics_setting_dict.get(quality, b'\x01')

        # Set the graphics quality
        graphics_files = ["ArtQuality", "LobbyRenderQuality", "BattleRenderQuality"]
        for value in graphics_files:
            self.change_graphics_file(value, graphics_setting)

    def push_active_shadow_file(self):
        """
        Pushes the modified Active.sav & Shadow file to the device and restarts the game.
        """
        self.adb.shell(f"am force-stop {self.pubg_package}")
        sleep(0.2)

        data_dir = f"/sdcard/Android/data/{self.pubg_package}/files/UE4Game/ShadowTrackerExtra/ShadowTrackerExtra/Saved"

        files = [
            (self.resource_path(r"assets\new.fptools"), f"{data_dir}/SaveGames/Active.sav"),
            (self.resource_path(r"assets\user.fptools"), f"{data_dir}/Config/Android/UserCustom.ini")
        ]

        for src, dest in files:
            self.adb.sync.push(src, dest)
            sleep(0.2)

    def start_app(self):
        package = f"{self.pubg_package}/com.epicgames.ue4.SplashActivity"
        self.adb.shell(f"am start -n {package}")

    def kr_fullhd(self):
        def backup_folder(path):
            backup_path = path + '.FPbackup'

            output = self.adb.shell(f"[ -d {path} ] && echo 1 || echo 0").strip()
            backup_output = self.adb.shell(f"[ -d {backup_path} ] && echo 1 || echo 0").strip()
            if backup_output == '0' and output == '1':
                self.adb.shell(['mv', path, backup_path])
            elif backup_output == '1' and output == '1':
                self.adb.shell(['rm', '-r', path])

        def restore_folder(path):
            backup_path = path + '.FPbackup'
            backup_output = self.adb.shell(f"[ -d {backup_path} ] && echo 1 || echo 0").strip()
            if backup_output == '1':
                self.adb.shell(['mv', backup_path, path])

        data_path = f"/sdcard/Android/data/{self.pubg_package}"
        obb_path = f"/sdcard/Android/obb/{self.pubg_package}"
        user_custom_ini_path = f"{data_path}/files/UE4Game/ShadowTrackerExtra/ShadowTrackerExtra/Saved/Config/Android/UserCustom.ini"

        safe_path = "/sdcard/fp_safe_folder"
        data_path_for_account = f"/data/data/{self.pubg_package}"

        self.adb.push(self.resource_path(r'assets\fptools_kr.ini'), user_custom_ini_path)

        self.adb.shell(f"mkdir -p {safe_path}")
        self.adb.shell(f"cp -r {data_path_for_account}/shared_prefs {safe_path}/shared_prefs")
        self.adb.shell(f"cp -r {data_path_for_account}/databases {safe_path}/databases")

        backup_folder(data_path)
        backup_folder(obb_path)

        self.adb.shell(['pm', 'clear', self.pubg_package])
        self.adb.shell(['pm', 'grant', self.pubg_package, 'android.permission.READ_EXTERNAL_STORAGE'])
        self.adb.shell(['pm', 'grant', self.pubg_package, 'android.permission.WRITE_EXTERNAL_STORAGE'])

        restore_folder(data_path)
        restore_folder(obb_path)

        self.adb.shell(f"cp -r {safe_path}/shared_prefs {data_path_for_account}/shared_prefs")
        self.adb.shell(f"cp -r {safe_path}/databases {data_path_for_account}/databases")

        self.start_app()

        self.adb.shell(f"rm -r {safe_path}")
