"""Wallpaper rolls: perimeter strips, pattern repeat on drop length, strips per roll."""

from app.engines.helpers import ceil_units, floor_units

DEFAULT_MATCH_PATTERN = True


def effective_pattern_m(pattern_cm: float, match_pattern: bool) -> float:
    """对花开关解析：开启时取卷材花高，关闭时忽略花高按无花口径。"""
    if not match_pattern:
        return 0.0
    return max(0.0, float(pattern_cm) / 100.0)


def resolve_match_pattern(requested, settings: dict) -> bool:
    """当次测算入参优先；缺省时回落到设置里的 match_pattern_default。"""
    if requested is not None:
        return bool(requested)
    raw = (settings or {}).get("match_pattern_default")
    if raw is None:
        return DEFAULT_MATCH_PATTERN
    return str(raw).strip().lower() in ("1", "true", "yes", "on")


def roll_count(
    perimeter: float,
    height: float,
    roll_width: float,
    roll_length: float,
    pattern_cm: float,
    match_pattern: bool = True,
) -> dict:
    if roll_width <= 0 or roll_length <= 0:
        raise ValueError("invalid roll size")
    drops = ceil_units(float(perimeter) / float(roll_width))
    pattern_m = effective_pattern_m(pattern_cm, match_pattern)
    drop_len = float(height) + pattern_m
    if drop_len <= 0:
        raise ValueError("invalid drop length")
    strips_per_roll = max(1, floor_units(float(roll_length) / drop_len))
    rolls = ceil_units(drops / strips_per_roll)
    return {
        "drops": drops,
        "drop_len_m": round(drop_len, 3),
        "pattern_m": round(pattern_m, 3),
        "match_pattern": bool(match_pattern),
        "strips_per_roll": strips_per_roll,
        "rolls": rolls,
    }
