# Human Backlog

> Items automation attempted during autonomous `/build` but could not complete. BUILD_PLAN rows stay open until a human finishes them.

| Deferred | Sprint | Owner | Task | Reason |
|----------|--------|-------|------|--------|
| 2026-09-09 | Waiting on a person | ADB | Optional: Android SDK licenses + first AVD (/emulator) | Cloud agent has no ANDROID_HOME / USB; run `/emulator` on the machine with the phones |
| 2026-09-09 | Waiting on a person | ADB | Golden Path nav smoke on device (Settings Back → home; second Back stays) | Cloud agent has no adb; run on the host where the two devices are plugged in |

Declined 2026-09-10: optional Ollama on this template (maintainer). Recipe stays in `docs/LOCAL_MODELS.md` for child repos. Quarterly radar is Monday cron (`cursor-feature-radar.sh`), not a board row.
