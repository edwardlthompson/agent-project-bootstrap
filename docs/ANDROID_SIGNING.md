# Android signing and rollback

> Upload keys stay **outside git**. This template never ships a keystore.

## Upload keystore

Create one upload keystore on a machine you control (`keytool -genkeypair`). Store the `.jks` / `.keystore` / `.p12` file outside the repo (password manager or encrypted disk). **Never commit** those files — `.gitignore` already lists `*.jks`, `*.keystore`, and `*.p12`.

Play App Signing (optional commercial store) keeps the *app signing* key on Google's side. You keep only the **upload** key. F-Droid rebuilds from source and signs with the F-Droid key; your upload key is not required there.

## Environment variables

Copy `.env.example` → `.env` (gitignored). For a local signed release:

| Variable | Role |
|----------|------|
| `GOLDENPATH_UPLOAD_STORE_FILE` | Absolute path to the upload keystore |
| `GOLDENPATH_UPLOAD_STORE_PASSWORD` | Keystore password |
| `GOLDENPATH_UPLOAD_KEY_ALIAS` | Key alias (default `upload` in Gradle) |
| `GOLDENPATH_UPLOAD_KEY_PASSWORD` | Key password |

`examples/android/app/build.gradle.kts` applies the `upload` signing config only when `GOLDENPATH_UPLOAD_STORE_FILE` is set. Empty or missing → release stays debug-signed (CI hash compare).

## Local signed release

```bash
export SOURCE_DATE_EPOCH=1700000000
export GOLDENPATH_UPLOAD_STORE_FILE="$HOME/keys/goldenpath-upload.jks"
# plus the three password/alias variables
cd examples/android && ./gradlew assembleRelease
```

Confirm `app/build/outputs/apk/release/` is signed (`apksigner verify`). Keep that version's `mapping.txt` with the GitHub Release.

## Continuous integration

`android-release` in `.github/workflows/ci.yml` must **not** receive store passwords. It assembles twice with `SOURCE_DATE_EPOCH=1700000000` and compares APK hashes. Production signing happens on a human-held keystore or a protected GitHub Environment — never on the default `GITHUB_TOKEN` job.

## F-Droid and Play

| Channel | Who signs | Rollback |
|---------|-----------|----------|
| GitHub Releases | Your upload (or debug for CI proofs) | Re-attach the previous tag's APK / AAB |
| F-Droid | F-Droid builders | Previous suggested version in the recipe |
| Play (optional) | Play App Signing after upload | Play Console → prior release; keep the same upload key |

## Rollback

1. Identify the last known-good tag (GitHub Release).
2. Re-publish that APK/AAB (do not rebuild if the key or epoch changed).
3. If users already installed a bad build, ship a **higher** `versionCode` that reverts the code, signed with the **same** upload key.
4. Retrace crashes with that version's `mapping.txt` (`app/build/outputs/mapping/release/mapping.txt`).
5. Log user-impacting incidents in `DECISION_LOG.md`.

Losing the upload key **cannot** be fixed by generating a new one for the same Play listing. Rotate only via `docs/RUNBOOK.md` Secret Rotation after a leak; then enroll a new upload key in Play Console.

## Mapping files

Archive `mapping.txt` next to each signed artifact. R8 obfuscation makes unmapped Play/F-Droid stacks useless. Do not commit mappings that embed secrets; they are build outputs (`*.apk` is already gitignored).
