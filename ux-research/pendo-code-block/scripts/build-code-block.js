#!/usr/bin/env node
/**
 * Concatenates an ordered list of source files into one IIFE-wrapped output
 * file, per SKILL.md fact 2 (inline everything into one IIFE; Pendo does
 * not guarantee a separately `<script src>`-loaded file finishes before
 * the JS tab runs).
 *
 * Usage:
 *   node build-code-block.js --config path/to/build.config.json
 *
 * Config shape:
 *   {
 *     "files": ["src/data.js", "src/payload.js", "src/ui.js"],
 *     "output": "dist/code-block.js"
 *   }
 *
 * Paths in "files" and "output" are resolved relative to the config file's
 * own directory, not the current working directory.
 */
const fs = require('fs');
const path = require('path');

function readConfig(configPath) {
  const raw = fs.readFileSync(configPath, 'utf8');
  const config = JSON.parse(raw);
  if (!Array.isArray(config.files) || config.files.length === 0) {
    throw new Error('build.config.json must have a non-empty "files" array');
  }
  if (!config.output || typeof config.output !== 'string') {
    throw new Error('build.config.json must have an "output" string');
  }
  return config;
}

function buildCodeBlock(configPath) {
  const configDir = path.dirname(path.resolve(configPath));
  const config = readConfig(configPath);

  const pieces = config.files.map((relFile) => {
    const filePath = path.join(configDir, relFile);
    if (!fs.existsSync(filePath)) {
      throw new Error(`Source file not found: ${filePath}`);
    }
    return fs.readFileSync(filePath, 'utf8').trimEnd();
  });

  const body = pieces.join('\n\n');
  const wrapped = `(function () {\n'use strict';\n\n${body}\n})();\n`;

  const outputPath = path.join(configDir, config.output);
  fs.mkdirSync(path.dirname(outputPath), { recursive: true });
  fs.writeFileSync(outputPath, wrapped, 'utf8');

  return outputPath;
}

if (require.main === module) {
  const args = process.argv.slice(2);
  const configFlagIndex = args.indexOf('--config');
  if (configFlagIndex === -1 || !args[configFlagIndex + 1]) {
    console.error('Usage: node build-code-block.js --config path/to/build.config.json');
    process.exit(1);
  }
  const configPath = args[configFlagIndex + 1];
  try {
    const outputPath = buildCodeBlock(configPath);
    console.log(`Built ${outputPath}`);
  } catch (err) {
    console.error(`Build failed: ${err.message}`);
    process.exit(1);
  }
}

module.exports = { buildCodeBlock, readConfig };
