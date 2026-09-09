# Golden Path Lightroom Plugin Stub

Minimal `.lrplugin` metadata stub for agent-project-bootstrap. Adobe Lightroom Classic is proprietary; this example documents structure and SDK compliance only — there is no headless build.

## SDK Version Compatibility

| Field | Value | Notes |
|-------|-------|-------|
| `LrSdkVersion` | **13.0** | Target SDK for development (Lightroom Classic 13.x) |
| `LrSdkMinimumVersion` | **6.0** | Minimum supported Lightroom Classic version |
Update these fields in `Info.lua` when you change target Lightroom versions. Record the chosen versions in `AGENT_MEMORY.md` per `modules/lightroom/MODULE.md`.

## Compliance (Module D)

- Use **only** Adobe Lightroom SDK `Lr*` namespaces (`LrTasks`, `LrDialogs`, `LrLogger`, `LrView`, etc.).
- Do **not** `require` generic Lua modules or call OS APIs outside SDK boundaries.
- One real export path: `LrExportServiceProvider` → `ExportServiceProvider.lua` `processRenderedPhotos` (uses `import "LrLogger"` + `exportContext.exportSession`).
- Second Lr* factory: `LrMetadataTagsetFactory` → `MetadataTagset.lua`.
- CI and feature-gate run `scripts/verify-lightroom.sh` plus `scripts/check-lightroom-lua.sh` (`.luacheckrc`).

## Local Load Test

1. Copy or symlink this folder as `YourPlugin.lrplugin`.
2. In Lightroom Classic: **File → Plug-in Manager → Add**.
3. Confirm the plugin appears and `LrLogger` output is visible when you add handlers.

## CI Integration

The **Lightroom SDK namespace check** job greps for non-`Lr*` imports and runs Lua lint. It does not execute Lightroom.

```bash
bash scripts/check-lightroom-lua.sh
```
