[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$root = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..\..")).Path
$env:PYTHONDONTWRITEBYTECODE = "1"
$env:PYTHONHASHSEED = "0"
python.exe -B (Join-Path $PSScriptRoot "run_tests.py")
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}
exit 0
