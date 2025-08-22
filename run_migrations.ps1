# PowerShell script to run Alembic migrations
Write-Host "SAFS Alembic Migration Runner" -ForegroundColor Cyan
Write-Host "==============================" -ForegroundColor Cyan

# Set working directory
$BackendDir = Join-Path $PSScriptRoot "backend\backend"
Write-Host "Backend directory: $BackendDir" -ForegroundColor Yellow

if (-not (Test-Path $BackendDir)) {
    Write-Host "ERROR: Backend directory not found!" -ForegroundColor Red
    exit 1
}

# Change to backend directory
Set-Location $BackendDir
Write-Host "Current directory: $(Get-Location)" -ForegroundColor Yellow

# Check if virtual environment exists
$VenvDir = Join-Path $BackendDir "venv"
$VenvPython = Join-Path $VenvDir "Scripts\python.exe"
$VenvAlembic = Join-Path $VenvDir "Scripts\alembic.exe"

if (Test-Path $VenvPython) {
    Write-Host "Using virtual environment" -ForegroundColor Green
    $PythonCmd = $VenvPython
    $AlembicCmd = if (Test-Path $VenvAlembic) { $VenvAlembic } else { "$VenvPython -m alembic" }
} else {
    Write-Host "Using system Python" -ForegroundColor Yellow
    $PythonCmd = "python"
    $AlembicCmd = "python -m alembic"
}

# Check .env file
$EnvFile = Join-Path $BackendDir ".env"
if (Test-Path $EnvFile) {
    Write-Host ".env file found" -ForegroundColor Green
    Write-Host "Environment configuration:" -ForegroundColor Yellow
    Get-Content $EnvFile | ForEach-Object {
        if ($_ -notlike "#*" -and $_ -ne "") {
            if ($_ -like "*PASSWORD*") {
                $key = ($_ -split "=")[0]
                Write-Host "  $key=****" -ForegroundColor Gray
            } else {
                Write-Host "  $_" -ForegroundColor Gray
            }
        }
    }
} else {
    Write-Host "WARNING: .env file not found" -ForegroundColor Yellow
}

Write-Host "`n=== STEP 1: Checking current Alembic status ===" -ForegroundColor Cyan
try {
    & cmd /c "$AlembicCmd current" 2>&1
    Write-Host "Current status check completed" -ForegroundColor Green
} catch {
    Write-Host "WARNING: Could not check current status: $($_.Exception.Message)" -ForegroundColor Yellow
}

Write-Host "`n=== STEP 2: Showing migration history ===" -ForegroundColor Cyan
try {
    & cmd /c "$AlembicCmd history" 2>&1
    Write-Host "History check completed" -ForegroundColor Green
} catch {
    Write-Host "WARNING: Could not show history: $($_.Exception.Message)" -ForegroundColor Yellow
}

Write-Host "`n=== STEP 3: Applying migrations ===" -ForegroundColor Cyan
try {
    & cmd /c "$AlembicCmd upgrade head" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "SUCCESS: Migrations applied successfully!" -ForegroundColor Green
    } else {
        Write-Host "ERROR: Migration failed with exit code $LASTEXITCODE" -ForegroundColor Red
        exit $LASTEXITCODE
    }
} catch {
    Write-Host "ERROR: Could not run migration: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host "`n=== STEP 4: Verifying final status ===" -ForegroundColor Cyan
try {
    & cmd /c "$AlembicCmd current" 2>&1
    Write-Host "Final status check completed" -ForegroundColor Green
} catch {
    Write-Host "WARNING: Could not verify final status: $($_.Exception.Message)" -ForegroundColor Yellow
}

Write-Host "`n==============================" -ForegroundColor Cyan
Write-Host "MIGRATION PROCESS COMPLETED" -ForegroundColor Green
Write-Host "==============================" -ForegroundColor Cyan