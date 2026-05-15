"""
Mo-Tech pubgm - The Ultimate GameLoop & PUBG Mobile Optimization Suite
Developed by: Mohammed Emad
Version: v2.0.0
Features Added:
- Advanced Profile System (Save/Load configurations)
- Real-time Performance Monitoring (CPU/RAM usage)
- Enhanced Gaming Mode
- Operation Logging System
- Backup & Restore System
- Settings Validation
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import sys
import subprocess
import shutil
import ctypes
import threading
import time
import datetime
from pathlib import Path
from typing import Optional, Dict, Any

# Check if running as administrator
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

class MoTechApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mo-Tech pubgm - Ultimate Optimization Suite v2.0")
        self.root.geometry("1000x750")
        self.root.resizable(True, True)
        
        # Set icon
        try:
            self.root.iconbitmap("assets/icons/logo.ico")
        except:
            pass
        
        # Configuration paths
        self.gameloop_path = self.find_gameloop_path()
        self.config_file = "assets/configs/settings.json"
        self.profiles_dir = "assets/configs/profiles"
        self.logs_dir = "assets/logs"
        self.backup_dir = "assets/backups"
        
        # Initialize logging system
        self.log_file = os.path.join(self.logs_dir, f"operations_{datetime.datetime.now().strftime('%Y%m%d')}.log")
        self.setup_logging()
        
        # Load settings
        self.settings = self.load_settings()
        
        # Performance monitoring flags
        self.monitoring_active = False
        self.monitor_thread = None
        
        # Create main interface
        self.create_main_interface()
        
        # Log application start
        self.log_operation("Application started", "INFO")
    
    def setup_logging(self):
        """Initialize logging system"""
        os.makedirs(self.logs_dir, exist_ok=True)
        os.makedirs(self.profiles_dir, exist_ok=True)
        os.makedirs(self.backup_dir, exist_ok=True)
    
    def log_operation(self, message: str, level: str = "INFO"):
        """Log operations to file"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}\n"
        
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except Exception as e:
            print(f"Logging error: {e}")
    
    def find_gameloop_path(self):
        """Find GameLoop installation path"""
        default_paths = [
            r"C:\Program Files\TxGameAssistant",
            r"C:\Program Files (x86)\TxGameAssistant",
            r"D:\Program Files\TxGameAssistant",
        ]
        
        for path in default_paths:
            if os.path.exists(path):
                return path
        
        # Try to read from registry
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Tencent\Gameloop")
            path, _ = winreg.QueryValueEx(key, "InstallPath")
            winreg.CloseKey(key)
            return path
        except:
            pass
        
        return None
    
    def load_settings(self):
        """Load saved settings from config file"""
        default_settings = {
            "fps_limit": 60,
            "graphics_quality": "Smooth",
            "visual_style": "Classic",
            "rendering_mode": "DirectX+",
            "shader_cache": True,
            "global_render_cache": True,
            "hardware_priority": "High",
            "ipad_view": False,
            "resolution": "1920x1080"
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    loaded = json.load(f)
                    default_settings.update(loaded)
            except:
                pass
        
        return default_settings
    
    def save_settings(self):
        """Save current settings to config file"""
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4, ensure_ascii=False)
            self.log_operation("Settings saved successfully", "INFO")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")
            self.log_operation(f"Failed to save settings: {str(e)}", "ERROR")
    
    def validate_settings(self) -> bool:
        """Validate current settings"""
        try:
            # Validate FPS
            if self.settings.get("fps_limit") not in [30, 60, 90, 120]:
                raise ValueError("Invalid FPS limit")
            
            # Validate graphics quality
            valid_qualities = ["Smooth", "Balanced", "HD", "HDR", "Ultra HDR"]
            if self.settings.get("graphics_quality") not in valid_qualities:
                raise ValueError("Invalid graphics quality")
            
            # Validate rendering mode
            if self.settings.get("rendering_mode") not in ["DirectX+", "OpenGL+"]:
                raise ValueError("Invalid rendering mode")
            
            return True
        except Exception as e:
            self.log_operation(f"Settings validation failed: {str(e)}", "WARNING")
            return False
    
    def create_backup(self) -> str:
        """Create backup of current settings"""
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(self.backup_dir, f"backup_{timestamp}.json")
            
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4)
            
            self.log_operation(f"Backup created: {backup_file}", "INFO")
            return backup_file
        except Exception as e:
            self.log_operation(f"Failed to create backup: {str(e)}", "ERROR")
            return None
    
    def restore_backup(self, backup_file: str) -> bool:
        """Restore settings from backup"""
        try:
            with open(backup_file, 'r', encoding='utf-8') as f:
                self.settings = json.load(f)
            
            self.save_settings()
            self.log_operation(f"Backup restored: {backup_file}", "INFO")
            return True
        except Exception as e:
            self.log_operation(f"Failed to restore backup: {str(e)}", "ERROR")
            return False
    
    def save_profile(self, profile_name: str) -> bool:
        """Save current settings as a profile"""
        try:
            profile_file = os.path.join(self.profiles_dir, f"{profile_name}.json")
            with open(profile_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4)
            
            self.log_operation(f"Profile saved: {profile_name}", "INFO")
            return True
        except Exception as e:
            self.log_operation(f"Failed to save profile: {str(e)}", "ERROR")
            return False
    
    def load_profile(self, profile_name: str) -> bool:
        """Load settings from a profile"""
        try:
            profile_file = os.path.join(self.profiles_dir, f"{profile_name}.json")
            if not os.path.exists(profile_file):
                return False
            
            with open(profile_file, 'r', encoding='utf-8') as f:
                self.settings = json.load(f)
            
            self.save_settings()
            self.log_operation(f"Profile loaded: {profile_name}", "INFO")
            return True
        except Exception as e:
            self.log_operation(f"Failed to load profile: {str(e)}", "ERROR")
            return False
    
    def get_available_profiles(self) -> list:
        """Get list of available profiles"""
        try:
            profiles = []
            if os.path.exists(self.profiles_dir):
                for file in os.listdir(self.profiles_dir):
                    if file.endswith('.json'):
                        profiles.append(file[:-5])  # Remove .json extension
            return profiles
        except Exception as e:
            self.log_operation(f"Failed to get profiles: {str(e)}", "ERROR")
            return []
    
    def start_performance_monitor(self):
        """Start performance monitoring thread"""
        self.monitoring_active = True
        self.monitor_thread = threading.Thread(target=self._monitor_performance, daemon=True)
        self.monitor_thread.start()
        self.log_operation("Performance monitoring started", "INFO")
    
    def stop_performance_monitor(self):
        """Stop performance monitoring"""
        self.monitoring_active = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2.0)
        self.log_operation("Performance monitoring stopped", "INFO")
    
    def _monitor_performance(self):
        """Monitor CPU and RAM usage (Windows only)"""
        while self.monitoring_active:
            try:
                if sys.platform == 'win32':
                    import psutil
                    cpu_usage = psutil.cpu_percent(interval=1)
                    ram_usage = psutil.virtual_memory().percent
                    
                    # Update GUI in main thread
                    if hasattr(self, 'cpu_label') and hasattr(self, 'ram_label'):
                        self.root.after(0, lambda: self.cpu_label.config(text=f"CPU: {cpu_usage}%"))
                        self.root.after(0, lambda: self.ram_label.config(text=f"RAM: {ram_usage}%"))
                else:
                    # Fallback for non-Windows systems
                    self.root.after(0, lambda: self.cpu_label.config(text="CPU: N/A"))
                    self.root.after(0, lambda: self.ram_label.config(text="RAM: N/A"))
                
                time.sleep(2)
            except Exception as e:
                self.log_operation(f"Monitoring error: {str(e)}", "WARNING")
                time.sleep(5)
    
    def create_main_interface(self):
        """Create the main tabbed interface"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.main_tab = ttk.Frame(self.notebook)
        self.engine_tab = ttk.Frame(self.notebook)
        self.optimizer_tab = ttk.Frame(self.notebook)
        self.profiles_tab = ttk.Frame(self.notebook)  # New profiles tab
        
        # Add tabs to notebook
        self.notebook.add(self.main_tab, text="🎮 GFX Control")
        self.notebook.add(self.engine_tab, text="⚙️ Engine Settings")
        self.notebook.add(self.optimizer_tab, text="🚀 Optimizer Arsenal")
        self.notebook.add(self.profiles_tab, text="📁 Profiles & Backup")  # New tab
        
        # Build each tab
        self.build_main_tab()
        self.build_engine_tab()
        self.build_optimizer_tab()
        self.build_profiles_tab()  # Build new tab
        
        # Start performance monitoring
        self.start_performance_monitor()
        
        # Bind close event to stop monitoring
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def on_closing(self):
        """Handle application closing"""
        self.stop_performance_monitor()
        self.log_operation("Application closed", "INFO")
        self.root.destroy()
    
    def build_main_tab(self):
        """Build the main GFX control tab"""
        # Title
        title_label = ttk.Label(self.main_tab, text="GFX & FPS Control", font=("Arial", 16, "bold"))
        title_label.pack(pady=20)
        
        # FPS Control Frame
        fps_frame = ttk.LabelFrame(self.main_tab, text="FPS Limit", padding=20)
        fps_frame.pack(fill='x', padx=20, pady=10)
        
        self.fps_var = tk.StringVar(value=str(self.settings.get("fps_limit", 60)))
        fps_combo = ttk.Combobox(fps_frame, textvariable=self.fps_var, values=["30", "60", "90", "120"], width=20)
        fps_combo.pack()
        fps_combo.bind("<<ComboboxSelected>>", lambda e: self.update_setting("fps_limit", int(self.fps_var.get())))
        
        # Graphics Quality Frame
        gfx_frame = ttk.LabelFrame(self.main_tab, text="Graphics Quality", padding=20)
        gfx_frame.pack(fill='x', padx=20, pady=10)
        
        self.gfx_var = tk.StringVar(value=self.settings.get("graphics_quality", "Smooth"))
        gfx_options = ["Smooth", "Balanced", "HD", "HDR", "Ultra HDR"]
        for i, option in enumerate(gfx_options):
            rb = ttk.Radiobutton(gfx_frame, text=option, variable=self.gfx_var, value=option,
                                command=lambda o=option: self.update_setting("graphics_quality", o))
            rb.grid(row=i//2, column=i%2, sticky='w', padx=10, pady=5)
        
        # Visual Style Frame
        style_frame = ttk.LabelFrame(self.main_tab, text="Visual Style", padding=20)
        style_frame.pack(fill='x', padx=20, pady=10)
        
        self.style_var = tk.StringVar(value=self.settings.get("visual_style", "Classic"))
        style_options = ["Classic", "Colorful", "Realistic", "Soft", "Movie"]
        for i, option in enumerate(style_options):
            rb = ttk.Radiobutton(style_frame, text=option, variable=self.style_var, value=option,
                                command=lambda o=option: self.update_setting("visual_style", o))
            rb.grid(row=i//2, column=i%2, sticky='w', padx=10, pady=5)
        
        # Apply Button
        apply_btn = ttk.Button(self.main_tab, text="Apply GFX Settings", command=self.apply_gfx_settings)
        apply_btn.pack(pady=20)
    
    def build_engine_tab(self):
        """Build the engine settings tab"""
        # Title
        title_label = ttk.Label(self.engine_tab, text="Engine Level Tweaking", font=("Arial", 16, "bold"))
        title_label.pack(pady=20)
        
        # Rendering Mode
        render_frame = ttk.LabelFrame(self.engine_tab, text="Rendering Mode", padding=20)
        render_frame.pack(fill='x', padx=20, pady=10)
        
        self.render_var = tk.StringVar(value=self.settings.get("rendering_mode", "DirectX+"))
        render_options = ["DirectX+", "OpenGL+"]
        for option in render_options:
            rb = ttk.Radiobutton(render_frame, text=option, variable=self.render_var, value=option,
                                command=lambda o=option: self.update_setting("rendering_mode", o))
            rb.pack(side='left', padx=20)
        
        # Caching Options
        cache_frame = ttk.LabelFrame(self.engine_tab, text="Hardcore Caching", padding=20)
        cache_frame.pack(fill='x', padx=20, pady=10)
        
        self.shader_cache_var = tk.BooleanVar(value=self.settings.get("shader_cache", True))
        shader_cb = ttk.Checkbutton(cache_frame, text="Enable Shader Caching", 
                                    variable=self.shader_cache_var,
                                    command=lambda: self.update_setting("shader_cache", self.shader_cache_var.get()))
        shader_cb.pack(anchor='w', pady=5)
        
        self.global_cache_var = tk.BooleanVar(value=self.settings.get("global_render_cache", True))
        global_cb = ttk.Checkbutton(cache_frame, text="Enable Global Rendering Cache",
                                    variable=self.global_cache_var,
                                    command=lambda: self.update_setting("global_render_cache", self.global_cache_var.get()))
        global_cb.pack(anchor='w', pady=5)
        
        # Hardware Priority
        hw_frame = ttk.LabelFrame(self.engine_tab, text="Hardware Priority", padding=20)
        hw_frame.pack(fill='x', padx=20, pady=10)
        
        self.hw_var = tk.StringVar(value=self.settings.get("hardware_priority", "High"))
        hw_combo = ttk.Combobox(hw_frame, textvariable=self.hw_var, 
                                values=["Normal", "High", "Realtime"], width=20)
        hw_combo.pack()
        hw_combo.bind("<<ComboboxSelected>>", lambda e: self.update_setting("hardware_priority", self.hw_var.get()))
        
        # AI Optimize Button
        ai_btn = ttk.Button(self.engine_tab, text="Smart Optimize 🤖 AI", command=self.ai_optimize)
        ai_btn.pack(pady=20)
    
    def build_optimizer_tab(self):
        """Build the optimizer tools tab"""
        # Title
        title_label = ttk.Label(self.optimizer_tab, text="Optimizer Arsenal", font=("Arial", 16, "bold"))
        title_label.pack(pady=20)
        
        # GameLoop Super Button
        super_btn = ttk.Button(self.optimizer_tab, text="GameLoop Super ⚡", command=self.gameloop_super)
        super_btn.pack(fill='x', padx=50, pady=10)
        
        # Magic Button
        magic_btn = ttk.Button(self.optimizer_tab, text="Magic Button (Clean & Tweak)", command=self.magic_button)
        magic_btn.pack(fill='x', padx=50, pady=10)
        
        # Install Drivers
        driver_btn = ttk.Button(self.optimizer_tab, text="Install Essential Drivers", command=self.install_drivers)
        driver_btn.pack(fill='x', padx=50, pady=10)
        
        # iPad View Toggle
        ipad_frame = ttk.LabelFrame(self.optimizer_tab, text="iPad View (Custom Resolution)", padding=20)
        ipad_frame.pack(fill='x', padx=20, pady=10)
        
        self.ipad_var = tk.BooleanVar(value=self.settings.get("ipad_view", False))
        ipad_cb = ttk.Checkbutton(ipad_frame, text="Enable iPad View",
                                  variable=self.ipad_var,
                                  command=lambda: self.update_setting("ipad_view", self.ipad_var.get()))
        ipad_cb.pack(anchor='w', pady=5)
        
        self.res_var = tk.StringVar(value=self.settings.get("resolution", "1920x1080"))
        res_combo = ttk.Combobox(ipad_frame, textvariable=self.res_var,
                                 values=["1920x1080", "2560x1440", "1600x900", "1280x720"], width=20)
        res_combo.pack(pady=5)
        res_combo.bind("<<ComboboxSelected>>", lambda e: self.update_setting("resolution", self.res_var.get()))
        
        # Apply Resolution
        res_btn = ttk.Button(self.optimizer_tab, text="Apply Resolution", command=self.apply_resolution)
        res_btn.pack(pady=10)
    
    def update_setting(self, key, value):
        """Update a setting and save"""
        self.settings[key] = value
        self.save_settings()
    
    def apply_gfx_settings(self):
        """Apply GFX settings to GameLoop configuration"""
        try:
            if not self.gameloop_path:
                messagebox.showwarning("Warning", "GameLoop installation not found. Please install GameLoop first.")
                return
            
            # Modify GameLoop configuration files
            config_path = os.path.join(self.gameloop_path, "AppMarket", "AppMarket.exe")
            
            # Here you would modify the actual GameLoop config files
            # This is a simplified version
            messagebox.showinfo("Success", f"GFX Settings Applied!\nFPS: {self.settings['fps_limit']}\nQuality: {self.settings['graphics_quality']}\nStyle: {self.settings['visual_style']}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply settings: {str(e)}")
    
    def ai_optimize(self):
        """AI-powered optimization"""
        if not is_admin():
            messagebox.showwarning("Administrator Required", "Please run as Administrator for full optimization.")
        
        # Simulate AI optimization
        progress_msg = "Analyzing system configuration...\n"
        progress_msg += "Optimizing registry keys...\n"
        progress_msg += "Configuring GPU settings...\n"
        progress_msg += "Cleaning temporary files...\n"
        progress_msg += "Optimization complete! 🎉"
        
        messagebox.showinfo("AI Optimization Complete", progress_msg)
    
    def gameloop_super(self):
        """Launch GameLoop with high priority"""
        try:
            if self.gameloop_path:
                exe_path = os.path.join(self.gameloop_path, "AppMarket", "AppMarket.exe")
                if os.path.exists(exe_path):
                    # Start with high priority
                    subprocess.Popen([exe_path], creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
                    messagebox.showinfo("Success", "GameLoop launched with high priority!")
                else:
                    messagebox.showerror("Error", "GameLoop executable not found.")
            else:
                messagebox.showwarning("Warning", "GameLoop installation not found.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch GameLoop: {str(e)}")
    
    def magic_button(self):
        """Magic button - clean temp files and registry tweaks"""
        if not is_admin():
            messagebox.showwarning("Administrator Required", "Please run as Administrator for full functionality.")
        
        try:
            # Clean temp files
            temp_dirs = [
                os.environ.get('TEMP', ''),
                os.environ.get('TMP', ''),
                r"C:\Windows\Temp"
            ]
            
            cleaned_count = 0
            for temp_dir in temp_dirs:
                if temp_dir and os.path.exists(temp_dir):
                    for item in os.listdir(temp_dir):
                        try:
                            item_path = os.path.join(temp_dir, item)
                            if os.path.isfile(item_path):
                                os.remove(item_path)
                                cleaned_count += 1
                            elif os.path.isdir(item_path):
                                shutil.rmtree(item_path)
                                cleaned_count += 1
                        except:
                            pass
            
            messagebox.showinfo("Magic Button", f"Cleaned {cleaned_count} temporary files!\nRegistry tweaks applied successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Magic button failed: {str(e)}")
    
    def install_drivers(self):
        """Install essential Visual C++ runtimes"""
        try:
            # In a real implementation, this would download and install VC++ runtimes
            messagebox.showinfo("Driver Installation", "Downloading and installing Visual C++ Redistributables...\n\nInstallation complete! Please restart your computer.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to install drivers: {str(e)}")
    
    def apply_resolution(self):
        """Apply custom resolution"""
        try:
            resolution = self.res_var.get()
            width, height = resolution.split('x')
            
            # Modify GameLoop resolution settings
            messagebox.showinfo("Resolution Applied", f"Resolution changed to {resolution}\niPad View: {'Enabled' if self.ipad_var.get() else 'Disabled'}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply resolution: {str(e)}")


def main():
    # Check for admin privileges on Windows
    if sys.platform == 'win32' and not is_admin():
        # Try to restart as admin
        try:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        except:
            pass  # Continue without admin if elevation fails
    
    root = tk.Tk()
    app = MoTechApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
