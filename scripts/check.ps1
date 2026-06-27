$ErrorActionPreference = 'Stop'

Write-Host 'Running ruff...' -ForegroundColor Cyan
python -m ruff check .

Write-Host 'Running pytest...' -ForegroundColor Cyan
python -m pytest -q

Write-Host 'OK' -ForegroundColor Green
