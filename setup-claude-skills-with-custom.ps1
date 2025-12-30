#Requires -Version 5.1
<#
.SYNOPSIS
    Sets up Claude skills including custom skills for any project
.DESCRIPTION
    This script clones official Anthropic skills and adds custom skills
    to enable Claude skills functionality in Cursor IDE.
.PARAMETER CustomSkillsPath
    Path to custom skills directory (defaults to script's custom-skills-backup folder)
.EXAMPLE
    .\setup-claude-skills-with-custom.ps1
.EXAMPLE
    .\setup-claude-skills-with-custom.ps1 -CustomSkillsPath "C:\My\Custom\Skills"
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $false)]
    [ValidateNotNullOrEmpty()]
    [string]$CustomSkillsPath = "$PSScriptRoot\custom-skills-backup"
)

# Set error action preference
$ErrorActionPreference = "Stop"

# Colors for output
$Green = "Green"
$Yellow = "Yellow"
$Red = "Red"
$Cyan = "Cyan"
$Gray = "Gray"
$Magenta = "Magenta"

function Write-ColorOutput {
    param([string]$Message, [string]$Color = "White")
    Write-Host $Message -ForegroundColor $Color
}

function Write-Step {
    param([string]$Message)
    Write-ColorOutput "[STEP] $Message" $Cyan
}

function Write-Success {
    param([string]$Message)
    Write-ColorOutput "[OK] $Message" $Green
}

function Write-Warning {
    param([string]$Message)
    Write-ColorOutput "[WARNING] $Message" $Yellow
}

function Write-Error {
    param([string]$Message)
    Write-ColorOutput "[ERROR] $Message" $Red
}

