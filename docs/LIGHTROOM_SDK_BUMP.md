# Lightroom SDK bump playbook

> Keep `Info.lua` and the README version table in lockstep. Do not bump on rumor.

## Current versions

The Golden Path stub targets Lightroom Classic **13.x**. Values live in `examples/lightroom/Info.lua` and must match the table in `examples/lightroom/README.md`.

| Field | Role |
|-------|------|
| `LrSdkVersion` | SDK you develop against (Adobe's current Classic SDK) |
| `LrSdkMinimumVersion` | Oldest Classic you still claim to load |
**Pin + checksum (FOSS stub only):** this repo does **not** vendor Adobe SDK headers. Pin is the `LrSdkVersion` / `LrSdkMinimumVersion` pair in `Info.lua`. Integrity check: `sha256sum examples/lightroom/Info.lua` must match the value recorded in `examples/lightroom/SDK_PIN.sha256` (updated only when the HUMAN-approved SDK bump edits `Info.lua`).

## When to bump

- Adobe ships a **new Classic major** and documents SDK N+1.
- An `Lr*` API you use is **removed** or replaced in the new SDK.
- You are **dropping** an old Classic major (`LrSdkMinimumVersion` only).

Do not bump because a beta build exists, or because CI is bored. `[HUMAN]` confirms the plugin still loads in Plug-in Manager after the edit.

## Steps

1. Read Adobe's Lightroom Classic SDK release notes for removed `Lr*` symbols.
2. Edit `LrSdkVersion` / `LrSdkMinimumVersion` in `examples/lightroom/Info.lua`.
3. Update the README compatibility table to the same numbers (bold the target SDK).
4. Run `bash scripts/check-lightroom-sdk-playbook.sh` and `bash scripts/check-lightroom-lua.sh`.
5. `[HUMAN]` File → Plug-in Manager → Add (or Reload) and exercise export + the metadata tagset.
6. Note the new pair in `AGENT_MEMORY.md` on child repos (this template already documents 13.0 / 6.0).

`scripts/check-lightroom-sdk-playbook.sh` fails when the README table drifts from `Info.lua`.

## HUMAN load test

Lightroom Classic has no headless runner. After every SDK bump:

1. Copy `examples/lightroom` to `GoldenPath.lrplugin`.
2. Reload the plugin.
3. Export one JPEG through Golden Path Export.
4. Confirm the Golden Path tagset appears in the Library metadata panel.

## Do not

- Raise `LrSdkMinimumVersion` without a written reason (you silently drop older Classic).
- Add generic `require()` while "just testing" the new SDK.
- Commit Adobe SDK headers or sample plugins (proprietary).
