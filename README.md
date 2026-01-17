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
├── custom-skills-backup/                  # 🎯 Your custom skills
│   ├── eye-tracking-analysis/            # Eye-tracking analysis tool
│   ├── n8n-code-javascript/              # n8n JavaScript code guide
│   ├── n8n-code-python/                   # n8n Python code guide
│   ├── n8n-expression-syntax/            # n8n expression syntax
│   ├── n8n-mcp-tools-expert/             # n8n MCP tools expert
│   ├── n8n-node-configuration/           # n8n node configuration
│   ├── n8n-validation-expert/            # n8n validation expert
│   └── n8n-workflow-patterns/            # n8n workflow patterns
├── create_new_skill.ps1                   # 🛠️  Create new skills
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

### Custom Skills (Included)
- **eye-tracking-analysis** - Eye-tracking analysis tool for visual attention patterns
- **n8n-code-javascript** - JavaScript code in n8n Code nodes
- **n8n-code-python** - Python code in n8n Code nodes
- **n8n-expression-syntax** - n8n expression syntax and validation
- **n8n-mcp-tools-expert** - Expert guide for n8n-mcp MCP tools
- **n8n-node-configuration** - Operation-aware node configuration guidance
- **n8n-validation-expert** - Validation error interpretation and fixing
- **n8n-workflow-patterns** - Proven workflow architectural patterns

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
# Pull latest changes
git pull origin main

# Update official skills (handled automatically by setup script)
.\setup-claude-skills-with-custom.ps1
```

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