#!/usr/bin/env node
// audit-repo.mjs — read-only OSS-readiness audit. Reports which governance / fork-ability files are
// present vs missing, by severity, and points at the deeper sibling skills. No writes, no network.
// Exits 1 if any MUST-HAVE is missing (so it's CI-usable).
import { existsSync, readFileSync, readdirSync } from 'node:fs';
import { join, resolve } from 'node:path';

const repo = resolve(process.argv[2] || '.');
const miss = []; // {sev, item, fix}
const present = [];
const add = (sev, item, fix) => miss.push({ sev, item, fix });
const has = (p) => existsSync(join(repo, p));
const firstOf = (...ps) => ps.find(has);

// --- MUST-HAVE ---
const license = firstOf('LICENSE', 'LICENSE.md', 'LICENSE.txt');
if (!license) {
  add('MUST', 'LICENSE', 'add a license (e.g. MIT) — with none, the repo is "all rights reserved"');
} else {
  const txt = readFileSync(join(repo, license), 'utf8');
  // No \b anchors: '[' '<' '{' are non-word chars, so word boundaries never match before them.
  const placeholder = /(YOUR NAME|FULLNAME|\[(?:year|name|fullname|your name|email)\]|<(?:year|name|copyright holders?)>|\{\{[A-Za-z_]+\}\})/i;
  const realCopyright = /copyright \(c\)\s+\d{4}\s+\S+/i;
  if (placeholder.test(txt)) add('MUST', 'LICENSE copyright', 'LICENSE still has a placeholder name/year');
  else if (!realCopyright.test(txt)) add('MUST', 'LICENSE copyright', 'LICENSE has no clear "Copyright (c) <year> <holder>" line');
  else present.push('LICENSE');
}
firstOf('README.md', 'README', 'README.rst') ? present.push('README') : add('MUST', 'README', 'add a README');

// --- RECOMMENDED governance files ---
for (const [p, item, why] of [
  ['CONTRIBUTING.md', 'CONTRIBUTING', 'how to contribute + the project guardrails'],
  ['SECURITY.md', 'SECURITY', 'how to report vulnerabilities privately'],
  ['CODE_OF_CONDUCT.md', 'CODE_OF_CONDUCT', 'community standards'],
  ['CHANGELOG.md', 'CHANGELOG', 'notable changes'],
  ['.gitignore', '.gitignore', 'ignore build artifacts and secret files'],
]) (has(p) ? present.push(item) : add('RECOMMENDED', item, `add ${item} — ${why}`));

// --- .github/ ---
const wfDir = join(repo, '.github', 'workflows');
const hasWorkflows = existsSync(wfDir) && readdirSync(wfDir).some((f) => /\.ya?ml$/.test(f));
(has('.github/ISSUE_TEMPLATE') || has('.github/ISSUE_TEMPLATE.md')) ? present.push('issue templates') : add('RECOMMENDED', 'issue templates', 'add .github/ISSUE_TEMPLATE/');
(has('.github/PULL_REQUEST_TEMPLATE.md') || has('.github/pull_request_template.md')) ? present.push('PR template') : add('RECOMMENDED', 'PR template', 'add .github/PULL_REQUEST_TEMPLATE.md');
hasWorkflows ? present.push('CI workflow') : add('RECOMMENDED', 'CI', 'add a .github/workflows CI (e.g. run tests on push/PR)');

// --- node-specific ---
if (has('package.json')) {
  try {
    const pkg = JSON.parse(readFileSync(join(repo, 'package.json'), 'utf8'));
    pkg.license ? present.push('package.json license') : add('RECOMMENDED', 'package.json "license"', 'add a "license" field');
  } catch { /* malformed package.json — not this script's job */ }
}
if (has('.env.example') || has('.env.sample')) present.push('.env.example');

// --- pointers to deeper sibling skills ---
add('INFO', 'secrets scan', 'run releasebench-scan-secrets for committed-secret risks');
add('INFO', 'config schema', 'if there is a JSON config, run releasebench-document-config for a schema + validator + Make-it-yours');

// --- report ---
const order = { MUST: 0, RECOMMENDED: 1, INFO: 2 };
miss.sort((a, b) => order[a.sev] - order[b.sev]);
console.log(`[audit-repo] ${repo}`);
console.log(`present: ${present.length ? present.join(', ') : '(none)'}\n`);
for (const m of miss) console.log(`  [${m.sev}] ${m.item} — ${m.fix}`);
const mustMissing = miss.filter((m) => m.sev === 'MUST').length;
const recMissing = miss.filter((m) => m.sev === 'RECOMMENDED').length;
console.log(`\nsummary: ${mustMissing} must-have missing, ${recMissing} recommended missing, ${present.length} present.`);
if (mustMissing) console.log('Run releasebench-scaffold-governance to generate the missing files.');
process.exitCode = mustMissing ? 1 : 0;
