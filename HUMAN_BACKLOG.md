# Human Backlog

> Items automation attempted during autonomous `/build` but could not complete. BUILD_PLAN rows stay open until a human finishes them.

| Deferred | Sprint | Owner | Task | Reason |
|----------|--------|-------|------|--------|
| 2026-09-10 | Waiting on a person | ADB | Golden Path nav smoke on device (Settings Back → home; second Back stays) | AVD `goldenpath-api34` + android-34 image ready. Phone still fails Compose InputManager. Emulator blocked until reboot: WHPX (`HypervisorPlatform`) was Disabled and is now Enabled (RestartNeeded). After reboot: unplug phone or set `ANDROID_SERIAL=emulator-5554`, then `python3 scripts/agent-run.py run-android-emulator-local -- --keep-emulator`. |
Declined 2026-09-10: optional Ollama on this template (maintainer). Recipe stays in `docs/LOCAL_MODELS.md` for child repos. Quarterly radar is Monday cron (`cursor-feature-radar.sh`), not a board row.
