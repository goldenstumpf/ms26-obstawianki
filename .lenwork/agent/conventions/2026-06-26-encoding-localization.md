# Encoding-localization Conventions

**Updated:** 2026-06-26 10:49 UTC

## Encoding/Localization

- Keep `app/utils/components.py` saved as UTF-8 to preserve emoji literals (🔴/🟡/⚫, 🏆, ✔, ✏️). If emojis appear as '??' or imports fail with UTF-8 errors, check for accidental cp1250/other encoding saves and re-encode to UTF-8.
