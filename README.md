# My Claude Skills Repository

A portable, version-controlled setup for Claude skills in Cursor, including custom skills for personal automation workflows.

## 🚀 Quick Setup (Any Computer)

```bash
# Clone this repository
git clone https://github.com/minw147/my-claude-skills.git claude-skills-setup

# Navigate to the directory
cd claude-skills-setup

# Run the automated setup
.\setup-claude-skills-with-custom.ps1
```

**That's it!** Your Claude skills are now ready in Cursor.

## 📁 Repository Contents

```
my-claude-skills/
├── setup-claude-skills-with-custom.ps1    # 🚀 Main setup script
├── all-skills/                            # 🎯 All skills (official + custom)
│   ├── algorithmic-art/                     # Official: Algorithmic art creation
│   ├── brainstorming/                    # Custom: Design refinement
│   ├── brand-guidelines/                 # Official: Brand styling
│   ├── canvas-design/                    # Official: Visual design
│   ├── docx/                             # Official: Word documents
│   ├── eye-tracking-analysis/            # Custom: Eye-tracking analysis
│   ├── n8n-code-javascript/             # Custom: n8n JavaScript
│   ├── n8n-code-python/                  # Custom: n8n Python
│   ├── n8n-expression-syntax/            # Custom: n8n expressions
│   ├── n8n-mcp-tools-expert/             # Custom: n8n MCP tools
│   ├── n8n-node-configuration/           # Custom: n8n node config
│   ├── n8n-validation-expert/            # Custom: n8n validation
│   ├── n8n-workflow-patterns/            # Custom: n8n patterns
│   ├── pdf/                              # Official: PDF manipulation
│   ├── pptx/                             # Official: PowerPoint
│   ├── systematic-debugging/             # Custom: Debugging workflow
│   ├── test-driven-development/          # Custom: TDD workflow
│   ├── xlsx/                             # Official: Excel/spreadsheets
│   └── ... (39 total skills)
├── custom-skills-backup/                  # 📦 Legacy backup (can be removed)
├── create_new_skill.ps1                  # 🛠️  Create new skills
├── update-skills.ps1                      # 🔄 Update existing skills
├── README.md                              # 📖 This file
└── .gitignore                            # 🚫 Ignore generated files
```

## 🎯 What Gets Installed

### Official Skills (Auto-downloaded)
- **xlsx** - Excel/spreadsheet creation
- **pptx** - PowerPoint presentations
- **docx** - Word document creation
- **pdf** - PDF manipulation
- **frontend-design** - Web UI components
- And 14+ more official skills from Anthropic

### All Skills (Included - Official + Custom)
This repository includes **all 39 skills** in one place:
- **Official Anthropic Skills** (17 skills) - xlsx, docx, pdf, pptx, frontend-design, algorithmic-art, and more
- **Custom Skills** (22 skills):
  - **eye-tracking-analysis** - Eye-tracking analysis tool for visual attention patterns
  - **n8n Skills Suite** (7 skills) - Expert guidance for building production-ready n8n workflows
  - **Superpowers Skills Suite** (14 skills) - Complete software development workflow for coding agents

**Benefits:** Single source of truth, no need to clone multiple repositories, simpler setup!

## 🔧 Development Workflow

### Adding New Custom Skills
```bash
# Create a new skill
.\create_new_skill.ps1 -SkillName "my-new-skill" -Description "What it does"

# Edit the generated SKILL.md file
# Add your scripts, references, and assets

# Test the skill locally
openskills sync --yes

# Commit and push
git add .
git commit -m "Add my-new-skill"
git push
```

### Updating Skills
```bash
# Pull latest changes from this repository
git pull origin main

# Re-run setup to get updated skills
.\setup-claude-skills-with-custom.ps1
```

**Note:** To update official Anthropic skills, you'll need to manually pull from their repository and copy to `all-skills/`, or wait for this repository to be updated.

## 🛡️ Reliability Features

### Encoding Protection
- **`.gitattributes` file** ensures proper line endings for PowerShell scripts
- **UTF-8 BOM handling** prevents parsing errors during cloning
- **Cross-platform compatibility** for Windows/Unix environments

### Error Handling
- **Comprehensive try-catch blocks** for all critical operations
- **Detailed error messages** with troubleshooting guidance
- **Graceful degradation** when custom skills are unavailable
- **Validation checks** before executing operations

### Robustness Improvements
- **PowerShell best practices** with `CmdletBinding` and parameter validation
- **Path validation** and existence checks
- **Git operation verification** with exit code checking
- **Fallback behaviors** for various failure scenarios

## 🖥️ Using on Multiple Computers

### First Time Setup
```bash
# On any computer with Git
git clone https://github.com/yourusername/my-claude-skills.git
cd my-claude-skills
.\setup-claude-skills-with-custom.ps1
```

### Staying Updated
```bash
# On any computer
cd my-claude-skills
git pull
.\setup-claude-skills-with-custom.ps1
```

## 📋 Included Custom Skills

