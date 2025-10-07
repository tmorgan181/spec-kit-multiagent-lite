# Spec-Kit Multiagent Installer - PowerShell Wrapper
# Modern CLI with autocomplete support

#region Status Helpers

function Write-StatusOk {
    param([string]$Message)
    Write-Host "[OK] " -NoNewline -ForegroundColor Green
    Write-Host $Message
}

function Write-StatusError {
    param([string]$Message)
    Write-Host "[ERROR] " -NoNewline -ForegroundColor Red
    Write-Host $Message
}

function Write-StatusWarn {
    param([string]$Message)
    Write-Host "[WARN] " -NoNewline -ForegroundColor Yellow
    Write-Host $Message
}

function Write-StatusSkip {
    param([string]$Message)
    Write-Host "[SKIP] " -NoNewline -ForegroundColor Yellow
    Write-Host $Message
}

function Write-StatusInfo {
    param([string]$Message)
    Write-Host "[INFO] " -NoNewline -ForegroundColor Cyan
    Write-Host $Message
}

#endregion

#region Banner and Help

function Show-Banner {
    Write-Host ""
    Write-Host "  ================================================================" -ForegroundColor Cyan
    Write-Host "                                                                  " -ForegroundColor Cyan
    Write-Host "    spec-kit-multiagent  -  Multi-agent coordination             " -ForegroundColor White
    Write-Host "                                                                  " -ForegroundColor Cyan
    Write-Host "  ================================================================" -ForegroundColor Cyan
    Write-Host ""
}

function Show-Help {
    param([string]$Command)

    if ($Command) {
        # Command-specific help
        switch ($Command) {
            "install" {
                Write-Host "`ninstall" -ForegroundColor Yellow
                Write-Host "  Add coordination kits to a spec-kit project`n"
                Write-Host "Usage:" -ForegroundColor Yellow
                Write-Host "  lite-kits install [-Recommended] [-All] [-Kit <names>] [-Target <path>]`n"
                Write-Host "Options:" -ForegroundColor Yellow
                Write-Host "  -Recommended       Install project + git kits (recommended for most users)"
                Write-Host "  -All               Install all kits (project + git + multiagent)"
                Write-Host "  -Kit <names>       Install specific kits (comma-separated: project,git,multiagent)"
                Write-Host "  -Target <path>     Target directory (default: current directory)"
                Write-Host "  -WhatIf            Preview what would be installed`n"
                Write-Host "Examples:" -ForegroundColor Yellow
                Write-Host "  lite-kits install -Recommended"
                Write-Host "  lite-kits install -Kit project,git"
                Write-Host "  lite-kits install -All -WhatIf"
                Write-Host ""
            }
            "remove" {
                Write-Host "`nremove" -ForegroundColor Yellow
                Write-Host "  Remove coordination kits from a spec-kit project`n"
                Write-Host "Usage:" -ForegroundColor Yellow
                Write-Host "  lite-kits remove [-All] [-Kit <names>] [-Target <path>] [-Force]`n"
                Write-Host "Options:" -ForegroundColor Yellow
                Write-Host "  -All               Remove all kits"
                Write-Host "  -Kit <names>       Remove specific kits (comma-separated)"
                Write-Host "  -Target <path>     Target directory (default: current directory)"
                Write-Host "  -Force             Skip confirmation prompt`n"
                Write-Host "Examples:" -ForegroundColor Yellow
                Write-Host "  lite-kits remove -Kit git"
                Write-Host "  lite-kits remove -All"
                Write-Host "  lite-kits remove -All -Force"
                Write-Host ""
            }
            "status" {
                Write-Host "`nstatus" -ForegroundColor Yellow
                Write-Host "  Show installed kits and available commands`n"
                Write-Host "Usage:" -ForegroundColor Yellow
                Write-Host "  lite-kits status [-Target <path>]`n"
                Write-Host "Options:" -ForegroundColor Yellow
                Write-Host "  -Target <path>     Target directory (default: current directory)`n"
                Write-Host "Examples:" -ForegroundColor Yellow
                Write-Host "  lite-kits status"
                Write-Host "  lite-kits status -Target c:\projects\my-app"
                Write-Host ""
            }
            default {
                Show-MainHelp
            }
        }
    } else {
        Show-MainHelp
    }
}

