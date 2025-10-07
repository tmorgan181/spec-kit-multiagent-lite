# Spec-Kit Multiagent Installer - PowerShell Wrapper
# Quick functions for installing/removing kits

function Install-SpecKit {
    param(
        [string[]]$Kits,
        [switch]$Recommended,
        [switch]$All,
        [string]$Target = "."
    )

    $args = @("add")

    if ($Target -eq ".") {
        $args += "--here"
    } else {
        $args += $Target
    }

    if ($Recommended) {
        $args += "--recommended"
    } elseif ($All) {
        $args += "--kit=project,git,multiagent"
    } elseif ($Kits) {
        $args += "--kit=$($Kits -join ',')"
    }

    python -m src.speckit_multiagent.cli @args
}

function Remove-SpecKit {
    param(
        [string[]]$Kits,
        [switch]$All,
        [string]$Target = "."
    )

    $args = @("remove")

    if ($Target -eq ".") {
        $args += "--here"
    } else {
        $args += $Target
    }

    if ($All) {
        $args += "--all"
    } elseif ($Kits) {
        $args += "--kit=$($Kits -join ',')"
    }

    python -m src.speckit_multiagent.cli @args
}

function Show-SpecKitStatus {
    param(
        [string]$Target = "."
    )

    $targetPath = if ($Target -eq ".") { Get-Location } else { $Target }

    Write-Host "`nSpec-Kit Status for: $targetPath" -ForegroundColor Cyan
    Write-Host "=" * 60

    # Check Claude commands
    $claudeCommands = Get-ChildItem "$targetPath\.claude\commands" -Filter "*.md" -ErrorAction SilentlyContinue
    Write-Host "`nClaude Commands ($($claudeCommands.Count)):" -ForegroundColor Yellow
    $claudeCommands | ForEach-Object { Write-Host "  - $($_.BaseName)" }

    # Check GitHub prompts
    $ghPrompts = Get-ChildItem "$targetPath\.github\prompts" -Filter "*.md" -ErrorAction SilentlyContinue
    Write-Host "`nGitHub Prompts ($($ghPrompts.Count)):" -ForegroundColor Yellow
    $ghPrompts | ForEach-Object { Write-Host "  - $($_.BaseName)" }

    # Detect installed kits
    Write-Host "`nDetected Kits:" -ForegroundColor Yellow
    $hasProject = Test-Path "$targetPath\.claude\commands\orient.md"
    $hasGit = Test-Path "$targetPath\.claude\commands\commit.md"
    $hasMultiagent = Test-Path "$targetPath\.specify\memory\parallel-work-protocol.md"

    if ($hasProject) { Write-Host "  + project-kit" -ForegroundColor Green }
    if ($hasGit) { Write-Host "  + git-kit" -ForegroundColor Green }
    if ($hasMultiagent) { Write-Host "  + multiagent-kit" -ForegroundColor Green }
    if (-not ($hasProject -or $hasGit -or $hasMultiagent)) {
        Write-Host "  (none detected)" -ForegroundColor DarkGray
    }

    Write-Host ""
}

# Quick aliases
Set-Alias -Name "spec-install" -Value Install-SpecKit
Set-Alias -Name "spec-remove" -Value Remove-SpecKit
Set-Alias -Name "spec-status" -Value Show-SpecKitStatus

# Display usage
Write-Host @"

Spec-Kit Multiagent Installer loaded!

Quick Functions:
  Install-SpecKit -Recommended          Install project + git kits
  Install-SpecKit -All                  Install all kits
  Install-SpecKit -Kits project,git     Install specific kits

  Remove-SpecKit -All                   Remove all kits
  Remove-SpecKit -Kits git              Remove specific kits

  Show-SpecKitStatus                    Show installed kits

Aliases:
  spec-install, spec-remove, spec-status

Examples:
  spec-install -Recommended
  spec-status
  spec-remove -Kits git

"@ -ForegroundColor Cyan
