@echo off
setlocal
cd /d "%~dp0"
echo ================================================
echo Cloud Secure Hospital ERP - FINAL BUILD
echo ================================================
where python >nul 2>nul
if errorlevel 1 (
  echo Python was not found. Make sure `python` works in PowerShell.
  pause
  exit /b 1
)
python -m pip install --user --upgrade pyinstaller customtkinter pillow pandas matplotlib openpyxl reportlab >nul 2>&1
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
python -m PyInstaller --noconfirm --clean "Cloud Secure Hospital ERP.spec"
if errorlevel 1 (
  echo.
  echo BUILD FAILED.
  pause
  exit /b 1
)
echo.
echo BUILD SUCCESSFUL.
echo EXE: dist\Cloud Secure Hospital ERP\Cloud Secure Hospital ERP.exe
pause
