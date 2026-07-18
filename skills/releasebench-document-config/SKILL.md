---
name: releasebench-document-config
description: >-
  Generates an IDE-friendly JSON Schema for a project's JSON config file, a matching
  dependency-free fail-fast validator, and a "Make it yours" README section — all describing the
  same fields so they never drift. Use when a JSON config needs editor autocomplete, startup
  validation, or fork-friendly customization docs. It does not fix unrelated loader bugs, invent
  requirements, add dependencies, prepare releases, or publish.
---

!`node "${CLAUDE_SKILL_DIR}/scripts/read-lessons.mjs" 2>/dev/null || cat "${CLAUDE_SKILL_DIR}/LESSONS.md" 2>/dev/null`

# Generating a config schema (+ validator + "Make it yours" docs)

A config file is the #1 fork-ability lever: it's the thing a new user edits first. This skill turns
a plain JSON config into a **self-documenting, validated, fork-friendly** contract by producing three
artifacts that describe the *same fields with the same wording* so they can't drift:

1. **`<config>.schema.json`** — a JSON Schema referenced via `$schema`, giving editors autocomplete,
   hover docs, and typo-catching. Lets you retire brittle inline `_comment` keys.
2. **A dependency-free fail-fast validator** — runs at startup, collects ALL problems, and prints
   plain-language errors before the program touches the network, state, or money.
3. **A "Make it yours" README section** — a short table of the 3–5 fields a user most needs to
   change, plus a safe (offline/dry-run) quickstart.

> Single source of truth: the schema `description`s, the validator messages, and the README table
> all describe the same fields. Write the wording once and reuse it verbatim across all three.

## When to use this

Trigger when the user wants any of: a JSON Schema for a config, config autocomplete/validation,
startup config checks, retiring `_comment`/`_note` keys, or making a config "fork-friendly" /
"self-documenting" / "easy to customize." Works for any language's project (the schema + README are
language-agnostic; the validator is emitted in the project's runtime).

## Procedure

### 1. Learn the REAL contract (don't guess from the file alone)
The config file shows the shape, but the code shows what's **required**, **typed**, and
**enumerated**. Before writing anything:
- Read the config file in full.
- Grep the codebase for how each top-level key is read (e.g. `config.engine`, `config["taxRate"]`,
  `cfg.watchlist`). A key read with `?? default` is optional; a key dereferenced bare is required.
- Note any value compared against a fixed set (`=== 'serpapi'`, `includes(policy)`) → that's an
  **enum**. Note numeric bounds implied by the code (percent, count, price floor).
- List every inline `_comment`/`_note`/`_*` key — these become schema `description`s and are then
  deleted from the config.

### 2. Pick the "Make it yours" fields
From the contract, choose the **3–5 fields a forker must change** to make the tool theirs (budget,
identity, the list of things tracked, where alerts go). These get the README table. Everything else
is still in the schema, just not headlined.

### 3. Write the schema
Use `templates/config.schema.template.json` as the starting point. Rules that make it good:
- `"$schema": "http://json-schema.org/draft-07/schema#"` (draft-07 is the most broadly supported by
  editors). Give it a `title` and a top-level `description`.
- **`"additionalProperties": false`** at the top level and inside each object/array-item — this is
  what catches typos (`budgetcap` vs `budgetCap`). Explicitly allow the `"$schema"` string property.
- `required: [...]` = only the keys the code truly needs (from step 1), not every key.
- Put a **`description` on every property** — this is the hover doc and the single source of truth.
  Reuse the exact text in the validator and README.
- Use `enum` for fixed sets, `format` (`email`, `uri`, `date`) where apt, and numeric
  `minimum`/`maximum`/`exclusiveMinimum` for bounds.

Then reference it from the config and retire the inline comments:
- Add `"$schema": "./<config>.schema.json"` as the **first** key (relative path resolves in VS Code).
- **Delete** the `_comment`/`_note` keys (confirm via grep that no code reads them first).

### 4. Write the dependency-free validator
Copy `templates/validate-config.template.mjs` (adapt to the project's language/runtime). Principles:
- **No new dependencies** — hand-rolled checks, not a schema-interpreter library. The schema file is
  for editors; this is the runtime guard.
- **Collect ALL errors and return them** (don't throw on the first) so the user fixes everything in
  one pass. Each message is plain language naming the field and what's expected.
- Validate the high-value things: money/identity fields, the enum(s), required arrays non-empty,
  each list item's required fields, **duplicate IDs/keys**, and cross-field sanity (min < max).
- **Fail fast**: call it right after parsing the config and BEFORE any network/state/spend; on
  errors, print them and exit non-zero. Mirror an existing path override (e.g. `STATE_PATH`) by
  adding a `CONFIG_PATH` env so an alternate config can be validated/tested.

### 5. Write the "Make it yours" README section
Use `templates/make-it-yours.template.md`. A 3–5 row field table (reusing the schema descriptions
verbatim) + an **offline-first / dry-run quickstart** (clone → edit the fields → run tests →
preview with no spend/sends → only then go live). Point readers at the config as the single source
of truth.

### 6. Verify (do not skip)
- The schema file is valid JSON; the config parses with the new `$schema` key and no `_comment` keys.
- The validator passes the **real** config (add a test asserting this — it guards against drift) and
  rejects a deliberately-broken config with readable errors (run it as a CLI to prove the wiring,
  exit code non-zero).
- Run the project's test suite; it stays green.

## Anti-patterns
- Don't make the validator a generic JSON-Schema engine or pull in a dependency — keep it tiny and
  hand-rolled.
- Don't let the three artifacts drift: if a field's meaning changes, update schema + validator +
  README together.
- Don't mark every key `required` — over-strict validation frustrates forkers. Required = what the
  code actually needs.
- Don't keep the inline `_comment` keys "just in case" once the schema documents them — that's the
  drift you're removing (but DO confirm no code reads them first).

## Security & altitude
Model-invocable (also chained by `releasebench-prepare-repository` step 3 — `disable-model-invocation`
would block that Skill-tool call); no `allowed-tools` — its writes (schema, validator, README
section, in-place config edits) go through the normal permission prompts.

## Improve this skill (feedback loop)
When the user corrects your output or states a reusable preference (a schema dialect, a field
convention, a tool to prefer), **propose a reviewable diff** appending one entry to `LESSONS.md`
(schema in that file) — never edit it silently. Record the smallest general rule; supersede stale
entries; keep it ≤100 lines. Promote a verified, high-confidence "rule was ignored" lesson into the
steps above with MUST language. Cross-project / how-Claude-works preferences go to Claude's memory
instead. `LESSONS.md` is injected at the top of this skill each run.

## Bundled files
- `templates/config.schema.template.json` — draft-07 schema skeleton with the patterns above.
- `templates/validate-config.template.mjs` — dependency-free, collect-all-errors validator (Node/ESM;
  adapt for other runtimes).
- `templates/make-it-yours.template.md` — the README section + quickstart.
