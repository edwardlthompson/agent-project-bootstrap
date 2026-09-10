"""Tests for hello.cli module."""

import json
import sys
from unittest.mock import patch

import pytest

from hello.cli import main


def test_main_prints_greeting(capsys: pytest.CaptureFixture[str]) -> None:
    with patch.object(sys, "argv", ["hello", "FOSS"]):
        main()
    assert "Hello, FOSS!" in capsys.readouterr().out


def test_main_default_greeting(capsys: pytest.CaptureFixture[str]) -> None:
    with patch.object(sys, "argv", ["hello"]):
        main()
    assert "Hello, world!" in capsys.readouterr().out


def test_main_invalid_name_exits(capsys: pytest.CaptureFixture[str]) -> None:
    with patch.object(sys, "argv", ["hello", "x" * 101]):
        with pytest.raises(SystemExit) as exc:
            main()
    assert exc.value.code == 1
    assert "Error:" in capsys.readouterr().err


def test_main_about(capsys: pytest.CaptureFixture[str]) -> None:
    with patch.object(sys, "argv", ["hello", "--about"]):
        main()
    out = capsys.readouterr().out
    assert "0.1.0" in out
    assert "donate" in out


def test_main_feedback(capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GITHUB_REPO", "acme/app")
    with patch.object(sys, "argv", ["hello", "--feedback", "--kind", "bug", "--title", "Crash"]):
        main()
    out, err = capsys.readouterr()
    body = json.loads(out)
    assert body["kind"] == "bug"
    assert "github.com/acme/app/issues/new" in body["url"]
    assert '"msg":"feedback"' in err


def test_main_ready(capsys: pytest.CaptureFixture[str]) -> None:
    with patch.object(sys, "argv", ["hello", "--ready"]):
        main()
    out, err = capsys.readouterr()
    assert json.loads(out) == {"status": "ok"}
    assert '"msg":"ready"' in err


def test_main_openapi(capsys: pytest.CaptureFixture[str]) -> None:
    with patch.object(sys, "argv", ["hello", "--openapi"]):
        main()
    spec = json.loads(capsys.readouterr().out)
    assert spec["openapi"].startswith("3.")
    assert "/health" in spec["paths"]
