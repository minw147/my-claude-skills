# My Claude Skills Repository

A portable, version-controlled setup for Claude skills in Cursor, including custom skills for personal automation workflows.

## 🚀 Quick Setup (Any Computer)

```bash
# Clone this repository
git clone https://github.com/yourusername/my-claude-skills.git claude-skills-setup

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
│   └── n8n-workflow-helper/              # n8n automation helper
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
- **n8n-workflow-helper** - Comprehensive n8n automation guidance

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

### n8n-workflow-helper
**Purpose:** Comprehensive guidance for n8n automation workflows
**Features:**
- AI Agent integration patterns
- Memory management strategies
- Webhook best practices
- Error handling workflows
- Backup automation patterns

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