function Show-MainHelp {
    Show-Banner

    Write-Host "A modular multi-agent coordination add-on for GitHub spec-kit`n" -ForegroundColor Gray

    Write-Host "Usage:" -ForegroundColor Yellow
    Write-Host "  lite-kits <COMMAND> [OPTIONS]`n"

    Write-Host "Commands:" -ForegroundColor Yellow
    Write-Host "  install            Add coordination kits to a project"
    Write-Host "  remove             Remove kits from a project"
    Write-Host "  status             Show installed kits and commands"
    Write-Host "  help               Display help for a command`n"

    Write-Host "Kit Options:" -ForegroundColor Yellow
    Write-Host "  -Recommended       Install project + git kits"
    Write-Host "  -All               Install/remove all kits"
    Write-Host "  -Kit <names>       Specific kits: project, git, multiagent`n"

    Write-Host "Global Options:" -ForegroundColor Yellow
    Write-Host "  -Target <path>     Target directory (default: current directory)"
    Write-Host "  -WhatIf            Preview changes without applying"
    Write-Host "  -Verbose           Show detailed output"
    Write-Host "  -Force             Skip confirmation prompts`n"

    Write-Host "Examples:" -ForegroundColor Yellow
    Write-Host "  lite-kits install -Recommended      # Install recommended kits"
    Write-Host "  lite-kits status                    # Check what's installed"
    Write-Host "  lite-kits remove -Kit git           # Remove git-kit only"
    Write-Host "  lite-kits help install              # Get help for install command`n"

    Write-Host "Use " -NoNewline -ForegroundColor Gray
    Write-Host "lite-kits help <command>" -NoNewline -ForegroundColor White
    Write-Host " for more information on a specific command." -ForegroundColor Gray
    Write-Host ""
}

#endregion

#region Core Commands

function Invoke-LiteKitsInstall {
    [CmdletBinding(SupportsShouldProcess = $true)]
    param(
        [Parameter(Position = 0)]
        [string[]]$Kit,

        [switch]$Recommended,
        [switch]$All,
        [string]$Target = ".",
        [switch]$Force
    )

    # Validate kits
    $validKits = @("project", "git", "multiagent")
    if ($Kit) {
        $invalidKits = $Kit | Where-Object { $_ -notin $validKits }
        if ($invalidKits) {
            Write-StatusError "Invalid kit(s): $($invalidKits -join ', ')"
            Write-Host "Valid kits: " -NoNewline -ForegroundColor Gray
            Write-Host ($validKits -join ', ') -ForegroundColor Yellow
            return
        }
    }

    $cliArgs = @("add")

    if ($Target -eq ".") {
        $cliArgs += "--here"
    } else {
        $cliArgs += $Target
    }

    if ($Recommended) {
        $cliArgs += "--recommended"
        Write-Host "`nInstalling recommended kits: " -NoNewline -ForegroundColor Cyan
        Write-Host "project, git" -ForegroundColor White
    } elseif ($All) {
        $cliArgs += "--kit=project,git,multiagent"
        Write-Host "`nInstalling all kits: " -NoNewline -ForegroundColor Cyan
        Write-Host "project, git, multiagent" -ForegroundColor White
    } elseif ($Kit) {
        $cliArgs += "--kit=$($Kit -join ',')"
        Write-Host "`nInstalling kits: " -NoNewline -ForegroundColor Cyan
        Write-Host ($Kit -join ', ') -ForegroundColor White
    } else {
        Write-StatusError "Must specify -Recommended, -All, or -Kit <names>"
        Write-Host "Run " -NoNewline -ForegroundColor Gray
        Write-Host "lite-kits help install" -NoNewline -ForegroundColor White
        Write-Host " for usage." -ForegroundColor Gray
        return
    }

    if ($PSCmdlet.ShouldProcess("Install Spec-Kit kits", "Run: python -m src.speckit_multiagent.cli $($cliArgs -join ' ')")) {
        Write-Host ""
        & python -m src.speckit_multiagent.cli @cliArgs 2>&1 | Out-Host

        if ($LASTEXITCODE -eq 0) {
            Write-Host ""
            Write-StatusOk "Installation completed!"
        } else {
            Write-Host ""
            Write-StatusError "Installation failed (exit code: $LASTEXITCODE)"
        }
    }
}

