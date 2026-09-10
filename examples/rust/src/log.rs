//! JSON logs and readiness for the Rust Golden Path CLI.

use std::io::{self, Write};

pub fn ready_json() -> &'static str {
    "{\"status\":\"ok\"}"
}

pub fn log_json(level: &str, msg: &str) -> String {
    format!(
        "{{\"level\":{},\"msg\":{}}}",
        json_str(level),
        json_str(msg)
    )
}

fn json_str(value: &str) -> String {
    let escaped = value.replace('\\', "\\\\").replace('"', "\\\"");
    format!("\"{escaped}\"")
}

pub fn run(args: &[String], stdout: &mut impl Write, stderr: &mut impl Write) -> i32 {
    if args.iter().any(|a| a == "--ready") {
        let _ = writeln!(stderr, "{}", log_json("info", "ready"));
        let _ = writeln!(stdout, "{}", ready_json());
        return 0;
    }
    let _ = writeln!(stderr, "{}", log_json("info", "start"));
    let _ = writeln!(stdout, "{}", crate::greet());
    let _ = writeln!(stdout, "{}", crate::about::summary());
    0
}

pub fn run_stdio(args: &[String]) -> i32 {
    run(args, &mut io::stdout(), &mut io::stderr())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn ready_payload() {
        assert_eq!(ready_json(), "{\"status\":\"ok\"}");
    }

    #[test]
    fn ready_flag_writes_json() {
        let mut out = Vec::new();
        let mut err = Vec::new();
        assert_eq!(run(&["--ready".into()], &mut out, &mut err), 0);
        assert_eq!(String::from_utf8_lossy(&out).trim(), ready_json());
        let log = String::from_utf8_lossy(&err);
        assert!(log.contains("\"msg\":\"ready\""));
        assert!(log.contains("\"level\":\"info\""));
    }
}
