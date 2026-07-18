// validate-config.template.mjs — a tiny, DEPENDENCY-FREE, fail-fast config validator.
//
// This is NOT a JSON-Schema engine (the .schema.json file gives editors that). It catches the
// handful of mistakes that would otherwise cause silent bad behavior, and reports ALL of them at
// once in plain language so a forker fixes everything in one pass.
//
// Adapt the field checks to your config; keep the shape (helpers → collect errors → return list).

const isNum = (v) => typeof v === 'number' && Number.isFinite(v);
const isStr = (v) => typeof v === 'string' && v.trim().length > 0;
const isArr = (v) => Array.isArray(v);

// Fixed-choice fields become an explicit allow-list (mirror the schema's `enum`).
const PROVIDERS = ['<onlySupportedValue>'];

/**
 * Validate a parsed config object.
 * @returns {string[]} plain-language problems; empty array means valid.
 */
export function validateConfig(config) {
  if (config == null || typeof config !== 'object' || Array.isArray(config)) {
    return ['config must be a JSON object (the parsed contents of your config file).'];
  }
  const errors = [];
  const add = (m) => errors.push(m);

  // --- high-value scalar fields (money / identity / where things go) ---
  if (!isNum(config.numberField) || config.numberField <= 0) {
    add('numberField must be a positive number — <what it is and the unit>.');
  }
  if (!isStr(config.emailField) || !config.emailField.includes('@')) {
    add('emailField must be an email address — <where notifications go> (or set the <ENV_VAR> env var).');
  }

  // --- fixed-choice (enum) fields ---
  if (config.enumObject == null || typeof config.enumObject !== 'object') {
    add('enumObject must be an object with provider one of: ' + PROVIDERS.join(', ') + '.');
  } else if (!PROVIDERS.includes(config.enumObject.provider)) {
    add(`enumObject.provider must be one of ${PROVIDERS.join(', ')} (got ${JSON.stringify(config.enumObject.provider)}).`);
  }

  // --- the required list a forker edits ---
  if (!isArr(config.requiredArray) || config.requiredArray.length === 0) {
    add('requiredArray must be a non-empty array.');
  } else {
    const seen = new Set();
    config.requiredArray.forEach((item, i) => {
      const tag = isStr(item?.id) ? ` ("${item.id}")` : '';
      const where = `requiredArray[${i}]${tag}`;
      if (item == null || typeof item !== 'object' || Array.isArray(item)) {
        add(`${where} must be an object.`);
        return;
      }
      for (const f of ['id', 'itemRequiredField']) {
        if (!isStr(item[f])) add(`${where}.${f} is required and must be a non-empty string.`);
      }
      if (isStr(item.id)) {
        if (seen.has(item.id)) add(`${where}.id is duplicated — each id must be unique (it is a storage key).`);
        seen.add(item.id);
      }
      // numeric per-item fields:
      // if (!isNum(item.someNumber) || item.someNumber <= 0) add(`${where}.someNumber must be a positive number.`);
    });
  }

  // --- cross-field sanity (catch min/max inversions etc.) ---
  if (config.bounds != null) {
    const { min, max } = config.bounds;
    if (isNum(min) && isNum(max) && min >= max) add('bounds.min must be less than bounds.max.');
  }

  return errors;
}

export default validateConfig;

// ── Wire it in at startup (fail fast, BEFORE any network / state / spend) ──
//
//   import { validateConfig } from './lib/validate-config.mjs';
//   const configPath = process.env.CONFIG_PATH || join(repoRoot, '<path>', '<config>.json');
//   const config = JSON.parse(await readFile(configPath, 'utf8'));
//   const problems = validateConfig(config);
//   if (problems.length) {
//     console.error(`[app] ${configPath} is invalid — fix these and re-run:\n  - ${problems.join('\n  - ')}`);
//     process.exitCode = 1;
//     return;
//   }
//
// And add a test asserting the SHIPPED config passes — that guards against drift:
//   test('the real config is valid', async () => {
//     const c = JSON.parse(await readFile('<path>/<config>.json', 'utf8'));
//     assert.deepEqual(validateConfig(c), []);
//   });
