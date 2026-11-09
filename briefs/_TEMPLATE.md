---
brief: example-brief
kind: feature
scope: tag:web
touch: ["src/**", "app/**"]
expect_files: "2-4"
verify: "test -f README.md"
verify_timeout_s: 120
reversible: true
auto: false
---

Describe the change in plain English and what done looks like.
