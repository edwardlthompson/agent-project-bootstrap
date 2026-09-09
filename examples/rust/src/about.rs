//! CLI About slice: version + donate URL + update stub.

pub const APP_VERSION: &str = env!("CARGO_PKG_VERSION");
pub const DONATE_URL: &str = "https://github.com/sponsors";

pub fn summary() -> String {
    format!("golden-path {APP_VERSION} donate {DONATE_URL}")
}

/// Shared About/donate/update JSON (no serde — keep the stub dependency-free).
pub fn payload_json() -> String {
    format!(
        "{{\"version\":\"{APP_VERSION}\",\"donate\":\"{DONATE_URL}\",\"summary\":\"{}\",\"update\":{{\"status\":\"current\",\"version\":null,\"url\":null}}}}",
        summary()
    )
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn includes_version_and_donate() {
        let text = summary();
        assert!(text.contains(APP_VERSION));
        assert!(text.contains("donate"));
    }

    #[test]
    fn payload_json_matches_shared_contract() {
        let raw = payload_json();
        assert!(raw.contains(format!("\"version\":\"{APP_VERSION}\"").as_str()));
        assert!(raw.contains("\"status\":\"current\""));
        assert!(raw.contains("\"url\":null"));
        assert!(raw.contains(DONATE_URL));
    }
}
