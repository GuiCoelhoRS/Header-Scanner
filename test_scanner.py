from scanner import (
    analyze_x_content_type_options,
    analyze_x_frame_options,
    analyze_referrer_policy,
)


# ===== Tests for analyze_x_content_type_options =====

def test_xcto_valid_lowercase():
    grade, _ = analyze_x_content_type_options("nosniff")
    assert grade == "A"

def test_xcto_valid_uppercase():
    grade, _ = analyze_x_content_type_options("NOSNIFF")
    assert grade == "A"

def test_xcto_valid_with_whitespace():
    grade, _ = analyze_x_content_type_options("  nosniff  ")
    assert grade == "A"

def test_xcto_invalid():
    grade, _ = analyze_x_content_type_options("lol")
    assert grade == "F"

def test_xcto_empty():
    grade, _ = analyze_x_content_type_options("")
    assert grade == "F"


# ===== Tests for analyze_x_frame_options =====

def test_xfo_deny():
    grade, _ = analyze_x_frame_options("DENY")
    assert grade == "A"

def test_xfo_sameorigin():
    grade, _ = analyze_x_frame_options("SAMEORIGIN")
    assert grade == "B"

def test_xfo_allow_from():
    grade, _ = analyze_x_frame_options("ALLOW-FROM https://example.com")
    assert grade == "C"

def test_xfo_duplicated():
    grade, _ = analyze_x_frame_options("SAMEORIGIN, SAMEORIGIN")
    assert grade == "F"

def test_xfo_invalid():
    grade, _ = analyze_x_frame_options("lol")
    assert grade == "F"


# ===== Tests for analyze_referrer_policy =====

def test_rp_no_referrer():
    grade, _ = analyze_referrer_policy("no-referrer")
    assert grade == "A+"

def test_rp_strong_privacy():
    grade, _ = analyze_referrer_policy("strict-origin-when-cross-origin")
    assert grade == "A"

def test_rp_origin():
    grade, _ = analyze_referrer_policy("origin")
    assert grade == "B"

def test_rp_origin_when_cross():
    grade, _ = analyze_referrer_policy("origin-when-cross-origin")
    assert grade == "C"

def test_rp_unsafe_url():
    grade, _ = analyze_referrer_policy("unsafe-url")
    assert grade == "F"

def test_rp_fallback_uses_first_value():
    grade, _ = analyze_referrer_policy("origin-when-cross-origin, strict-origin-when-cross-origin")
    assert grade == "C" 

def test_rp_invalid():
    grade, _ = analyze_referrer_policy("LOL")
    assert grade == "F"