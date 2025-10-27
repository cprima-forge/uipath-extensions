#Requires -Version 7.0
<#
.SYNOPSIS
    Publishes Python package to specified repository index

.DESCRIPTION
    Publishes built Python packages to MyGet, PyPI, or TestPyPI

.PARAMETER Repository
    Target repository: myget, pypi, or testpypi (default: pypi)

.PARAMETER DryRun
    Show what would be published without uploading

.EXAMPLE
    .\tools\publish.ps1 -Repository myget
    .\tools\publish.ps1 -Repository pypi
    .\tools\publish.ps1 -DryRun
#>

[CmdletBinding()]
param(
    [Parameter()]
    [ValidateSet('myget', 'pypi', 'testpypi')]
    [string]$Repository = 'pypi',

    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

# Get current version
$currentVersion = & python ./tools/get-version.py
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to read version from pyproject.toml"
    exit 1
}

Write-Host "Current version: " -NoNewline -ForegroundColor Green
Write-Host $currentVersion -ForegroundColor Cyan

# Check if dist/ exists and has files
if (-not (Test-Path "dist") -or ((Get-ChildItem "dist" -ErrorAction SilentlyContinue).Count -eq 0)) {
    Write-Error "dist/ directory is empty or doesn't exist"
    Write-Host "Run 'make build' first to create distribution packages" -ForegroundColor Yellow
    exit 1
}

# List packages to be uploaded
Write-Host "`nPackages to upload:" -ForegroundColor Green
Get-ChildItem dist | Format-Table Name, Length, LastWriteTime -AutoSize

# Build uv publish command based on repository
$publishCmd = @("uv", "publish")

switch ($Repository) {
    'myget' {
        Write-Host "Publishing to MyGet.org..." -ForegroundColor Green

        if (-not $env:MYGET_FEED_URL) {
            Write-Error "MYGET_FEED_URL environment variable not set"
            Write-Host "Set it to your MyGet Python feed URL, e.g.:" -ForegroundColor Yellow
            Write-Host "  `$env:MYGET_FEED_URL = 'https://www.myget.org/F/your-feed/python/upload'" -ForegroundColor Cyan
            exit 1
        }

        if (-not $env:MYGET_API_KEY) {
            Write-Error "MYGET_API_KEY environment variable not set"
            Write-Host "Get your API key from MyGet feed settings" -ForegroundColor Yellow
            exit 1
        }

        $publishCmd += @(
            "--publish-url", $env:MYGET_FEED_URL,
            "--username", "myget",
            "--password", $env:MYGET_API_KEY
        )
    }

    'pypi' {
        Write-Host "Publishing to PyPI..." -ForegroundColor Green
        # uv publish defaults to PyPI
    }

    'testpypi' {
        Write-Host "Publishing to TestPyPI..." -ForegroundColor Green
        $publishCmd += @("--publish-url", "https://test.pypi.org/legacy/")
    }
}

if ($DryRun) {
    Write-Host "`n[DRY RUN] Would execute:" -ForegroundColor Yellow
    Write-Host "  $($publishCmd -join ' ')" -ForegroundColor Cyan
    exit 0
}

# Execute publish
Write-Host "`nExecuting: " -NoNewline -ForegroundColor Green
Write-Host ($publishCmd -join ' ') -ForegroundColor Cyan

& $publishCmd[0] $publishCmd[1..($publishCmd.Length-1)]

if ($LASTEXITCODE -ne 0) {
    Write-Error "Publishing failed"
    exit 1
}

Write-Host "`n✓ Package published successfully to $Repository!" -ForegroundColor Green
