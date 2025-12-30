# Claude Skills Setup with Custom Skills Support
# This script sets up Claude skills including your custom n8n-workflow-helper skill
# Compatible with PowerShell 5.1+

param(
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

function Write-Step {
    param([string]$Message)
    Write-Host "[STEP] $Message" -ForegroundColor $Cyan
}

function Write-Success {
    param([string]$Message)
    Write-Host "[OK] $Message" -ForegroundColor $Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor $Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor $Red
}

# Main execution
Write-Host ""
Write-Host "==================================================" -ForegroundColor $Magenta
Write-Host ">>> Setting up Claude skills with custom skills support..." -ForegroundColor $Magenta
Write-Host "==================================================" -ForegroundColor $Magenta

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

if (!(Test-Path ".claude")) {
    New-Item -ItemType Directory -Path ".claude" -Force | Out-Null
    Write-Success "Created .claude directory"
}

if (!(Test-Path ".claude/skills")) {
    New-Item -ItemType Directory -Path ".claude/skills" -Force | Out-Null
    Write-Success "Created .claude/skills directory"
}

# Clone official Anthropic skills
Write-Step "Setting up official Anthropic skills..."

if (!(Test-Path ".claude/skills/.git")) {
    Write-Host "[DOWNLOAD] Cloning official Anthropic skills..." -ForegroundColor $Yellow
    git clone https://github.com/anthropics/skills.git .claude/skills
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Official skills cloned successfully"
    } else {
        Write-Error "Failed to clone official skills"
        exit 1
    }
} else {
    Write-Host "[SKIP] Official skills already exist, skipping clone..." -ForegroundColor $Gray
}

# Organize official skills (move from subdirectory)
if (Test-Path ".claude/skills/skills") {
    Write-Step "Organizing official skills structure..."
    Move-Item -Path ".claude/skills/skills/*" -Destination ".claude/skills/" -Force
    if (!(Get-ChildItem ".claude/skills/skills" -Directory -ErrorAction SilentlyContinue)) {
        Remove-Item ".claude/skills/skills" -Recurse -Force
    }
    Write-Success "Official skills organized"
}

# Copy custom skills if available
if (Test-Path $CustomSkillsPath) {
    Write-Step "Adding custom skills..."
    $customSkillDirs = Get-ChildItem -Path $CustomSkillsPath -Directory -ErrorAction SilentlyContinue
    if ($customSkillDirs.Count -eq 0) {
        Write-Warning "No skill directories found in custom skills path"
    } else {
        foreach ($skillDir in $customSkillDirs) {
            $skillName = $skillDir.Name
            Write-Host "   [INFO] Copying skill: $skillName" -ForegroundColor $Gray
            Copy-Item -Path $skillDir.FullName -Destination ".claude/skills/" -Recurse -Force
        }
        Write-Success "Custom skills added ($($customSkillDirs.Count) skills)"
    }
}

# Update .gitignore to exclude .claude folder
Write-Step "Updating .gitignore..."
$gitignoreExists = Test-Path ".gitignore"
$claudeIgnored = $false

if ($gitignoreExists) {
    $content = Get-Content ".gitignore" -ErrorAction SilentlyContinue
    $claudeIgnored = $content -contains ".claude/"
}

if (!$claudeIgnored) {
    Add-Content -Path ".gitignore" -Value ".claude/"
    Write-Success ".gitignore updated to exclude .claude/"
} else {
    Write-Host "[INFO] .claude/ already in .gitignore" -ForegroundColor $Gray
}

# Sync skills with Claude
Write-Step "Syncing skills with Cursor..."
openskills sync --yes
if ($LASTEXITCODE -eq 0) {
    Write-Success "Skills synced with Cursor"
} else {
    Write-Error "Failed to sync skills: Make sure OpenSkills CLI is installed"
    exit 1
}

# Verify installation
Write-Step "Verifying installation..."
openskills list
if ($LASTEXITCODE -eq 0) {
    Write-Success "Skills installation verified"
} else {
    Write-Warning "Could not verify skills installation"
}

# Success message
Write-Host ""
Write-Host "==================================================" -ForegroundColor $Green
Write-Success "*** CLAUDE SKILLS SETUP COMPLETE! ***"
Write-Host "==================================================" -ForegroundColor $Green
Write-Host "Available skills are now active in Cursor for this project." -ForegroundColor $Cyan
Write-Host ""
Write-Host "[TIPS]:" -ForegroundColor $Cyan
Write-Host "   - Test with: Ask Cursor to 'help me create an n8n workflow'" -ForegroundColor White
Write-Host "   - Update skills: .\update-skills.ps1" -ForegroundColor White
Write-Host "   - Custom skills path: $CustomSkillsPath" -ForegroundColor White
Write-Host ""
Write-Host "==================================================" -ForegroundColor $Green
