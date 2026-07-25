#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');

const REPO_ROOT = path.resolve(__dirname, '..');
const TARGET_ROOT = path.join(process.cwd(), '.claude', 'skills');
const IGNORED_DIRS = new Set(['.git', 'bin', 'node_modules']);

function copyRecursive(src, dest) {
  fs.mkdirSync(dest, { recursive: true });
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);
    if (entry.isDirectory()) {
      copyRecursive(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

function findSkills() {
  const categories = fs.readdirSync(REPO_ROOT, { withFileTypes: true })
    .filter((entry) => entry.isDirectory() && !entry.name.startsWith('.') && !IGNORED_DIRS.has(entry.name))
    .map((entry) => entry.name);

  const skills = [];
  for (const category of categories) {
    const categoryPath = path.join(REPO_ROOT, category);
    for (const entry of fs.readdirSync(categoryPath, { withFileTypes: true })) {
      if (!entry.isDirectory()) continue;
      const skillPath = path.join(categoryPath, entry.name);
      if (fs.existsSync(path.join(skillPath, 'SKILL.md'))) {
        skills.push({ category, name: entry.name, path: skillPath });
      }
    }
  }
  return skills;
}

function main() {
  const requested = process.argv.slice(2);
  const all = findSkills();

  if (!all.length) {
    console.error('No skills found in this repository.');
    process.exit(1);
  }

  const selected = requested.length
    ? all.filter((s) => requested.includes(s.name) || requested.includes(s.category))
    : all;

  if (!selected.length) {
    console.error(`No matching skills for: ${requested.join(', ')}`);
    console.error(`Available: ${all.map((s) => `${s.category}/${s.name}`).join(', ')}`);
    process.exit(1);
  }

  fs.mkdirSync(TARGET_ROOT, { recursive: true });

  console.log(`Installing into ${path.relative(process.cwd(), TARGET_ROOT) || '.'}${path.sep}\n`);
  for (const skill of selected) {
    copyRecursive(skill.path, path.join(TARGET_ROOT, skill.name));
    console.log(`  + ${skill.category}/${skill.name}`);
  }

  console.log(`\nInstalled ${selected.length} skill(s). Re-run this command any time to pull the latest version.`);
}

main();
