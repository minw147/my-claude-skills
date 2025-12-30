# Claude Skills Setup with Custom Skills Support
# This script sets up Claude skills including your custom n8n-workflow-helper skill

param(
    [string]$CustomSkillsPath = "$PSScriptRoot\custom-skills-backup"
)

Write-Host "🚀 Setting up Claude skills with custom skills support..." -ForegroundColor Green

# Create .claude/skills directory if it doesn't exist
if (!(Test-Path ".claude")) {
    New-Item -ItemType Directory -Path ".claude" -Force | Out-Null
}

if (!(Test-Path ".claude/skills")) {
    New-Item -ItemType Directory -Path ".claude/skills" -Force | Out-Null
}

# Clone official Anthropic skills
Write-Host "📥 Cloning official Anthropic skills..." -ForegroundColor Yellow
if (!(Test-Path ".claude/skills/.git")) {
    git clone https://github.com/anthropics/skills.git .claude/skills
} else {
    Write-Host "Official skills already cloned, skipping..." -ForegroundColor Gray
}

# Move skills from subdirectory to main skills directory
if (Test-Path ".claude/skills/skills") {
    Write-Host "📁 Organizing official skills..." -ForegroundColor Yellow
    Move-Item -Path ".claude/skills/skills/*" -Destination ".claude/skills/" -Force
    if (!(Get-ChildItem ".claude/skills/skills" -Directory)) {
        Remove-Item ".claude/skills/skills" -Recurse -Force
    }
}

# Copy custom skills if available
if (Test-Path $CustomSkillsPath) {
    Write-Host "🔧 Adding custom skills..." -ForegroundColor Yellow
    # Copy each skill directory (not the contents directly)
    Get-ChildItem -Path $CustomSkillsPath -Directory | ForEach-Object {
        $skillName = $_.Name
        Write-Host "   Copying skill: $skillName" -ForegroundColor Gray
        Copy-Item -Path $_.FullName -Destination ".claude/skills/" -Recurse -Force
    }
    Write-Host "✅ Custom skills added!" -ForegroundColor Green
} else {
    Write-Host "⚠️  Custom skills path not found: $CustomSkillsPath" -ForegroundColor Yellow
    Write-Host "   You can specify a different path with: .\setup-claude-skills-with-custom.ps1 -CustomSkillsPath 'C:\Path\To\Custom\Skills'" -ForegroundColor Gray
}

# Update .gitignore to exclude .claude folder
if (!(Test-Path ".gitignore") -or !(Select-String -Path ".gitignore" -Pattern "^\.claude/" -Quiet)) {
    Write-Host "📝 Updating .gitignore..." -ForegroundColor Yellow
    Add-Content -Path ".gitignore" -Value ".claude/"
}

# Sync skills
Write-Host "🔄 Syncing skills with Claude..." -ForegroundColor Yellow
openskills sync --yes

# Verify installation
Write-Host "✅ Setup complete! Verifying installation..." -ForegroundColor Green
openskills list

Write-Host ""
Write-Host "🎉 Claude skills setup complete!" -ForegroundColor Green
Write-Host "   Available skills are now active in Cursor for this project." -ForegroundColor White
Write-Host ""
Write-Host "💡 Tips:" -ForegroundColor Cyan
Write-Host "   • Test with: Ask Cursor to 'help me create an n8n workflow'" -ForegroundColor White
Write-Host "   • Update skills: .\update-skills.ps1" -ForegroundColor White
Write-Host "   • Custom skills path: $CustomSkillsPath" -ForegroundColor White
