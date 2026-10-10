@echo off
setlocal
cd /d "%~dp0"
echo ================================================
echo Cloud Secure Hospital ERP - HOSPITAL BUILD
echo ================================================
where python >nul 2>nul
if errorlevel 1 (
  echo Python was not found.
  pause
  exit /b 1
)
python -m pip install --user --upgrade pyinstaller customtkinter pillow pandas matplotlib openpyxl reportlab bcrypt tkcalendar >nul 2>&1
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
python -m PyInstaller --noconfirm --clean "Cloud Secure Hospital ERP.spec"
if errorlevel 1 (
  echo BUILD FAILED.
  pause
  exit /b 1
)
if exist Hospital_Install rmdir /s /q Hospital_Install
mkdir Hospital_Install
xcopy /E /I /Y "dist\Cloud Secure Hospital ERP" "Hospital_Install\Cloud Secure Hospital ERP" >nul
copy /Y "HOSPITAL-DEPLOYMENT-NOTE.txt" "Hospital_Install\" >nul
copy /Y "README-HOSPITAL.txt" "Hospital_Install\" >nul
copy /Y "INSTALL-HOSPITAL.bat" "Hospital_Install\" >nul
echo.
echo BUILD SUCCESSFUL.
echo Hospital package: Hospital_Install\
pause