### eye-tracking-analysis
**Purpose:** AI-powered eye-tracking analysis using Spectral Residual Saliency methodology
**Features:**
- Heat map generation with color-coded attention zones
- Fixation sequence prediction
- AOI (Areas of Interest) analysis
- Website landing page analysis
- Professional report generation with PDF export

### n8n Skills Suite (7 Complementary Skills)
**Purpose:** Expert guidance for building production-ready n8n workflows using n8n-mcp MCP server

**Skills:**
1. **n8n-expression-syntax** - Validate n8n expression syntax and fix common errors
2. **n8n-mcp-tools-expert** - Expert guide for using n8n-mcp MCP tools effectively (HIGHEST PRIORITY)
3. **n8n-workflow-patterns** - Proven workflow architectural patterns from real n8n workflows
4. **n8n-validation-expert** - Interpret validation errors and guide fixing them
5. **n8n-node-configuration** - Operation-aware node configuration guidance
6. **n8n-code-javascript** - Write JavaScript code in n8n Code nodes
7. **n8n-code-python** - Write Python code in n8n Code nodes

**Features:**
- Correct n8n expression syntax ({{}} patterns)
- Effective use of n8n-mcp tools
- Proven workflow patterns from 2,653+ templates
- Validation error interpretation and fixing
- Operation-aware node configuration
- Production-tested Code node patterns

### Superpowers Skills Suite (14 Complementary Skills)
**Purpose:** Complete software development workflow for coding agents, built on composable skills that ensure systematic, test-driven development

**Testing:**
- **test-driven-development** - RED-GREEN-REFACTOR cycle with testing anti-patterns reference

**Debugging:**
- **systematic-debugging** - 4-phase root cause process with root-cause-tracing, defense-in-depth, and condition-based-waiting techniques
- **verification-before-completion** - Ensure it's actually fixed before claiming success

**Collaboration:**
- **brainstorming** - Socratic design refinement before creative work
- **writing-plans** - Detailed implementation plans with bite-sized tasks
- **executing-plans** - Batch execution with review checkpoints
- **dispatching-parallel-agents** - Concurrent subagent workflows for independent tasks
- **requesting-code-review** - Pre-review checklist before merging
- **receiving-code-review** - Responding to feedback with technical rigor
- **using-git-worktrees** - Parallel development branches with isolation
- **finishing-a-development-branch** - Merge/PR decision workflow
- **subagent-driven-development** - Fast iteration with two-stage review (spec compliance, then code quality)

**Meta:**
- **writing-skills** - Create new skills following best practices with testing methodology
- **using-superpowers** - Introduction to the skills system and how to find/use skills

**Features:**
- Test-Driven Development (TDD) enforcement
- Systematic debugging over ad-hoc guessing
- Complexity reduction and simplicity focus
- Evidence-based verification before assertions
- Mandatory workflows, not suggestions
- Skills trigger automatically based on context

## 🔒 Security & Git

### What's Tracked
- ✅ Custom skills and their code
- ✅ Setup scripts and utilities
- ✅ Documentation and guides

### What's Ignored
- ❌ Official Anthropic skills (auto-downloaded)
- ❌ Generated `.claude/` directory
- ❌ Dependencies and logs

## 🆘 Troubleshooting

### Setup Fails
1. Ensure PowerShell execution policy allows scripts:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
2. Install OpenSkills CLI: `npm install -g openskills`

### Skills Not Installed
**Problem:** Script runs but skills don't appear in AGENTS.md

**Cause:** The script looks for `all-skills` folder in the same directory as the script. If you only copied the script file, the folder isn't there.

**Solutions:**

1. **Clone the entire repository (Recommended):**
   ```powershell
   # Clone the repository
   git clone https://github.com/minw147/my-claude-skills.git
   cd my-claude-skills
   # Run the script (it will find all-skills automatically)
   .\setup-claude-skills-with-custom.ps1
   ```

2. **Point to a different location:**
   ```powershell
   .\setup-claude-skills-with-custom.ps1 -AllSkillsPath "C:\path\to\all-skills"
   ```

**Verify installation:**
```powershell
# Check if skills are in .claude/skills
Get-ChildItem ".claude\skills" -Directory | Measure-Object

# Re-sync if needed
openskills sync --yes
```

### Skills Not Recognized
1. Run: `openskills sync --yes`
2. Restart Cursor
3. Check: `openskills list`

### Permission Issues
- Run PowerShell as Administrator
- Or use: `powershell.exe -ExecutionPolicy Bypass -File script.ps1`

## 🤝 Contributing

### Adding Skills
1. Use `create_new_skill.ps1` to create the structure
2. Follow the SKILL.md format
3. Test locally before committing
4. Update this README

### Repository Structure
- Keep official skills out (they're downloaded by script)
- One skill per directory in `custom-skills-backup/`
- Clear naming and documentation

## 📞 Support

- **Issues:** Check the troubleshooting section above
- **Updates:** Official skills update automatically
- **Custom Skills:** Modify and commit to this repository

---

**Created:** December 30, 2025
**Maintained by:** [Your Name]
**License:** Personal use