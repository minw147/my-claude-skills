# Claude Skills Setup Script
# Sets up all Claude skills (official + custom) from the all-skills folder
# Compatible with PowerShell 5.1+

param(
    [string]$AllSkillsPath = "$PSScriptRoot\all-skills"
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

# Validate all-skills path
if (!(Test-Path $AllSkillsPath)) {
    Write-Error "All skills path not found: $AllSkillsPath"
    Write-Error ""
    Write-Error "The 'all-skills' folder must exist in the same directory as this script,"
    Write-Error "or use -AllSkillsPath parameter to specify the location."
    Write-Error ""
    Write-Error "Example: .\setup-claude-skills-with-custom.ps1 -AllSkillsPath 'C:\path\to\all-skills'"
    Write-Error "Or clone from GitHub: git clone https://github.com/minw147/my-claude-skills.git && cd my-claude-skills && .\setup-claude-skills-with-custom.ps1"
    exit 1
} else {
    Write-Success "Found all skills at: $AllSkillsPath"
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

# Copy all skills from all-skills folder
Write-Step "Copying all skills..."

$skillDirs = Get-ChildItem -Path $AllSkillsPath -Directory -ErrorAction SilentlyContinue
if ($skillDirs.Count -eq 0) {
    Write-Error "No skill directories found in all-skills path: $AllSkillsPath"
    Write-Error "Expected structure: all-skills/skill-name/SKILL.md"
    exit 1
}

$copiedCount = 0
$skippedCount = 0
foreach ($skillDir in $skillDirs) {
    $skillName = $skillDir.Name
    $skillMdPath = Join-Path $skillDir.FullName "SKILL.md"
    if (Test-Path $skillMdPath) {
        Write-Host "   [INFO] Copying skill: $skillName" -ForegroundColor $Gray
        Copy-Item -Path $skillDir.FullName -Destination ".claude/skills/" -Recurse -Force
        $copiedCount++
    } else {
        Write-Warning "   [SKIP] Skipping '$skillName' - missing SKILL.md file"
        $skippedCount++
    }
}

if ($copiedCount -gt 0) {
    Write-Success "Skills copied successfully ($copiedCount skills)"
    if ($skippedCount -gt 0) {
        Write-Warning "Skipped $skippedCount invalid skill directories"
    }
} else {
    Write-Error "No valid skills found to copy"
    exit 1
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
    
    # Show summary of installed skills
    $totalSkills = (Get-ChildItem ".claude/skills" -Directory | Measure-Object).Count
    Write-Host ""
    Write-Host "Total skills installed: $totalSkills" -ForegroundColor $Cyan
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
Write-Host "   - Update skills: Pull latest from GitHub and re-run this script" -ForegroundColor White
Write-Host "   - All skills source: $AllSkillsPath" -ForegroundColor White
Write-Host ""
Write-Host "==================================================" -ForegroundColor $Green
