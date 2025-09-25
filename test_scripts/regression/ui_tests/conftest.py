# test_scripts/regression/ui_tests/conftest.py
from __future__ import annotations

import base64
import datetime as dt
from pathlib import Path

import pytest
from pytest_html import extras


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    """Capture screenshot on test failure and attach to an HTML report."""
    outcome = yield
    rep = outcome.get_result()

    # only on failure during test execution (when == 'call')
    if rep.when != "call" or not rep.failed:
        return

    ui = item.funcargs.get("ui")
    driver = getattr(ui, "driver", None) if ui else None
    if driver is None:
        return

    screenshots_dir = Path("artifacts") / "screenshots"
    screenshots_dir.mkdir(parents=True, exist_ok=True)

    ts = dt.datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    filename = f"{item.name}-{ts}.png"
    filepath = screenshots_dir / filename

    png_bytes = driver.get_screenshot_as_png()
    filepath.write_bytes(png_bytes)

    png_b64 = base64.b64encode(png_bytes).decode("ascii")
    extra = getattr(rep, "extra", [])
    extra.append(extras.image(png_b64, mime_type="image/png"))
    rep.extra = extra
