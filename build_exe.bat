@echo off
REM ============================================================
REM  build_exe.bat - builds ARCTIC.exe via PyInstaller
REM  Just double-click to run (keep this file in the project folder,
REM  next to arctic.py, router.py, config.py, arctic_config.json)
REM ============================================================

echo.
echo === ARCTIC Build Script ===
echo.



REM --- Check whether Python itself is available ---
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python was not found in PATH.
    echo Install Python from https://python.org and make sure
    echo "Add python.exe to PATH" is checked during installation.
    pause
    exit /b 1
)



REM --- Install dependencies from pyproject.toml ---
echo [INFO] Installing required dependencies...
python -m pip install -e .
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)



REM --- Check whether PyInstaller is installed, install it if missing ---
python -m PyInstaller --version >nul 2>&1
if errorlevel 1 (
    echo [INFO] PyInstaller not found - installing it now...
    python -m pip install --upgrade pip >nul 2>&1
    python -m pip install pyinstaller
    if errorlevel 1 (
        echo [ERROR] Failed to install PyInstaller. Check your internet
        echo connection or install it manually with: pip install pyinstaller
        pause
        exit /b 1
    )
    echo [OK] PyInstaller installed successfully.
) else (
    echo [OK] PyInstaller found.
)



echo.
echo Building ARCTIC.exe, please wait...
echo.

REM --- Actual build command ---
REM --distpath . places the finished .exe directly in this folder,
REM next to arctic.py and the other project files.
python -m PyInstaller --onefile --windowed --icon=icon.ico --distpath . --name ARCTIC arctic.py

REM --- Check whether the build actually succeeded ---
if not exist "ARCTIC.exe" (
    echo.
    echo [ERROR] Build failed.
    pause
    exit /b 1
)

echo.
echo [OK] Build successful: ARCTIC.exe



REM --- Clean up temporary PyInstaller files ---
REM "build" folder and the .spec file are only needed during the build
REM itself - safe to delete afterwards, PyInstaller recreates them
REM automatically on the next run.
if exist "build" (
    rmdir /s /q build
    echo [OK] Removed temporary "build" folder
)

if exist "ARCTIC.spec" (
    del /q ARCTIC.spec
    echo [OK] Removed ARCTIC.spec
)



echo.
echo Done! ARCTIC.exe is ready in this folder.
pause