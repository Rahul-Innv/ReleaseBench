import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { mkdtempSync, mkdirSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import test from 'node:test';
import { fileURLToPath } from 'node:url';

import { isDocumentedPlaceholder } from '../../skills/releasebench-scan-secrets/scripts/secret-placeholders.mjs';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..', '..');
const AUDIT = join(ROOT, 'skills', 'releasebench-audit-repository', 'scripts', 'audit-repo.mjs');

test('repository audit accepts GitHub and GitLab native files', () => {
  for (const host of ['github', 'gitlab']) {
    const fixture = mkdtempSync(join(tmpdir(), `releasebench-${host}-`));
    try {
      writeFileSync(join(fixture, 'LICENSE'), 'MIT License\n\nCopyright (c) 2026 Example Maintainer\n');
      for (const name of [
        'README.md', 'CONTRIBUTING.md', 'SECURITY.md', 'CODE_OF_CONDUCT.md',
        'CHANGELOG.md', '.gitignore',
      ]) {
        writeFileSync(join(fixture, name), 'fixture\n');
      }
      if (host === 'github') {
        mkdirSync(join(fixture, '.github', 'ISSUE_TEMPLATE'), { recursive: true });
        writeFileSync(join(fixture, '.github', 'PULL_REQUEST_TEMPLATE.md'), 'fixture\n');
        mkdirSync(join(fixture, '.github', 'workflows'), { recursive: true });
        writeFileSync(join(fixture, '.github', 'workflows', 'ci.yml'), 'fixture\n');
      } else {
        mkdirSync(join(fixture, '.gitlab', 'issue_templates'), { recursive: true });
        mkdirSync(join(fixture, '.gitlab', 'merge_request_templates'), { recursive: true });
        writeFileSync(join(fixture, '.gitlab-ci.yml'), 'fixture\n');
      }

      const completed = spawnSync(process.execPath, [AUDIT, fixture], { encoding: 'utf8' });
      assert.equal(completed.status, 0, completed.stderr);
      assert.match(completed.stdout, /summary: 0 must-have missing, 0 recommended missing/);
      assert.doesNotMatch(completed.stdout, /\[RECOMMENDED\] (issue templates|PR\/MR template|CI)/);
    } finally {
      rmSync(fixture, { recursive: true, force: true });
    }
  }
});

test('scanner distinguishes documented length placeholders from assignments', () => {
  assert.equal(isDocumentedPlaceholder('\u20268+ chars\u2026'), true);
  assert.equal(isDocumentedPlaceholder('...8+ chars...'), true);
  assert.equal(isDocumentedPlaceholder('alphaBETA42'), false);
});
