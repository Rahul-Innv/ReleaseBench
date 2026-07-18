<!-- Drop this near the TOP of the README (it's the #1 fork-ability lever). Reuse the field
descriptions VERBATIM from the JSON Schema so the docs/schema/validator never drift. -->

## Make it yours

This project is built to be **forked**. Point it at *your* <things> by editing one file —
`<path>/<config>.json`, the single source of truth — then preview everything **offline** before
spending a cent or sending anything.

**The fields you'll usually change:**

| Field | Type | What it means |
|---|---|---|
| `<fieldA>` | <type> | <Reuse the schema description verbatim.> |
| `<fieldB>` | <type> | <Reuse the schema description verbatim.> |
| `<fieldC>` | <type> | <Reuse the schema description verbatim.> |
| `<requiredArray>[]` | array | <What each entry tracks; list its required + optional sub-fields.> |

**Offline-first quickstart (zero spend, nothing sent):**

1. Clone, then create your env file (keys are *not* needed for the offline preview):
   `git clone <repo-url> && cd <repo>` then copy `.env.example` to `.env`.
2. Edit the fields above in `<path>/<config>.json`.
3. Run the tests — they're offline and spend nothing: `<test command>`.
4. Preview the whole pipeline offline (writes to a scratch dir, sends nothing):
   `<dry-run / mock command>`.
5. Only once you're happy: add your secrets and go live — see **[<deploy section>](#deploy)**.

The rest of `<path>/<config>.json` is documented inline by `<config>.schema.json` (hover any field
in an editor); the contributor guardrails are in **[CONTRIBUTING.md](CONTRIBUTING.md)**.
