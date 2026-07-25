const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { buildCodeBlock, readConfig } = require('./build-code-block.js');

function makeTempProject() {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'build-code-block-test-'));
  fs.writeFileSync(path.join(dir, 'a.js'), 'const a = 1;');
  fs.writeFileSync(path.join(dir, 'b.js'), 'const b = 2;');
  const config = { files: ['a.js', 'b.js'], output: 'dist/out.js' };
  const configPath = path.join(dir, 'build.config.json');
  fs.writeFileSync(configPath, JSON.stringify(config));
  return { dir, configPath };
}

test('readConfig throws on missing files array', () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'build-code-block-test-'));
  const configPath = path.join(dir, 'build.config.json');
  fs.writeFileSync(configPath, JSON.stringify({ output: 'x.js' }));
  assert.throws(() => readConfig(configPath), /non-empty "files" array/);
});

test('readConfig throws on missing output', () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'build-code-block-test-'));
  const configPath = path.join(dir, 'build.config.json');
  fs.writeFileSync(configPath, JSON.stringify({ files: ['a.js'] }));
  assert.throws(() => readConfig(configPath), /must have an "output" string/);
});

test('buildCodeBlock throws when a source file is missing', () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'build-code-block-test-'));
  const configPath = path.join(dir, 'build.config.json');
  fs.writeFileSync(configPath, JSON.stringify({ files: ['missing.js'], output: 'out.js' }));
  assert.throws(() => buildCodeBlock(configPath), /Source file not found/);
});

test('buildCodeBlock concatenates files in order, wrapped in one IIFE', () => {
  const { dir, configPath } = makeTempProject();
  const outputPath = buildCodeBlock(configPath);
  const output = fs.readFileSync(outputPath, 'utf8');

  assert.match(output, /^\(function \(\) \{/);
  assert.match(output, /'use strict';/);
  assert.match(output, /\}\)\(\);\s*$/);

  const aIndex = output.indexOf('const a = 1;');
  const bIndex = output.indexOf('const b = 2;');
  assert.ok(aIndex > -1, 'a.js content missing from output');
  assert.ok(bIndex > -1, 'b.js content missing from output');
  assert.ok(aIndex < bIndex, 'files must appear in config order');

  assert.strictEqual(outputPath, path.join(dir, 'dist', 'out.js'));
});

test('buildCodeBlock produces syntactically valid JavaScript', () => {
  const { configPath } = makeTempProject();
  const outputPath = buildCodeBlock(configPath);
  const output = fs.readFileSync(outputPath, 'utf8');
  // Throws a SyntaxError if the generated IIFE is malformed.
  assert.doesNotThrow(() => new Function(output));
});