function Invoke-LiteKitsRemove {
    [CmdletBinding(SupportsShouldProcess = $true, ConfirmImpact = 'High')]
    param(
        [Parameter(Position = 0)]
        [string[]]$Kit,

        [switch]$All,
        [string]$Target = ".",
        [switch]$Force
    )

    # Validate kits
    $validKits = @("project", "git", "multiagent")
    if ($Kit) {
        $invalidKits = $Kit | Where-Object { $_ -notin $validKits }
        if ($invalidKits) {
            Write-StatusError "Invalid kit(s): $($invalidKits -join ', ')"
            Write-Host "Valid kits: " -NoNewline -ForegroundColor Gray
            Write-Host ($validKits -join ', ') -ForegroundColor Yellow
            return
        }
    }

    $cliArgs = @("remove")

    if ($Target -eq ".") {
        $cliArgs += "--here"
    } else {
        $cliArgs += $Target
    }

    if ($All) {
        $cliArgs += "--all"
        Write-Host "`nRemoving all kits" -ForegroundColor Yellow
    } elseif ($Kit) {
        $cliArgs += "--kit=$($Kit -join ',')"
        Write-Host "`nRemoving kits: " -NoNewline -ForegroundColor Yellow
        Write-Host ($Kit -join ', ') -ForegroundColor White
    } else {
        Write-StatusError "Must specify -All or -Kit <names>"
        Write-Host "Run " -NoNewline -ForegroundColor Gray
        Write-Host "lite-kits help remove" -NoNewline -ForegroundColor White
        Write-Host " for usage." -ForegroundColor Gray
        return
    }

    if ($Force -or $PSCmdlet.ShouldProcess("Remove Spec-Kit kits", "Run: python -m src.speckit_multiagent.cli $($cliArgs -join ' ')")) {
        Write-Host ""
        & python -m src.speckit_multiagent.cli @cliArgs 2>&1 | Out-Host

        if ($LASTEXITCODE -eq 0) {
            Write-Host ""
            Write-StatusOk "Removal completed!"
        } else {
            Write-Host ""
            Write-StatusError "Removal failed (exit code: $LASTEXITCODE)"
        }
    }
}

function Invoke-LiteKitsStatus {
    [CmdletBinding()]
    param(
        [string]$Target = "."
    )

    $targetPath = if ($Target -eq ".") { Get-Location } else { Resolve-Path $Target -ErrorAction SilentlyContinue }

    if (-not $targetPath) {
        Write-StatusError "Target directory not found: $Target"
        return
    }

    Write-Host "`nStatus for: " -NoNewline -ForegroundColor Yellow
    Write-Host $targetPath -ForegroundColor White
    Write-Host ("=" * 65) -ForegroundColor DarkGray

    # Check Claude commands
    $claudePath = Join-Path $targetPath ".claude\commands"
    $claudeCommands = Get-ChildItem $claudePath -Filter "*.md" -ErrorAction SilentlyContinue
    Write-Host "`nClaude Commands " -NoNewline -ForegroundColor Yellow
    Write-Host "($($claudeCommands.Count)):" -ForegroundColor Gray
    if ($claudeCommands) {
        $claudeCommands | ForEach-Object {
            Write-Host "  - " -NoNewline -ForegroundColor DarkGray
            Write-Host $_.BaseName -ForegroundColor White
        }
    } else {
        Write-Host "  (none)" -ForegroundColor DarkGray
    }

    # Check GitHub prompts
    $ghPath = Join-Path $targetPath ".github\prompts"
    $ghPrompts = Get-ChildItem $ghPath -Filter "*.md" -ErrorAction SilentlyContinue
    Write-Host "`nGitHub Prompts " -NoNewline -ForegroundColor Yellow
    Write-Host "($($ghPrompts.Count)):" -ForegroundColor Gray
    if ($ghPrompts) {
        $ghPrompts | ForEach-Object {
            Write-Host "  - " -NoNewline -ForegroundColor DarkGray
            Write-Host $_.BaseName -ForegroundColor White
        }
    } else {
        Write-Host "  (none)" -ForegroundColor DarkGray
    }

    # Detect installed kits
    Write-Host "`nInstalled Kits:" -ForegroundColor Yellow
    $hasProject = Test-Path (Join-Path $targetPath ".claude\commands\orient.md")
    $hasGit = Test-Path (Join-Path $targetPath ".claude\commands\commit.md")
    $hasMultiagent = Test-Path (Join-Path $targetPath ".specify\memory\parallel-work-protocol.md")

    if ($hasProject) {
        Write-Host "  " -NoNewline
        Write-Host "[OK] " -NoNewline -ForegroundColor Green
        Write-Host "project-kit"
    }
    if ($hasGit) {
        Write-Host "  " -NoNewline
        Write-Host "[OK] " -NoNewline -ForegroundColor Green
        Write-Host "git-kit"
    }
    if ($hasMultiagent) {
        Write-Host "  " -NoNewline
        Write-Host "[OK] " -NoNewline -ForegroundColor Green
        Write-Host "multiagent-kit"
    }
    if (-not ($hasProject -or $hasGit -or $hasMultiagent)) {
        Write-Host "  " -NoNewline
        Write-Host "[SKIP] " -NoNewline -ForegroundColor Yellow
        Write-Host "No kits detected" -ForegroundColor DarkGray
    }

    Write-Host ""
}

