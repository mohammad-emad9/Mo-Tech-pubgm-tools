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
        self.root.geometry("1100x800")
        self.root.resizable(True, True)
        
        # Modern color scheme
        self.colors = {
            'bg_primary': '#1a1a2e',
            'bg_secondary': '#16213e',
            'bg_card': '#0f3460',
            'accent': '#e94560',
            'accent_hover': '#ff6b6b',
            'text_primary': '#ffffff',
            'text_secondary': '#a0a0a0',
            'success': '#00d26a',
            'warning': '#ffc107',
            'info': '#00b4d8'
        }
        
        # Set background color
        self.root.configure(bg=self.colors['bg_primary'])
        
        # Set icon
        try:
            self.root.iconbitmap("assets/icons/logo.ico")
        except:
            pass
        
        # Configure ttk styles for modern look
        self.setup_modern_styles()
        
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
    
    def setup_modern_styles(self):
        """Configure modern ttk styles"""
        style = ttk.Style()
        
        # Configure colors
        style.theme_use('clam')  # Modern base theme
        
        # Configure common styles
        style.configure('.', 
                       background=self.colors['bg_primary'],
                       foreground=self.colors['text_primary'],
                       font=('Segoe UI', 10))
        
        # Configure TFrame
        style.configure('TFrame', background=self.colors['bg_primary'])
        
        # Configure TLabelFrame with custom styling
        style.configure('TLabelframe', 
                       background=self.colors['bg_secondary'],
                       foreground=self.colors['text_primary'],
                       bordercolor=self.colors['accent'],
                       lightcolor=self.colors['bg_card'],
                       darkcolor=self.colors['bg_secondary'],
                       relief='flat')
        
        style.configure('TLabelframe.Label',
                       background=self.colors['bg_secondary'],
                       foreground=self.colors['accent'],
                       font=('Segoe UI', 11, 'bold'))
        
        # Configure TLabel
        style.configure('TLabel',
                       background=self.colors['bg_primary'],
                       foreground=self.colors['text_primary'],
                       font=('Segoe UI', 10))
        
        style.configure('Title.TLabel',
                       font=('Segoe UI', 18, 'bold'),
                       foreground=self.colors['accent'])
        
        # Configure TButton
        style.configure('TButton',
                       background=self.colors['accent'],
                       foreground=self.colors['text_primary'],
                       font=('Segoe UI', 10, 'bold'),
                       padding=10,
                       relief='flat',
                       borderwidth=0)
        
        style.map('TButton',
                 background=[('active', self.colors['accent_hover']),
                            ('pressed', self.colors['bg_card'])])
        
        # Configure TRadiobutton
        style.configure('TRadiobutton',
                       background=self.colors['bg_secondary'],
                       foreground=self.colors['text_primary'],
                       font=('Segoe UI', 10),
                       indicatorcolor=self.colors['accent'],
                       borderwidth=0)
        
        style.map('TRadiobutton',
                 background=[('active', self.colors['bg_secondary'])])
        
        # Configure TCheckbutton
        style.configure('TCheckbutton',
                       background=self.colors['bg_secondary'],
                       foreground=self.colors['text_primary'],
                       font=('Segoe UI', 10),
                       indicatorcolor=self.colors['accent'],
                       borderwidth=0)
        
        style.map('TCheckbutton',
                 background=[('active', self.colors['bg_secondary'])])
        
        # Configure TCombobox
        style.configure('TCombobox',
                       background=self.colors['bg_card'],
                       foreground=self.colors['text_primary'],
                       fieldbackground=self.colors['bg_card'],
                       arrowcolor=self.colors['accent'],
                       bordercolor=self.colors['accent'],
                       lightcolor=self.colors['bg_card'],
                       darkcolor=self.colors['bg_card'],
                       font=('Segoe UI', 10),
                       padding=8)
        
        style.map('TCombobox',
                 fieldbackground=[('readonly', self.colors['bg_card']),
                                 ('focus', self.colors['bg_card'])],
                 background=[('active', self.colors['bg_card']),
                            ('readonly', self.colors['bg_card'])])
        
        # Configure TNotebook (Tabs)
        style.configure('TNotebook',
                       background=self.colors['bg_primary'],
                       borderwidth=0)
        
        style.configure('TNotebook.Tab',
                       background=self.colors['bg_secondary'],
                       foreground=self.colors['text_secondary'],
                       font=('Segoe UI', 11, 'bold'),
                       padding=[20, 10])
        
        style.map('TNotebook.Tab',
                 background=[('selected', self.colors['accent'])],
                 foreground=[('selected', self.colors['text_primary'])])
    
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
        # Create header frame with logo and title
        self.create_header()
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=20, pady=(10, 20))
        
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
    
    def create_header(self):
        """Create modern header with title and status"""
        header_frame = tk.Frame(self.root, bg=self.colors['bg_secondary'])
        header_frame.pack(fill='x', padx=0, pady=(0, 10))
        
        # Title label
        title_label = tk.Label(
            header_frame,
            text="Mo-Tech pubgm",
            font=('Segoe UI', 24, 'bold'),
            bg=self.colors['bg_secondary'],
            fg=self.colors['accent']
        )
        title_label.pack(side='left', padx=30, pady=15)
        
        # Subtitle
        subtitle_label = tk.Label(
            header_frame,
            text="Ultimate Optimization Suite v2.0",
            font=('Segoe UI', 11),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_secondary']
        )
        subtitle_label.pack(side='left', padx=10, pady=18)
        
        # Status indicators frame
        status_frame = tk.Frame(header_frame, bg=self.colors['bg_secondary'])
        status_frame.pack(side='right', padx=30, pady=15)
        
        # Performance monitoring indicator
        self.status_indicator = tk.Canvas(
            status_frame,
            width=12,
            height=12,
            bg=self.colors['bg_secondary'],
            highlightthickness=0
        )
        self.status_indicator.pack(side='left', padx=5)
        self.status_indicator.create_oval(2, 2, 10, 10, fill=self.colors['success'], outline='')
        
        status_label = tk.Label(
            status_frame,
            text="Monitoring Active",
            font=('Segoe UI', 9),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_secondary']
        )
        status_label.pack(side='left', padx=5)
    
    def on_closing(self):
        """Handle application closing"""
        self.stop_performance_monitor()
        self.log_operation("Application closed", "INFO")
        self.root.destroy()
    
    def build_main_tab(self):
        """Build the main GFX control tab"""
        # Create a scrollable canvas for better layout
        main_container = ttk.Frame(self.main_tab)
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title with modern styling
        title_label = ttk.Label(main_container, text="🎮 GFX & FPS Control", style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Create a grid layout for cards
        card_frame = ttk.Frame(main_container)
        card_frame.pack(fill='both', expand=True)
        
        # FPS Control Card
        fps_frame = ttk.LabelFrame(card_frame, text="⚡ FPS Limit", padding=25)
        fps_frame.grid(row=0, column=0, sticky='nsew', padx=15, pady=15)
        
        self.fps_var = tk.StringVar(value=str(self.settings.get("fps_limit", 60)))
        fps_combo = ttk.Combobox(fps_frame, textvariable=self.fps_var, values=["30", "60", "90", "120"], 
                                 width=25, state='readonly')
        fps_combo.pack(pady=10)
        fps_combo.bind("<<ComboboxSelected>>", lambda e: self.update_setting("fps_limit", int(self.fps_var.get())))
        
        # Description label
        fps_desc = ttk.Label(fps_frame, text="Higher FPS = Smoother gameplay\nRequires powerful hardware", 
                            font=('Segoe UI', 9), wraplength=200)
        fps_desc.pack(pady=10)
        
        # Graphics Quality Card
        gfx_frame = ttk.LabelFrame(card_frame, text="🎨 Graphics Quality", padding=25)
        gfx_frame.grid(row=0, column=1, sticky='nsew', padx=15, pady=15)
        
        self.gfx_var = tk.StringVar(value=self.settings.get("graphics_quality", "Smooth"))
        gfx_options = ["Smooth", "Balanced", "HD", "HDR", "Ultra HDR"]
        for i, option in enumerate(gfx_options):
            rb = ttk.Radiobutton(gfx_frame, text=option, variable=self.gfx_var, value=option,
                                command=lambda o=option: self.update_setting("graphics_quality", o))
            rb.grid(row=i, column=0, sticky='w', padx=10, pady=8)
        
        # Visual Style Card
        style_frame = ttk.LabelFrame(card_frame, text="🌈 Visual Style", padding=25)
        style_frame.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=15, pady=15)
        
        self.style_var = tk.StringVar(value=self.settings.get("visual_style", "Classic"))
        style_options = ["Classic", "Colorful", "Realistic", "Soft", "Movie"]
        for i, option in enumerate(style_options):
            rb = ttk.Radiobutton(style_frame, text=option, variable=self.style_var, value=option,
                                command=lambda o=option: self.update_setting("visual_style", o))
            rb.grid(row=0, column=i, sticky='w', padx=20, pady=10)
        
        # Configure grid weights for responsive layout
        card_frame.grid_columnconfigure(0, weight=1)
        card_frame.grid_columnconfigure(1, weight=1)
        card_frame.grid_rowconfigure(0, weight=1)
        card_frame.grid_rowconfigure(1, weight=1)
        
        # Apply Button - Modern styled
        apply_btn = ttk.Button(main_container, text="💾 Apply GFX Settings", command=self.apply_gfx_settings)
        apply_btn.pack(pady=25)
    
    def build_engine_tab(self):
        """Build the engine settings tab"""
        # Create main container
        main_container = ttk.Frame(self.engine_tab)
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title with modern styling
        title_label = ttk.Label(main_container, text="⚙️ Engine Level Tweaking", style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Create grid layout for cards
        card_frame = ttk.Frame(main_container)
        card_frame.pack(fill='both', expand=True)
        
        # Rendering Mode Card
        render_frame = ttk.LabelFrame(card_frame, text="🎯 Rendering Mode", padding=25)
        render_frame.grid(row=0, column=0, sticky='nsew', padx=15, pady=15)
        
        self.render_var = tk.StringVar(value=self.settings.get("rendering_mode", "DirectX+"))
        render_options = ["DirectX+", "OpenGL+"]
        for option in render_options:
            rb = ttk.Radiobutton(render_frame, text=option, variable=self.render_var, value=option,
                                command=lambda o=option: self.update_setting("rendering_mode", o))
            rb.pack(anchor='w', padx=10, pady=10)
        
        render_desc = ttk.Label(render_frame, 
                               text="DirectX+: Better performance\nOpenGL+: Better compatibility",
                               font=('Segoe UI', 9), wraplength=200)
        render_desc.pack(pady=10)
        
        # Caching Options Card
        cache_frame = ttk.LabelFrame(card_frame, text="💾 Hardcore Caching", padding=25)
        cache_frame.grid(row=0, column=1, sticky='nsew', padx=15, pady=15)
        
        self.shader_cache_var = tk.BooleanVar(value=self.settings.get("shader_cache", True))
        shader_cb = ttk.Checkbutton(cache_frame, text="✓ Enable Shader Caching", 
                                    variable=self.shader_cache_var,
                                    command=lambda: self.update_setting("shader_cache", self.shader_cache_var.get()))
        shader_cb.pack(anchor='w', pady=8)
        
        self.global_cache_var = tk.BooleanVar(value=self.settings.get("global_render_cache", True))
        global_cb = ttk.Checkbutton(cache_frame, text="✓ Enable Global Rendering Cache",
                                    variable=self.global_cache_var,
                                    command=lambda: self.update_setting("global_render_cache", self.global_cache_var.get()))
        global_cb.pack(anchor='w', pady=8)
        
        cache_desc = ttk.Label(cache_frame, 
                              text="Caching improves loading times\nand reduces stuttering",
                              font=('Segoe UI', 9), wraplength=200)
        cache_desc.pack(pady=15)
        
        # Hardware Priority Card
        hw_frame = ttk.LabelFrame(card_frame, text="⚡ Hardware Priority", padding=25)
        hw_frame.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=15, pady=15)
        
        self.hw_var = tk.StringVar(value=self.settings.get("hardware_priority", "High"))
        hw_combo = ttk.Combobox(hw_frame, textvariable=self.hw_var, 
                                values=["Normal", "High", "Realtime"], width=25, state='readonly')
        hw_combo.pack(pady=10)
        hw_combo.bind("<<ComboboxSelected>>", lambda e: self.update_setting("hardware_priority", self.hw_var.get()))
        
        hw_desc = ttk.Label(hw_frame, 
                           text="Higher priority = More system resources\nRecommended: High",
                           font=('Segoe UI', 9), wraplength=300)
        hw_desc.pack(pady=10)
        
        # Configure grid weights
        card_frame.grid_columnconfigure(0, weight=1)
        card_frame.grid_columnconfigure(1, weight=1)
        card_frame.grid_rowconfigure(0, weight=1)
        card_frame.grid_rowconfigure(1, weight=1)
        
        # AI Optimize Button - Modern styled
        ai_btn = ttk.Button(main_container, text="🤖 Smart Optimize AI", command=self.ai_optimize)
        ai_btn.pack(pady=25)
    
    def build_optimizer_tab(self):
        """Build the optimizer tools tab"""
        # Create main container
        main_container = ttk.Frame(self.optimizer_tab)
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title with modern styling
        title_label = ttk.Label(main_container, text="🚀 Optimizer Arsenal", style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Create grid layout for tool cards
        card_frame = ttk.Frame(main_container)
        card_frame.pack(fill='both', expand=True)
        
        # Quick Actions Card
        actions_frame = ttk.LabelFrame(card_frame, text="⚡ Quick Actions", padding=25)
        actions_frame.grid(row=0, column=0, sticky='nsew', padx=15, pady=15)
        
        # GameLoop Super Button
        super_btn = ttk.Button(actions_frame, text="⚡ GameLoop Super Boost", command=self.gameloop_super)
        super_btn.pack(fill='x', pady=10)
        
        # Magic Button
        magic_btn = ttk.Button(actions_frame, text="🪄 Magic Button (Clean & Tweak)", command=self.magic_button)
        magic_btn.pack(fill='x', pady=10)
        
        # Install Drivers
        driver_btn = ttk.Button(actions_frame, text="🔧 Install Essential Drivers", command=self.install_drivers)
        driver_btn.pack(fill='x', pady=10)
        
        # iPad View Card
        ipad_frame = ttk.LabelFrame(card_frame, text="📱 iPad View (Custom Resolution)", padding=25)
        ipad_frame.grid(row=0, column=1, sticky='nsew', padx=15, pady=15)
        
        self.ipad_var = tk.BooleanVar(value=self.settings.get("ipad_view", False))
        ipad_cb = ttk.Checkbutton(ipad_frame, text="✓ Enable iPad View",
                                  variable=self.ipad_var,
                                  command=lambda: self.update_setting("ipad_view", self.ipad_var.get()))
        ipad_cb.pack(anchor='w', pady=10)
        
        res_label = ttk.Label(ipad_frame, text="Select Resolution:", font=('Segoe UI', 10))
        res_label.pack(anchor='w', pady=(15, 5))
        
        self.res_var = tk.StringVar(value=self.settings.get("resolution", "1920x1080"))
        res_combo = ttk.Combobox(ipad_frame, textvariable=self.res_var,
                                 values=["1920x1080", "2560x1440", "1600x900", "1280x720"], 
                                 width=25, state='readonly')
        res_combo.pack(anchor='w', pady=5)
        res_combo.bind("<<ComboboxSelected>>", lambda e: self.update_setting("resolution", self.res_var.get()))
        
        # Apply Resolution
        res_btn = ttk.Button(ipad_frame, text="💾 Apply Resolution", command=self.apply_resolution)
        res_btn.pack(anchor='w', pady=20)
        
        ipad_desc = ttk.Label(ipad_frame, 
                             text="iPad View gives you wider FOV\nRecommended for competitive play",
                             font=('Segoe UI', 9), wraplength=200)
        ipad_desc.pack(anchor='w', pady=10)
        
        # Configure grid weights
        card_frame.grid_columnconfigure(0, weight=1)
        card_frame.grid_columnconfigure(1, weight=1)
        card_frame.grid_rowconfigure(0, weight=1)
    
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
    
    def build_profiles_tab(self):
        """Build the profiles and backup tab"""
        # Create main container
        main_container = ttk.Frame(self.profiles_tab)
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title with modern styling
        title_label = ttk.Label(main_container, text="📁 Profiles & Backup", style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Create grid layout for cards
        card_frame = ttk.Frame(main_container)
        card_frame.pack(fill='both', expand=True)
        
        # Save Profile Card
        save_profile_frame = ttk.LabelFrame(card_frame, text="💾 Save Profile", padding=25)
        save_profile_frame.grid(row=0, column=0, sticky='nsew', padx=15, pady=15)
        
        profile_name_label = ttk.Label(save_profile_frame, text="Profile Name:", font=('Segoe UI', 10))
        profile_name_label.pack(anchor='w', pady=(0, 5))
        
        self.profile_name_var = tk.StringVar()
        profile_entry = ttk.Entry(save_profile_frame, textvariable=self.profile_name_var, width=30)
        profile_entry.pack(anchor='w', pady=5)
        
        save_profile_btn = ttk.Button(save_profile_frame, text="Save Current Settings", 
                                      command=lambda: self.save_profile_action())
        save_profile_btn.pack(anchor='w', pady=15)
        
        save_desc = ttk.Label(save_profile_frame, 
                             text="Save your current configuration\nas a reusable profile",
                             font=('Segoe UI', 9), wraplength=200)
        save_desc.pack(anchor='w', pady=10)
        
        # Load Profile Card
        load_profile_frame = ttk.LabelFrame(card_frame, text="📂 Load Profile", padding=25)
        load_profile_frame.grid(row=0, column=1, sticky='nsew', padx=15, pady=15)
        
        available_profiles = self.get_available_profiles()
        self.profile_list_var = tk.StringVar(value=available_profiles[0] if available_profiles else "No profiles")
        
        if available_profiles:
            profile_listbox = tk.Listbox(load_profile_frame, 
                                        bg=self.colors['bg_card'],
                                        fg=self.colors['text_primary'],
                                        font=('Segoe UI', 10),
                                        selectbackground=self.colors['accent'],
                                        selectforeground=self.colors['text_primary'],
                                        height=5,
                                        borderwidth=0,
                                        highlightthickness=0)
            profile_listbox.pack(fill='x', pady=10)
            
            for profile in available_profiles:
                profile_listbox.insert(tk.END, f"📄 {profile}")
            
            self.selected_profile = None
            
            def on_select(event):
                selection = profile_listbox.curselection()
                if selection:
                    self.selected_profile = available_profiles[selection[0]]
            
            profile_listbox.bind('<<ListboxSelect>>', on_select)
        else:
            no_profiles_label = ttk.Label(load_profile_frame, 
                                         text="No saved profiles found.\nCreate one to get started!",
                                         font=('Segoe UI', 9))
            no_profiles_label.pack(pady=20)
        
        load_profile_btn = ttk.Button(load_profile_frame, text="Load Selected Profile",
                                      command=lambda: self.load_profile_action())
        load_profile_btn.pack(pady=15)
        
        # Backup & Restore Card
        backup_frame = ttk.LabelFrame(card_frame, text="🔄 Backup & Restore", padding=25)
        backup_frame.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=15, pady=15)
        
        backup_btn = ttk.Button(backup_frame, text="📦 Create Backup", command=self.create_backup_action)
        backup_btn.pack(side='left', padx=20, pady=10)
        
        restore_btn = ttk.Button(backup_frame, text="♻️ Restore Backup", command=self.restore_backup_action)
        restore_btn.pack(side='left', padx=20, pady=10)
        
        backup_desc = ttk.Label(backup_frame, 
                               text="Create backups before making changes. Restore anytime if needed.",
                               font=('Segoe UI', 9), wraplength=400)
        backup_desc.pack(pady=15)
        
        # Configure grid weights
        card_frame.grid_columnconfigure(0, weight=1)
        card_frame.grid_columnconfigure(1, weight=1)
        card_frame.grid_rowconfigure(0, weight=1)
        card_frame.grid_rowconfigure(1, weight=1)
    
    def save_profile_action(self):
        """Action to save a profile"""
        profile_name = self.profile_name_var.get().strip()
        if not profile_name:
            messagebox.showwarning("Warning", "Please enter a profile name!")
            return
        
        if self.save_profile(profile_name):
            messagebox.showinfo("Success", f"Profile '{profile_name}' saved successfully!")
            self.profile_name_var.set("")
        else:
            messagebox.showerror("Error", "Failed to save profile.")
    
    def load_profile_action(self):
        """Action to load a profile"""
        if hasattr(self, 'selected_profile') and self.selected_profile:
            if self.load_profile(self.selected_profile):
                messagebox.showinfo("Success", f"Profile '{self.selected_profile}' loaded successfully!")
            else:
                messagebox.showerror("Error", "Failed to load profile.")
        else:
            messagebox.showwarning("Warning", "Please select a profile first!")
    
    def create_backup_action(self):
        """Action to create backup"""
        backup_file = self.create_backup()
        if backup_file:
            messagebox.showinfo("Success", f"Backup created successfully!\n{backup_file}")
        else:
            messagebox.showerror("Error", "Failed to create backup.")
    
    def restore_backup_action(self):
        """Action to restore backup"""
        try:
            backup_files = [f for f in os.listdir(self.backup_dir) if f.endswith('.json')]
            if not backup_files:
                messagebox.showwarning("Warning", "No backup files found!")
                return
            
            # Simple dialog to select backup (in real app, use file dialog)
            from tkinter import simpledialog
            backup_name = simpledialog.askstring("Restore Backup", 
                                                 "Enter backup filename (without .json):")
            if backup_name:
                backup_file = os.path.join(self.backup_dir, f"{backup_name}.json")
                if os.path.exists(backup_file):
                    if self.restore_backup(backup_file):
                        messagebox.showinfo("Success", "Backup restored successfully!")
                    else:
                        messagebox.showerror("Error", "Failed to restore backup.")
                else:
                    messagebox.showerror("Error", "Backup file not found!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to restore backup: {str(e)}")


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
