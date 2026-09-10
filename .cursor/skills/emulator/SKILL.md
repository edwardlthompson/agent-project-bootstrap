---
name: emulator
description: Run the local AOSP emulator and instrumented tests. Use when /emulator or Android device smoke.
disable-model-invocation: false
---

# Local Android emulator

See also: `.cursor/commands/emulator.md`, `modules/android/MODULE.md`

```bash
python3 scripts/agent-run.py run-android-emulator-local
python3 scripts/agent-run.py run-android-emulator-local -- --if-device
```

Missing SDK, hypervisor, or licenses → SKIP exit 0. Do not `git push`. Do not `adb reboot` or wipe a device this script did not start. First image download needs `[ADB]` `sdkmanager --licenses`. Force skip: `ANDROID_EMULATOR_LOCAL=0`.
