@echo off
setlocal
cd /d "%~dp0"
set APPDIR=%ProgramFiles%\Cloud Secure Hospital ERP
if not exist "%APPDIR%" mkdir "%APPDIR%" >nul 2>&1
if errorlevel 1 (
  echo Please run this installer as Administrator.
  pause
  exit /b 1
)
xcopy /E /I /Y "%~dp0Cloud Secure Hospital ERP" "%APPDIR%" >nul
powershell -NoProfile -ExecutionPolicy Bypass -Command "$s=(New-Object -ComObject WScript.Shell).CreateShortcut([Environment]::GetFolderPath('Desktop')+'\Cloud Secure Hospital ERP.lnk');$s.TargetPath='%APPDIR%\Cloud Secure Hospital ERP.exe';$s.WorkingDirectory='%APPDIR%';$s.Save()"
echo Hospital ERP installed.
echo Source code is not included in this installation package.
pause
