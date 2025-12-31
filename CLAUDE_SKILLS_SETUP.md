# Claude Skills Setup Guide for Cursor

This guide shows how to install Claude skills in Cursor on Windows, including workarounds for common permission issues.

## Prerequisites

- Node.js 20.6+ installed
- Git installed
- Cursor IDE

## Step 1: Install OpenSkills CLI

Install the openskills command-line tool globally:

```bash
npm install -g openskills
```

## Step 2: Add .claude Folder to .gitignore

Before installing skills, add the .claude folder to your .gitignore to prevent committing skill files to your repository:

```bash
echo ".claude/" >> .gitignore
```

## Step 3: Manual Installation (Workaround for Windows Permissions)

**Note:** The standard `openskills install anthropics/skills` and `openskills install anthropics/skills --global` commands may fail on Windows with "Security error: Installation path outside target directory" or permission issues. If you encounter these errors, use the manual installation method below:

### Clone the Anthropic Skills Repository

```bash
git clone https://github.com/anthropics/skills.git .claude/skills
```

### Move Skills to Correct Location

The skills are cloned into a subdirectory. Move them up one level:

```powershell
# PowerShell command
Move-Item -Path ".claude/skills/skills/*" -Destination ".claude/skills/" -Force
```

### Clean Up Empty Directory

Remove the now-empty skills subdirectory:

```powershell
Remove-Item ".claude/skills/skills" -Recurse -Force
```

## Step 4: Generate AGENTS.md File

Create the AGENTS.md file that Cursor will read to know about available skills:

```bash
openskills sync --yes
```

## Step 5: Verify Installation

Check that all skills are properly installed:

```bash
openskills list
```

You should see 17 skills listed, including:
- xlsx (spreadsheet creation/editing)
- docx (Word document creation)
- pdf (PDF manipulation)
- pptx (PowerPoint creation)
- canvas-design (visual design creation)
- frontend-design (web UI creation)
- algorithmic-art (generative art)
- And more...

## What Gets Created

After setup, you'll have:

```
.claude/
└── skills/
    ├── algorithmic-art/
    ├── brand-guidelines/
    ├── canvas-design/
    ├── docx/
    ├── pdf/
    ├── pptx/
    ├── xlsx/
    └── ... (14 more skills)
AGENTS.md (auto-generated)
update-skills.ps1 (optional update script)
.gitignore (updated to exclude .claude/)
```

**Cleanup:** After installation, you can safely remove any temporary HTML files (`slide*.html`) and intermediate scripts that were created during setup.

## How to Use in Cursor

Cursor automatically reads the `AGENTS.md` file. When you ask Cursor to:

- "Create an Excel spreadsheet with formulas"
- "Generate a PDF report"
- "Design a poster"
- "Create a Word document with track changes"
- "Build a React component"

Cursor will automatically use the appropriate skill for better results.

## Creating Your Own Skills

Want to create custom skills for your specific needs? Use the **skill-creator** skill and the provided script:

### Automated Skill Creation

1. **Use the creation script:**
   ```powershell
   .\create_new_skill.ps1 -SkillName "my-custom-skill" -Description "What this skill does and when to use it"
   ```

2. **Customize the generated files:**
   - `SKILL.md`: Edit the frontmatter and instructions
   - `scripts/`: Add automation scripts
   - `references/`: Add detailed documentation
   - `assets/`: Add templates and resources

3. **Move to skills directory:**
   ```powershell
   Move-Item -Path "my-custom-skill" -Destination ".claude/skills/" -Force
   ```

4. **Sync to enable:**
   ```bash
   openskills sync --yes
   ```

### Skill Structure
```
my-custom-skill/
├── SKILL.md (required - instructions & metadata)
├── scripts/ (optional - automation code)
├── references/ (optional - detailed docs)
└── assets/ (optional - templates & resources)
```

### Example: We Created n8n-workflow-helper

Following this process, we created a custom skill for n8n workflow development that provides:
- Workflow design patterns
- Node usage guidelines
- Error handling best practices
- Example workflow structures

## Real-World Example: Creating a PowerPoint Presentation

To see skills in action, try this in Cursor:

> "Create a PowerPoint presentation called 'My Presentation.pptx' with 3 slides: title slide, content slide with bullet points, and conclusion slide with key takeaways."

Cursor will use the **pptx skill** to create a professional presentation with proper formatting, layouts, and design standards - far beyond what basic AI could produce.

**Pro Tip:** For complex presentations, you can also create a JavaScript script using PptxGenJS (as demonstrated in `create_claude_skills_presentation.js`) to programmatically generate presentations with precise control over layouts, colors, and content.

## Updating Skills When New Ones Are Added

