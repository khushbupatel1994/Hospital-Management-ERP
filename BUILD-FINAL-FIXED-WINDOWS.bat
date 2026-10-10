@echo off
setlocal
cd /d "%~dp0"
echo ================================================
echo Cloud Secure Hospital ERP - FINAL FIXED BUILD
echo ================================================
python --version >nul 2>&1
if errorlevel 1 (
  echo.
  echo ERROR: Python is not available as "python".
  echo Open PowerShell and check: python --version
  pause
  exit /b 1
)
echo.
echo Installing/checking required packages...
python -m pip install --user pyinstaller customtkinter pillow pandas matplotlib openpyxl reportlab
if errorlevel 1 (
  echo.
  echo PACKAGE INSTALL FAILED.
  pause
  exit /b 1
)
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
echo.
echo Building EXE...
python -m PyInstaller --noconfirm --clean "Cloud Secure Hospital ERP.spec"
if errorlevel 1 (
  echo.
  echo BUILD FAILED.
  pause
  exit /b 1
)
echo.
echo ================================================
echo BUILD SUCCESSFUL
echo ================================================
echo EXE:
echo dist\Cloud Secure Hospital ERP\Cloud Secure Hospital ERP.exe
echo.
pause
