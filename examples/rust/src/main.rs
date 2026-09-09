//! Golden Path Rust hello + About + crash sanitize.

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    std::process::exit(hello::log::run_stdio(&args));
}
