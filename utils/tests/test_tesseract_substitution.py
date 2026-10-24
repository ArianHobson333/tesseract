# Copyright 2026 The Tesseract Authors
# You can use, redistribute, and/or modify this source code under
# the terms of the GPL-3.0 license that can be found in the LICENSE file.

import pytest

from ..tesseract_substitution import replace_text


@pytest.mark.parametrize("src,expected", [
    ("Helium", "Tesseract"),
    ("About Helium", "About Tesseract"),
    ("Helium Helium", "Tesseract Tesseract"),
    ("Helium's settings", "Tesseract's settings"),
])
def test_rewrites_product_name(src, expected):
    assert replace_text(src) == (expected, True)


@pytest.mark.parametrize("src", [
    "helium://settings",
    "https://services.helium.imput.net",
    "https://updates.helium.computer/mac/appcast-arm64.xml",
    "Copyright 2025 The Helium Authors",
    "github.com/imputnet/helium",
    "net.imput.helium",
    "Chrome Web Store",
    "Chrome Root Program",
    "HeliumBrowser",
    "Helium services",
    "Allow connecting to Helium Services",
])
def test_leaves_urls_credits_and_ids_alone(src):
    assert replace_text(src) == (src, False)


def test_mixed_line_rewrites_only_the_name():
    src = "Helium is built by The Helium Authors, see https://helium.computer"
    expected = "Tesseract is built by The Helium Authors, see https://helium.computer"
    assert replace_text(src) == (expected, True)
