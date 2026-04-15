@echo off
setlocal EnableDelayedExpansion
cd /d "%~dp0"

echo ============================================================
echo    Mo-Tech - Build Script
echo ============================================================
echo.

:: Check Python installation
echo [*] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [!] ERROR: Python is not installed or not in PATH.
    echo [!] Please install Python from https://www.python.org/downloads/
    echo [!] Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [+] Python %PYTHON_VERSION% detected.
echo.

:: Install setuptools for Python 3.14+ compatibility
echo [*] Installing setuptools (required for Python 3.14+)...
python -m pip install setuptools -q
if errorlevel 1 (
    echo [!] ERROR: Failed to install setuptools.
    pause
    exit /b 1
)
echo [+] setuptools installed successfully.
echo.

:: Install all dependencies from requirements.txt
echo [*] Installing dependencies from requirements.txt...
python -m pip install --upgrade pip -q
python -m pip install -r requirements.txt -q
if errorlevel 1 (
    echo [!] ERROR: Failed to install dependencies.
    echo [!] Check your internet connection and try again.
    pause
    exit /b 1
)
echo [+] Dependencies installed successfully.
echo.

:: Install PyInstaller separately
echo [*] Installing PyInstaller...
python -m pip install pyinstaller -q
if errorlevel 1 (
    echo [!] ERROR: Failed to install PyInstaller.
    pause
    exit /b 1
)
echo [+] PyInstaller installed successfully.
echo.

:: Verify required files exist
echo [*] Verifying required files...
if not exist "main.py" (
    echo [!] ERROR: main.py not found!
    pause
    exit /b 1
)
if not exist "assets\" (
    echo [!] ERROR: assets folder not found!
    pause
    exit /b 1
)
if not exist "assets\icons\logo.ico" (
    echo [!] WARNING: Icon file not found, build will continue without icon.
    set ICON_FLAG=
) else (
    set ICON_FLAG=--icon="assets/icons/logo.ico"
)
if not exist "images\" (
    echo [!] WARNING: images folder not found!
    set IMAGES_FLAG=
) else (
    set IMAGES_FLAG=--add-data "images;images"
)
echo [+] All required files verified.
echo.

:: Clean previous builds
echo [*] Cleaning previous builds...
if exist build rd /s /q build
if exist dist rd /s /q dist
if exist "Mo-Tech.spec" del /q "Mo-Tech.spec"
echo [+] Previous builds cleaned.
echo.

:: Build the application
echo [*] Building Mo-Tech (Mo-Tech)...
echo [*] This may take a few minutes...
echo.
python -m PyInstaller --noconfirm --onefile --windowed --name "Mo-Tech pubgm" %ICON_FLAG% --add-data "assets;assets" %IMAGES_FLAG% --hidden-import=adbutils --hidden-import=GPUtil --hidden-import=ping3 --hidden-import=psutil --hidden-import=winshell --hidden-import=wmi --hidden-import=xmltodict --hidden-import=pythoncom --hidden-import=pkg_resources --hidden-import=setuptools --hidden-import=pkg_resources.py2_warn "main.py"

if errorlevel 1 (
    echo.
    echo [!] ERROR: Build failed!
    echo [!] Check the error messages above for details.
    echo [!] Common issues:
    echo       - Missing dependencies (run: pip install -r requirements.txt)
    echo       - PyInstaller not installed (run: pip install pyinstaller)
    echo       - File permission issues (run as Administrator)
    pause
    exit /b 1
)

echo.
echo ============================================================
echo [+] BUILD SUCCESSFUL!
echo ============================================================
echo.
echo    Output: dist\Mo-Tech.exe
echo.
echo    You can now distribute the executable or create an installer.
echo    Make sure to test the built application before distributing.
echo.
echo ============================================================
pause
