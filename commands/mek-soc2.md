---
description: STUB — wraps the CosmicTasha API when running. Full integration is a v0.2.0 deliverable.
argument-hint: "[--check]"
---

# /mek-soc2 $ARGUMENTS

v0.1.0 behavior (stub):

1. Call `lib.source_app_detect.has_cosmictasha()`.
2. If absent: print `[mek-soc2] CosmicTasha API not detected at http://localhost:3000/api/health. This command lights up when CT is running. See docs/source-app-integration.md.`
3. If present: print `[mek-soc2] detected CosmicTasha at <url>` (+ version if available). `Full integration ships in v0.2.0.`
4. Always exit 0.
