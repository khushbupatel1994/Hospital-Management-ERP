@echo off
setlocal
cd /d "%~dp0"
if not exist "Cloud Secure Hospital ERP\Cloud Secure Hospital ERP.exe" (
  echo Compiled application not found.
  echo Ask the developer for a complete Hospital_Install package.
  pause
  exit /b 1
)
start "Cloud Secure Hospital ERP" "Cloud Secure Hospital ERP\Cloud Secure Hospital ERP.exe"
