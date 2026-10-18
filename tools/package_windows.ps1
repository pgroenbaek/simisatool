$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RootDir = Split-Path -Parent $ScriptDir
$DistDir = Join-Path $RootDir "dist"
$VenvDir = Join-Path $RootDir ".venv"
$RequirementsFile = Join-Path $RootDir "requirements.txt"

$Python = if ($env:PYTHON) { $env:PYTHON } else { "py" }
$VenvPython = Join-Path $VenvDir "Scripts\python.exe"

Set-Location $RootDir

Write-Host "==> Creating virtual environment"
if (-not (Test-Path $VenvPython)) {
    & $Python -m venv $VenvDir

    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }
}

Write-Host "==> Installing dependencies"
& $VenvPython -m pip install --upgrade pip

if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

if (Test-Path $RequirementsFile) {
    & $VenvPython -m pip install -r $RequirementsFile

    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }
}

& $VenvPython -m pip install nuitka

if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

Write-Host "==> Cleaning dist/"
if (Test-Path $DistDir) {
    Remove-Item $DistDir -Recurse -Force
}
New-Item -ItemType Directory -Path $DistDir | Out-Null

Write-Host "==> Building Nuitka executable"
& $VenvPython -m nuitka `
    --onefile `
    --python-flag=-m `
    "--output-dir=$DistDir" `
    "--output-filename=simisatool.exe" `
    "$RootDir\simisatool"

if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

Write-Host ""
Write-Host "==> Build complete:"
Get-ChildItem $DistDir -File | Sort-Object Name