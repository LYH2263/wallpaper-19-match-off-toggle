from app.engines.wallpaper_math import resolve_match_pattern, roll_count

def test_short_wall():
    assert roll_count(4.0, 2.5, 0.53, 10.0, 0)["rolls"] >= 1


def test_resolve_requested_wins_over_settings():
    assert resolve_match_pattern(False, {"match_pattern_default": "1"}) is False
    assert resolve_match_pattern(True, {"match_pattern_default": "0"}) is True


def test_resolve_falls_back_to_settings_default():
    assert resolve_match_pattern(None, {"match_pattern_default": "0"}) is False
    assert resolve_match_pattern(None, {"match_pattern_default": "1"}) is True


def test_resolve_default_when_setting_missing():
    assert resolve_match_pattern(None, {}) is True
    assert resolve_match_pattern(None, None) is True
