#Requires -Version 7.0
<#
.SYNOPSIS
    Intelligent release script for version tagging

.DESCRIPTION
    Reads version from pyproject.toml, compares with latest git tag,
    and creates new tag only if version changed.

.PARAMETER DryRun
    Show what would happen without making changes

.PARAMETER GoReleaser
    Run GoReleaser after creating tag

.EXAMPLE
    .\tools\release.ps1
    .\tools\release.ps1 -DryRun
    .\tools\release.ps1 -GoReleaser
#>

[CmdletBinding()]
param(
    [switch]$DryRun,
    [switch]$GoReleaser
)

$ErrorActionPreference = "Stop"

# Get current version from pyproject.toml
$currentVersion = & python ./tools/get-version.py
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to read version from pyproject.toml"
    exit 1
}

Write-Host "Current version in pyproject.toml: " -NoNewline -ForegroundColor Green
Write-Host $currentVersion -ForegroundColor Cyan

# Get latest git tag (if any)
$latestTag = git describe --tags --abbrev=0 2>$null
if ($LASTEXITCODE -ne 0) {
    $latestTag = "none"
    Write-Host "No existing tags found" -ForegroundColor Yellow
    $latestVersion = "none"
} else {
    # Strip 'v' prefix if present
    $latestVersion = $latestTag -replace '^v', ''
    Write-Host "Latest git tag: " -NoNewline -ForegroundColor Green
    Write-Host "$latestTag " -NoNewline -ForegroundColor Cyan
    Write-Host "(version: $latestVersion)" -ForegroundColor Green
}

# Compare versions
if ($latestVersion -eq $currentVersion) {
    Write-Host "Version unchanged ($currentVersion). No new tag needed." -ForegroundColor Yellow
    exit 0
}

# Version has changed - create new tag
$newTag = "v$currentVersion"
Write-Host "Version changed: " -NoNewline -ForegroundColor Green
Write-Host "$latestVersion → $currentVersion" -ForegroundColor Cyan
Write-Host "Creating new tag: " -NoNewline -ForegroundColor Green
Write-Host $newTag -ForegroundColor Cyan

if ($DryRun) {
    Write-Host "[DRY RUN] Would create tag: $newTag" -ForegroundColor Yellow
    if ($GoReleaser) {
        Write-Host "[DRY RUN] Would run: goreleaser release" -ForegroundColor Yellow
    }
    exit 0
}

# Create the tag
git tag -a $newTag -m "Release version $currentVersion"
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to create git tag"
    exit 1
}

Write-Host "✓ Created tag: $newTag" -ForegroundColor Green

# Optionally run GoReleaser
if ($GoReleaser) {
    Write-Host "Running GoReleaser..." -ForegroundColor Green
    goreleaser release --clean
    if ($LASTEXITCODE -ne 0) {
        Write-Error "GoReleaser failed"
        exit 1
    }
    Write-Host "✓ Release created" -ForegroundColor Green
} else {
    Write-Host "Tag created locally. To push:" -ForegroundColor Yellow
    Write-Host "  git push origin main --tags" -ForegroundColor Cyan
    Write-Host "To create GitHub release:" -ForegroundColor Yellow
    Write-Host "  goreleaser release --clean" -ForegroundColor Cyan
}
