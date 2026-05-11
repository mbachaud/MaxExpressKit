---
description: STUB — wraps the BookKeeper CLI when installed. Full integration is a v0.2.0 deliverable.
argument-hint: "[--check]"
---

# /mek-books $ARGUMENTS

v0.1.0 behavior (stub):

1. Call `lib.source_app_detect.has_bookkeeper()`.
2. If absent: print `[mek-books] BookKeeper CLI not detected. This command lights up when 'bookkeeper' is on PATH. See docs/source-app-integration.md.`
3. If present: print `[mek-books] detected BookKeeper at <path>. Full integration ships in v0.2.0.`
4. Always exit 0.
