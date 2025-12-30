# Claude Skills Update Script
# Run this to update your skills when new ones are added to the repository

param(
    [switch]$Force
)

Write-Host "🔄 Updating Claude Skills..." -ForegroundColor Cyan

if ($Force) {
    Write-Host "Performing clean reinstall..." -ForegroundColor Yellow
    Remove-Item ".claude/skills" -Recurse -Force -ErrorAction SilentlyContinue
    git clone https://github.com/anthropics/skills.git .claude/skills
} else {
    Write-Host "Updating existing skills..." -ForegroundColor Yellow
    if (Test-Path ".claude/skills") {
        Set-Location ".claude/skills"
        git pull origin main
        Set-Location "../.."
    } else {
        Write-Host "Skills directory not found. Performing initial install..." -ForegroundColor Yellow
        git clone https://github.com/anthropics/skills.git .claude/skills
    }
}

# Handle subdirectory structure (common in Anthropic's repo)
if (Test-Path ".claude/skills/skills") {
    Write-Host "Moving skills from subdirectory..." -ForegroundColor Yellow
    Move-Item -Path ".claude/skills/skills/*" -Destination ".claude/skills/" -Force
    if (!(Get-ChildItem ".claude/skills/skills" -Directory)) {
        Remove-Item ".claude/skills/skills" -Recurse -Force
    }
}

# Sync skills to AGENTS.md
Write-Host "Syncing skills to AGENTS.md..." -ForegroundColor Yellow
openskills sync --yes

Write-Host "✅ Skills updated successfully!" -ForegroundColor Green
Write-Host "Available skills:" -ForegroundColor Cyan
openskills list | Select-Object -First 10
