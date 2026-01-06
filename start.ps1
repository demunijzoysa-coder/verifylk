param(
    [switch]$SkipInstall
)

$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$backend = Join-Path $root "backend"
$frontend = Join-Path $root "frontend"
$venv = Join-Path $backend ".venv"
$venvPython = Join-Path $venv "Scripts\python.exe"
$venvPip = Join-Path $venv "Scripts\pip.exe"

Write-Host "Starting VerifyLK services..." -ForegroundColor Cyan

if (!(Test-Path $venvPython)) {
    Write-Host "Creating backend virtualenv..." -ForegroundColor Yellow
    python -m venv $venv
}

if (-not $SkipInstall) {
    Write-Host "Installing backend requirements..." -ForegroundColor Yellow
    & $venvPip install -r (Join-Path $backend "requirements.txt")

    Write-Host "Installing frontend dependencies..." -ForegroundColor Yellow
    Push-Location $frontend
    npm install
    Pop-Location
}

$backendCmd = "cd `"$backend`"; & `"$venvPython`" -m uvicorn app.main:app --reload"
$frontendCmd = "cd `"$frontend`"; npm run dev"

Write-Host "Launching backend..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoLogo -NoExit -Command $backendCmd"

Start-Sleep -Seconds 2
Write-Host "Launching frontend..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoLogo -NoExit -Command $frontendCmd"

Write-Host "Backend: http://127.0.0.1:8000  |  Frontend: http://127.0.0.1:5173" -ForegroundColor Cyan
Write-Host "Tip: re-run with -SkipInstall for faster startup next time." -ForegroundColor DarkGray