When the Anthropic skills repository adds new skills, update your local installation:

### Option 1: Pull Latest Changes (Recommended)

If you want to keep your existing setup and add new skills:

```bash
# Navigate to skills directory
cd .claude/skills

# Pull latest changes
git pull origin main

# Check if new skills are in subdirectory (common pattern)
Get-ChildItem skills -Directory

# If new skills exist in subdirectory, move them up
Move-Item -Path "skills/*" -Destination "." -Force

# Clean up if subdirectory is now empty
if (!(Get-ChildItem skills -Directory)) {
    Remove-Item skills -Recurse -Force
}

# Return to project root and sync
cd ../..
openskills sync --yes
```

### Option 2: Fresh Reinstall (Clean Slate)

For a completely clean update:

```bash
# Remove old skills
Remove-Item .claude/skills -Recurse -Force

# Reinstall fresh
git clone https://github.com/anthropics/skills.git .claude/skills
Move-Item -Path ".claude/skills/skills/*" -Destination ".claude/skills/" -Force
Remove-Item ".claude/skills/skills" -Recurse -Force
openskills sync --yes
```

### Option 3: Automated Update Script

Create a PowerShell script for easy updates:

```powershell
# Save as update-skills.ps1
param(
    [switch]$Force
)

if ($Force) {
    Write-Host "Performing clean reinstall..."
    Remove-Item ".claude/skills" -Recurse -Force -ErrorAction SilentlyContinue
    git clone https://github.com/anthropics/skills.git .claude/skills
} else {
    Write-Host "Updating existing skills..."
    Set-Location ".claude/skills"
    git pull origin main
    Set-Location "../.."
}

# Handle subdirectory structure
if (Test-Path ".claude/skills/skills") {
    Move-Item -Path ".claude/skills/skills/*" -Destination ".claude/skills/" -Force
    if (!(Get-ChildItem ".claude/skills/skills" -Directory)) {
        Remove-Item ".claude/skills/skills" -Recurse -Force
    }
}

# Sync skills
openskills sync --yes
Write-Host "Skills updated successfully!"
```

If you've followed this guide, you should have created an `update-skills.ps1` script in your project root.

Run with: `.\update-skills.ps1` or `.\update-skills.ps1 -Force` for clean reinstall.

**Quick Update Commands:**
```powershell
# Regular update (keeps your changes)
.\update-skills.ps1

# Clean reinstall (fresh start)
.\update-skills.ps1 -Force
```

## For Multiple Projects

Repeat steps 3-4 for each project where you want Claude skills:

```bash
# In each new project
git clone https://github.com/anthropics/skills.git .claude/skills
Move-Item -Path ".claude/skills/skills/*" -Destination ".claude/skills/" -Force
Remove-Item ".claude/skills/skills" -Recurse -Force
openskills sync --yes
```

### Including Custom Skills in Multiple Projects

If you have custom skills (like `n8n-workflow-helper`), you can include them in new projects:

#### Option 1: Copy Custom Skills After Setup
```powershell
# After completing basic setup above, copy your custom skills
# Note: Copy from your backup folder, not the .claude folder
Copy-Item -Path "C:\Path\To\Original\Project\custom-skills-backup\n8n-workflow-helper" -Destination ".claude/skills/" -Recurse -Force

# Sync to include the new skill
openskills sync --yes
```

**Alternative - Copy entire backup folder:**
```powershell
# Copy all custom skills at once
Copy-Item -Path "C:\Path\To\Original\Project\custom-skills-backup\*" -Destination ".claude/skills/" -Recurse -Force
openskills sync --yes
```

#### Option 2: Create a Custom Skills Repository
1. Create a GitHub repository for your custom skills
2. Push your custom skills (like `n8n-workflow-helper`) to it
3. Clone it alongside the official skills:

```bash
# Clone official skills
git clone https://github.com/anthropics/skills.git .claude/skills

# Clone your custom skills repository
git clone https://github.com/yourusername/custom-claude-skills.git .claude/custom-skills

# Move all skills to the main directory
Move-Item -Path ".claude/skills/skills/*" -Destination ".claude/skills/" -Force
Move-Item -Path ".claude/custom-skills/*" -Destination ".claude/skills/" -Force

# Clean up
Remove-Item ".claude/skills/skills" -Recurse -Force
Remove-Item ".claude/custom-skills" -Recurse -Force

# The result should be:
# .claude/skills/
# ├── algorithmic-art/
# ├── pptx/
# ├── n8n-workflow-helper/    # Your custom skill
# └── ...other skills

# Sync all skills
openskills sync --yes
```

#### Option 3: Automated Script for Custom Skills
Create a PowerShell script that includes your custom skills:

