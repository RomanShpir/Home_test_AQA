# test_scripts/regression/ui_tests/conftest.py
from __future__ import annotations

import datetime as dt
from pathlib import Path

import pytest
from pytest_html import extras


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    """Hook to take a screenshot on test failure and attach it to the pytest-html report."""
    outcome = yield
    rep = outcome.get_result()

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

    # take a screenshot and save the file
    png_bytes = driver.get_screenshot_as_png()
    filepath.write_bytes(png_bytes)

    # attach to pytest-html (self-contained-html inlines the image)
    extra = getattr(rep, "extra", [])
    extra.append(extras.image(png_bytes, mime_type="image/png"))
    rep.extra = extra
