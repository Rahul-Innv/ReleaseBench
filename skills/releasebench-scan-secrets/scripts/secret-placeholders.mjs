// Shared, dependency-free placeholder classification for the scanner and its Node regressions.
const DOCUMENTED_PLACEHOLDER = /^(your[a-z0-9_-]*|example|sample|changeme|placeholder|dummy|test|none|null|true|false|xxx+|<.*>|\$\{?[a-z0-9_]+\}?|\*+|\.+|\u2026\d+\+\s*chars\u2026|\.\.\.\d+\+\s*chars\.\.\.)$/i;

export function isDocumentedPlaceholder(value) {
  return DOCUMENTED_PLACEHOLDER.test(value);
}
