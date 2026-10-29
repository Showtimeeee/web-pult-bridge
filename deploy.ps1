# Заливает проект на Cardputer и перезапускает main.py
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

function Invoke-Mpremote {
    param([Parameter(ValueFromRemainingArguments = $true)] $CommandArgs)
    mpremote @CommandArgs
    if ($LASTEXITCODE -ne 0) {
        Write-Host "mpremote завершился с ошибкой (код $LASTEXITCODE)." -ForegroundColor Red
        Write-Host "Проверь USB-кабель и что устройство видно как COM-порт." -ForegroundColor Red
        exit $LASTEXITCODE
    }
}

if (-not (Get-Command mpremote -ErrorAction SilentlyContinue)) {
    Write-Host "mpremote не найден. Установи: pip install mpremote" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path ".env")) {
    Write-Host "Внимание: .env не найден, приложение стартует на заглушках из config.py" -ForegroundColor Yellow
}

Write-Host "Заливаю файлы..."
Invoke-Mpremote connect auto cp config.py .env net.py ui.py main.py :
Invoke-Mpremote connect auto cp -r profiles :

Write-Host "Перезапускаю устройство..."
Invoke-Mpremote connect auto soft-reset

Write-Host "Готово: приложение запущено на устройстве." -ForegroundColor Green
