$ErrorActionPreference = "SilentlyContinue"

Write-Host "Stopping VerifyLK services..." -ForegroundColor Yellow

$ports = @(8000, 5173)
foreach ($p in $ports) {
    Get-NetTCPConnection -LocalPort $p -State Listen | ForEach-Object {
        try {
            Write-Host "Stopping process on port $p (PID $($_.OwningProcess))" -ForegroundColor Cyan
            Stop-Process -Id $_.OwningProcess -Force
        } catch {}
    }
}

Write-Host "Done. Close any remaining dev terminals if still running." -ForegroundColor Green