```powershell
# Save as setup-claude-skills.ps1
param(
    [string]$CustomSkillsPath = "C:\Path\To\Your\Custom\Skills"
)

# Setup official skills
git clone https://github.com/anthropics/skills.git .claude/skills
Move-Item -Path ".claude/skills/skills/*" -Destination ".claude/skills/" -Force
Remove-Item ".claude/skills/skills" -Recurse -Force

# Copy custom skills if path exists (each skill should be in its own folder)
if (Test-Path $CustomSkillsPath) {
    Get-ChildItem -Path $CustomSkillsPath -Directory | ForEach-Object {
        Copy-Item -Path $_.FullName -Destination ".claude/skills/" -Recurse -Force
    }
}

# Sync all skills
openskills sync --yes
Write-Host "Claude skills setup complete!"
```

Run with: `.\setup-claude-skills.ps1 -CustomSkillsPath "C:\Path\To\Your\Custom\Skills"`

**Note:** Your custom skills folder should be structured like:
```
C:\Path\To\Your\Custom\Skills\
├── n8n-workflow-helper\
│   ├── SKILL.md
│   ├── assets\
│   ├── references\
│   └── scripts\
└── other-custom-skill\
    └── ...
```

### Option 4: Use the Automated Setup Script (Recommended)

I've created a comprehensive setup script that handles everything automatically:

1. **Copy the setup files to your new project:**
   ```powershell
   # Copy both the script and the custom skills backup
   Copy-Item -Path "C:\Path\To\This\Project\setup-claude-skills-with-custom.ps1" -Destination "C:\Path\To\New\Project\" -Force
   Copy-Item -Path "C:\Path\To\This\Project\custom-skills-backup" -Destination "C:\Path\To\New\Project\" -Recurse -Force
   ```

2. **Run the script in the new project:**
   ```powershell
   # Navigate to the new project directory
   cd "C:\Path\To\New\Project"

   # Run the automated setup
   .\setup-claude-skills-with-custom.ps1
   ```

3. **Verify installation:**
   ```bash
   openskills list
   ```

**What the script does automatically:**
- ✅ Clones official Anthropic skills
- ✅ Copies your custom skills from `custom-skills-backup/`
- ✅ Updates `.gitignore` to exclude `.claude/`
- ✅ Syncs all skills with Claude
- ✅ Provides verification and tips

**Correct folder structure:**
```
custom-skills-backup/
└── n8n-workflow-helper/     # Each skill in its own folder
    ├── SKILL.md
    ├── assets/
    ├── references/
    └── scripts/
```

## Staying Updated

### Monitor for New Skills

- **GitHub Watch**: Consider watching the [Anthropic skills repository](https://github.com/anthropics/skills) for releases
- **Periodic Updates**: Run the update script monthly or when you notice new capabilities you'd like
- **Check Changelog**: Review the repository's changelog for new skill announcements

### When to Update

Update when:
- You want access to newly released skills
- Existing skills have bug fixes or improvements
- You notice Cursor suggesting skills you don't have
- You want to ensure compatibility with latest Cursor version

## Troubleshooting

### Permission Errors
If you get "Security error: Installation path outside target directory", use the manual installation method above.

### Skills Not Recognized
Make sure `AGENTS.md` exists and contains the skills list. Run `openskills sync --yes` to regenerate it.

### Git Issues
If `.claude` folder gets committed, add it to `.gitignore` and remove from git tracking:
```bash
echo ".claude/" >> .gitignore
git rm -r --cached .claude/
```

## Available Skills

After installation, you'll have access to:

- **xlsx**: Comprehensive spreadsheet creation, editing, and analysis with formulas
- **docx**: Document creation with tracked changes and comments
- **pdf**: PDF manipulation toolkit for extraction, creation, and forms
- **pptx**: Presentation creation and editing
- **canvas-design**: Create posters and visual designs
- **frontend-design**: Build production-grade web interfaces
- **webapp-testing**: Test web applications with Playwright
- **algorithmic-art**: Generate art using p5.js
- **mcp-builder**: Build Model Context Protocol servers
- **theme-factory**: Apply consistent themes to artifacts
- **doc-coauthoring**: Guide for collaborative documentation
- **internal-comms**: Resources for internal communications
- **skill-creator**: Guide for creating custom skills
- **slack-gif-creator**: Create animated GIFs for Slack
- **web-artifacts-builder**: Build complex HTML artifacts
- **brand-guidelines**: Apply Anthropic's brand standards
- **n8n-workflow-helper**: Create and manage n8n automation workflows

---

**Last updated:** December 30, 2025
**Tested on:** Windows 11, Cursor IDE
