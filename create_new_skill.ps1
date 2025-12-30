# Claude Skill Creator Script
# Creates a new skill with proper structure

param(
    [Parameter(Mandatory=$true)]
    [string]$SkillName,
    [string]$Description,
    [string]$OutputPath = "."
)

$SkillPath = Join-Path $OutputPath $SkillName

Write-Host "Creating new Claude skill: $SkillName" -ForegroundColor Green
Write-Host "Location: $SkillPath" -ForegroundColor Yellow

# Create skill directory structure
New-Item -ItemType Directory -Path $SkillPath -Force | Out-Null
New-Item -ItemType Directory -Path "$SkillPath/scripts" -Force | Out-Null
New-Item -ItemType Directory -Path "$SkillPath/references" -Force | Out-Null
New-Item -ItemType Directory -Path "$SkillPath/assets" -Force | Out-Null

# Create SKILL.md template
$SkillMd = @"
---
name: $SkillName
description: $Description
---

# $SkillName

## Overview

[Describe what this skill does and when to use it]

## Basic Usage

[Add your skill instructions here]

## Advanced Features

[Add advanced usage patterns]

## Examples

[Include practical examples]

## Resources

- Scripts: Check the `scripts/` directory
- References: See `references/` for detailed documentation
- Assets: Templates and resources in `assets/`
"@

$SkillMd | Out-File -FilePath "$SkillPath/SKILL.md" -Encoding UTF8

# Create example files
@"
# Example script for $SkillName
# Add your automation code here

def main():
    print("Hello from $SkillName skill!")

if __name__ == "__main__":
    main()
"@ | Out-File -FilePath "$SkillPath/scripts/example.py" -Encoding UTF8

@"
# $SkillName Reference Guide

## Overview
This document contains detailed information and examples for the $SkillName skill.

## Usage Patterns
[Add detailed usage instructions]

## Best Practices
[Add best practices and tips]
"@ | Out-File -FilePath "$SkillPath/references/guide.md" -Encoding UTF8

@"
# Example asset file for $SkillName
# This could be a template, configuration file, etc.
"@ | Out-File -FilePath "$SkillPath/assets/template.txt" -Encoding UTF8

Write-Host "✅ Skill structure created successfully!" -ForegroundColor Green
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Edit $SkillPath/SKILL.md with your skill instructions" -ForegroundColor White
Write-Host "2. Add your scripts to $SkillPath/scripts/" -ForegroundColor White
Write-Host "3. Add documentation to $SkillPath/references/" -ForegroundColor White
Write-Host "4. Add templates/assets to $SkillPath/assets/" -ForegroundColor White
Write-Host "5. Test your skill and iterate" -ForegroundColor White
Write-Host "6. Run: openskills sync --yes (in your project)" -ForegroundColor White
