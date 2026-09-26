from app.engines.wallpaper_math import roll_count


def test_plain_master_bed():
    r = roll_count(16.0, 2.7, 0.53, 10.0, 0)
    assert r["drops"] == 31
    assert r["drop_len_m"] == 2.7
    assert r["strips_per_roll"] == 3
    assert r["rolls"] == 11
    assert r["match_pattern"] is True


def test_pattern_wall():
    r = roll_count(20.0, 2.8, 0.53, 10.0, 64)
    assert r["drops"] == 38
    assert r["drop_len_m"] == 3.44
    assert r["strips_per_roll"] == 2
    assert r["rolls"] == 19
    assert r["match_pattern"] is True


def test_match_off_ignores_pattern():
    off = roll_count(20.0, 2.8, 0.53, 10.0, 64, match_pattern=False)
    plain = roll_count(20.0, 2.8, 0.53, 10.0, 0)
    # 关闭对花须与花高为 0 的改造前同参结果一致
    assert off == {**plain, "match_pattern": False}
    assert off["drop_len_m"] == 2.8
    assert off["pattern_m"] == 0.0
    assert off["strips_per_roll"] == 3
    assert off["rolls"] == 13


def test_match_on_explicit_keeps_pattern():
    r = roll_count(20.0, 2.8, 0.53, 10.0, 64, match_pattern=True)
    assert r["drop_len_m"] == 3.44
    assert r["pattern_m"] == 0.64
    assert r["rolls"] == 19