# Main execution
try {
    Write-ColorOutput ""
    Write-ColorOutput "==================================================" $Magenta
    Write-ColorOutput "🚀 Setting up Claude skills with custom skills support..." $Magenta
    Write-ColorOutput "==================================================" $Magenta

    # Validate custom skills path
    if (!(Test-Path $CustomSkillsPath)) {
        Write-Warning "Custom skills path not found: $CustomSkillsPath"
        Write-Warning "Continuing with official skills only..."
        Write-Warning "Use -CustomSkillsPath parameter to specify custom skills location"
    } else {
        Write-Success "Found custom skills at: $CustomSkillsPath"
    }

    # Create .claude/skills directory if it doesn't exist
    Write-Step "Creating Claude skills directory structure..."
    try {
        if (!(Test-Path ".claude")) {
            New-Item -ItemType Directory -Path ".claude" -Force | Out-Null
            Write-Success "Created .claude directory"
        }

        if (!(Test-Path ".claude/skills")) {
            New-Item -ItemType Directory -Path ".claude/skills" -Force | Out-Null
            Write-Success "Created .claude/skills directory"
        }
    } catch {
        Write-Error "Failed to create directory structure: $($_.Exception.Message)"
        exit 1
    }

    # Clone official Anthropic skills
    Write-Step "Setting up official Anthropic skills..."
    try {
        if (!(Test-Path ".claude/skills/.git")) {
            Write-ColorOutput "📥 Cloning official Anthropic skills..." $Yellow
            $cloneResult = & git clone https://github.com/anthropics/skills.git .claude/skills 2>&1
            if ($LASTEXITCODE -ne 0) {
                throw "Git clone failed with exit code $LASTEXITCODE"
            }
            Write-Success "Official skills cloned successfully"
        } else {
            Write-ColorOutput "📁 Official skills already exist, skipping clone..." $Gray
        }
    } catch {
        Write-Error "Failed to clone official skills: $($_.Exception.Message)"
        exit 1
    }

    # Organize official skills (move from subdirectory)
    try {
        if (Test-Path ".claude/skills/skills") {
            Write-Step "Organizing official skills structure..."
            Move-Item -Path ".claude/skills/skills/*" -Destination ".claude/skills/" -Force -ErrorAction Stop
            if (!(Get-ChildItem ".claude/skills/skills" -Directory -ErrorAction SilentlyContinue)) {
                Remove-Item ".claude/skills/skills" -Recurse -Force -ErrorAction Stop
            }
            Write-Success "Official skills organized"
        }
    } catch {
        Write-Error "Failed to organize official skills: $($_.Exception.Message)"
        exit 1
    }

    # Copy custom skills if available
    if (Test-Path $CustomSkillsPath) {
        Write-Step "Adding custom skills..."
        try {
            $customSkillDirs = Get-ChildItem -Path $CustomSkillsPath -Directory -ErrorAction Stop
            if ($customSkillDirs.Count -eq 0) {
                Write-Warning "No skill directories found in custom skills path"
            } else {
                foreach ($skillDir in $customSkillDirs) {
                    $skillName = $skillDir.Name
                    Write-ColorOutput "   🔧 Copying skill: $skillName" $Gray
                    Copy-Item -Path $skillDir.FullName -Destination ".claude/skills/" -Recurse -Force -ErrorAction Stop
                }
                Write-Success "Custom skills added ($($customSkillDirs.Count) skills)"
            }
        } catch {
            Write-Error "Failed to copy custom skills: $($_.Exception.Message)"
            exit 1
        }
    }

    # Update .gitignore to exclude .claude folder
    Write-Step "Updating .gitignore..."
    try {
        $gitignoreExists = Test-Path ".gitignore"
        $claudeIgnored = $false

        if ($gitignoreExists) {
            $content = Get-Content ".gitignore" -ErrorAction Stop
            $claudeIgnored = $content -contains ".claude/"
        }

        if (!$claudeIgnored) {
            Add-Content -Path ".gitignore" -Value ".claude/" -ErrorAction Stop
            Write-Success ".gitignore updated to exclude .claude/"
        } else {
            Write-ColorOutput "📝 .claude/ already in .gitignore" $Gray
        }
    } catch {
        Write-Warning "Could not update .gitignore: $($_.Exception.Message)"
    }

    # Sync skills with Claude
    Write-Step "Syncing skills with Cursor..."
    try {
        $syncResult = & openskills sync --yes 2>&1
        if ($LASTEXITCODE -ne 0) {
            throw "OpenSkills sync failed with exit code $LASTEXITCODE"
        }
        Write-Success "Skills synced with Cursor"
    } catch {
        Write-Error "Failed to sync skills: $($_.Exception.Message)"
        Write-Error "Make sure OpenSkills CLI is installed: npm install -g openskills"
        exit 1
    }

    # Verify installation
    Write-Step "Verifying installation..."
    try {
        $listResult = & openskills list 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Skills installation verified"
        } else {
            Write-Warning "Could not verify skills list"
        }
    } catch {
        Write-Warning "Could not verify skills installation: $($_.Exception.Message)"
    }

    # Success message
    Write-ColorOutput ""
    Write-ColorOutput "==================================================" $Green
    Write-Success "🎉 CLAUDE SKILLS SETUP COMPLETE!"
    Write-ColorOutput "==================================================" $Green
    Write-ColorOutput "Available skills are now active in Cursor for this project." $Cyan
    Write-ColorOutput ""
    Write-ColorOutput "💡 Tips:" $Cyan
    Write-ColorOutput "   • Test with: Ask Cursor to 'help me create an n8n workflow'" $White
    Write-ColorOutput "   • Update skills: .\update-skills.ps1" $White
    Write-ColorOutput "   • Custom skills path: $CustomSkillsPath" $White
    Write-ColorOutput ""
    Write-ColorOutput "==================================================" $Green

} catch {
    Write-ColorOutput ""
    Write-ColorOutput "==================================================" $Red
    Write-Error "SETUP FAILED!"
    Write-ColorOutput "Error: $($_.Exception.Message)" $Red
    Write-ColorOutput "Line: $($_.InvocationInfo.ScriptLineNumber)" $Red
    Write-ColorOutput "==================================================" $Red
    Write-ColorOutput ""
    Write-ColorOutput "Troubleshooting:" $Yellow
    Write-ColorOutput "1. Make sure you have Git installed" $White
    Write-ColorOutput "2. Make sure you have Node.js and OpenSkills CLI installed" $White
    Write-ColorOutput "3. Try running as Administrator" $White
    Write-ColorOutput "4. Check internet connection" $White
    exit 1
}
