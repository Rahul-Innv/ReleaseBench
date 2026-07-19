#!/usr/bin/env node
// scan-secrets.mjs — read-only secret-hygiene scan of a git repo. Dependency-free, no network.
//
//   node scan-secrets.mjs [repo-dir]
//
// Checks: (1) git-tracked sensitive files, (2) .gitignore coverage, (3) hardcoded secrets in
// tracked text files. Prints findings by severity; exits 1 if any CRITICAL/HIGH (so it's CI-usable).
// It never writes, deletes, or sends anything — it only reports. Deep git-HISTORY scanning is out of
// scope (use trufflehog/gitleaks for that).
import { readFileSync, existsSync, statSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { join, resolve } from 'node:path';

const repo = resolve(process.argv[2] || '.');
const findings = [];
const add = (severity, what, file, line, detail) => findings.push({ severity, what, file, line, detail });

// --- tracked files via git (read-only) ---
let tracked = [];
try {
  tracked = execFileSync('git', ['-C', repo, 'ls-files'], { encoding: 'utf8', maxBuffer: 64 * 1024 * 1024 })
    .split('\n').map((s) => s.trim()).filter(Boolean);
} catch {
  console.error(`[scan-secrets] ${repo} is not a git repository (or git is unavailable) — cannot list tracked files.`);
  process.exit(2);
}

// --- (1) tracked sensitive files ---
const SENSITIVE = [
  { re: /(^|\/)\.env(\.|$)/i, ok: /\.env\.(example|sample|template|dist)$/i, sev: 'CRITICAL', what: 'tracked .env file (should be gitignored)' },
  { re: /\.(pem|key|p12|pfx|keystore|jks)$/i, sev: 'CRITICAL', what: 'tracked private key / certificate' },
  { re: /(^|\/)id_(rsa|dsa|ecdsa|ed25519)$/i, sev: 'CRITICAL', what: 'tracked SSH private key' },
  { re: /(^|\/)\.npmrc$/i, sev: 'HIGH', what: 'tracked .npmrc (often holds an _auth token)' },
  { re: /(^|\/)(credentials|\.netrc|\.pgpass|service-account.*\.json)$/i, sev: 'HIGH', what: 'tracked credentials file' },
];
for (const f of tracked) {
  for (const r of SENSITIVE) if (r.re.test(f) && !(r.ok && r.ok.test(f))) add(r.sev, r.what, f, null, '');
}

// --- (2) .gitignore coverage ---
const giPath = join(repo, '.gitignore');
if (!existsSync(giPath)) {
  add('MEDIUM', 'no .gitignore', '.gitignore', null, 'add one ignoring .env, .env.*, *.pem, *.key');
} else {
  const lines = readFileSync(giPath, 'utf8').split('\n').map((s) => s.trim()).filter((l) => l && !l.startsWith('#'));
  const has = (...alts) => alts.some((a) => lines.includes(a));
  const want = [
    { pat: '.env', covered: () => has('.env', '.env*', '/.env'), sev: 'MEDIUM' },
    { pat: '.env.* (.local/.backup)', covered: () => has('.env.*', '.env*'), sev: 'MEDIUM' },
    { pat: '*.pem', covered: () => has('*.pem'), sev: 'MEDIUM' },
    { pat: '*.key', covered: () => has('*.key'), sev: 'MEDIUM' },
  ];
  for (const w of want) if (!w.covered()) add(w.sev, '.gitignore missing pattern', '.gitignore', null, `add "${w.pat}"`);
}

// --- (3) hardcoded secrets in tracked text files ---
const SKIP_EXT = /\.(png|jpe?g|gif|webp|ico|pdf|zip|gz|tgz|tar|jar|exe|dll|so|dylib|woff2?|ttf|eot|mp[34]|mov|lock)$/i;
const SKIP_PATH = /(^|\/)(node_modules|\.git|dist|build|vendor|coverage)\/|(^|\/)(package-lock\.json|pnpm-lock\.yaml|npm-shrinkwrap\.json)$/;
const placeholder = /^(your[a-z0-9_-]*|example|sample|changeme|placeholder|dummy|test|none|null|true|false|xxx+|<.*>|\$\{?[a-z0-9_]+\}?|\*+|\.+|\u2026\d+\+\s*chars\u2026|\.\.\.\d+\+\s*chars\.\.\.)$/i;
const PATTERNS = [
  { re: /-----BEGIN (?:[A-Z0-9 ]+ )?PRIVATE KEY-----/, sev: 'CRITICAL', what: 'private key block' },
  { re: /\bAKIA[0-9A-Z]{16}\b/, sev: 'CRITICAL', what: 'AWS access key id' },
  { re: /\bsk_live_[0-9A-Za-z]{20,}\b/, sev: 'CRITICAL', what: 'Stripe live secret key' },
  { re: /\bghp_[A-Za-z0-9]{36}\b/, sev: 'HIGH', what: 'GitHub personal access token' },
  { re: /\bgithub_pat_[A-Za-z0-9_]{30,}\b/, sev: 'HIGH', what: 'GitHub fine-grained PAT' },
  { re: /\bxox[baprs]-[A-Za-z0-9-]{10,}\b/, sev: 'HIGH', what: 'Slack token' },
  { re: /\bAIza[0-9A-Za-z_\-]{35}\b/, sev: 'HIGH', what: 'Google API key' },
  { re: /\b(?:api[_-]?key|secret|token|password|passwd|client[_-]?secret|access[_-]?token)["']?\s*[:=]\s*["']([^"']{8,})["']/i, sev: 'MEDIUM', what: 'hardcoded secret-like assignment', grp: 1 },
];
const redact = (s) => (s.length <= 8 ? s[0] + '***' : s.slice(0, 3) + '***' + s.slice(-2));

for (const f of tracked) {
  if (SKIP_EXT.test(f) || SKIP_PATH.test(f)) continue;
  const abs = join(repo, f);
  let text;
  try {
    if (statSync(abs).size > 1024 * 1024) continue; // skip >1MB
    text = readFileSync(abs, 'utf8');
  } catch { continue; }
  if (text.includes('\0')) continue; // skip binary (NUL byte)
  const rows = text.split('\n');
  for (let i = 0; i < rows.length; i++) {
    for (const p of PATTERNS) {
      const m = rows[i].match(p.re);
      if (!m) continue;
      const val = p.grp ? m[p.grp] : m[0];
      if (p.grp && (placeholder.test(val) || /^(.)\1+$/.test(val))) continue; // skip obvious placeholders
      add(p.sev, p.what, f, i + 1, redact(val));
    }
  }
}

// --- report ---
const order = { CRITICAL: 0, HIGH: 1, MEDIUM: 2 };
findings.sort((a, b) => order[a.severity] - order[b.severity]);
const counts = findings.reduce((m, x) => ((m[x.severity] = (m[x.severity] || 0) + 1), m), {});
console.log(`[scan-secrets] ${repo}`);
console.log(`tracked files scanned: ${tracked.length}\n`);
if (!findings.length) {
  console.log('No secret-hygiene issues found. (History not scanned — use trufflehog/gitleaks for deep history.)');
  process.exit(0);
}
for (const x of findings) {
  const loc = x.line ? `${x.file}:${x.line}` : x.file;
  console.log(`  [${x.severity}] ${x.what} — ${loc}${x.detail ? `  (${x.detail})` : ''}`);
}
console.log(`\nsummary: ${Object.entries(counts).map(([k, v]) => `${v} ${k}`).join(', ')}`);
console.log('Fixes: add missing .gitignore patterns; for any committed secret, ROTATE it first (assume compromised), then remove from the tree AND purge from git history (git filter-repo / BFG) — never just delete in a new commit.');
process.exitCode = (counts.CRITICAL || counts.HIGH) ? 1 : 0;