#endregion

#region Main Dispatcher

function global:Invoke-LiteKits {
    [CmdletBinding()]
    param(
        [Parameter(Position = 0, Mandatory = $false)]
        [ValidateSet('install', 'remove', 'status', 'help')]
        [string]$Command,

        [Parameter(ValueFromRemainingArguments = $true)]
        $RemainingArgs
    )

    if (-not $Command -or $Command -eq 'help') {
        if ($RemainingArgs -and $RemainingArgs[0]) {
            Show-Help -Command $RemainingArgs[0]
        } else {
            Show-Help
        }
        return
    }

    # Parse remaining args into proper parameters
    $params = @{}
    $i = 0
    while ($i -lt $RemainingArgs.Count) {
        $arg = $RemainingArgs[$i]

        if ($arg -match '^-(\w+)$') {
            $paramName = $Matches[1]

            # Check if it's a switch or has a value
            if ($i + 1 -lt $RemainingArgs.Count -and $RemainingArgs[$i + 1] -notmatch '^-') {
                $params[$paramName] = $RemainingArgs[$i + 1]
                $i += 2
            } else {
                $params[$paramName] = $true
                $i++
            }
        } else {
            $i++
        }
    }

    switch ($Command) {
        'install' { Invoke-LiteKitsInstall @params }
        'remove'  { Invoke-LiteKitsRemove @params }
        'status'  { Invoke-LiteKitsStatus @params }
    }
}

# Create alias in global scope (use -Force to allow re-sourcing)
if (Get-Alias -Name 'lite-kits' -ErrorAction SilentlyContinue) {
    Remove-Alias -Name 'lite-kits' -Force -ErrorAction SilentlyContinue
}
Set-Alias -Name 'lite-kits' -Value Invoke-LiteKits -Scope Global

#endregion

#region Tab Completion

# Register argument completer for the lite-kits command
Register-ArgumentCompleter -CommandName Invoke-LiteKits -ParameterName Command -ScriptBlock {
    param($commandName, $parameterName, $wordToComplete, $commandAst, $fakeBoundParameters)

    @('install', 'remove', 'status', 'help') | Where-Object { $_ -like "$wordToComplete*" } | ForEach-Object {
        [System.Management.Automation.CompletionResult]::new($_, $_, 'ParameterValue', $_)
    }
}

# Register argument completer for -Kit parameter
Register-ArgumentCompleter -CommandName Invoke-LiteKitsInstall, Invoke-LiteKitsRemove -ParameterName Kit -ScriptBlock {
    param($commandName, $parameterName, $wordToComplete, $commandAst, $fakeBoundParameters)

    @('project', 'git', 'multiagent') | Where-Object { $_ -like "$wordToComplete*" } | ForEach-Object {
        [System.Management.Automation.CompletionResult]::new($_, $_, 'ParameterValue', $_)
    }
}

#endregion

# Show banner on load
Show-Banner
Write-Host "Type " -NoNewline -ForegroundColor Gray
Write-Host "lite-kits help" -NoNewline -ForegroundColor White
Write-Host " for usage information" -ForegroundColor Gray
Write-Host ""
