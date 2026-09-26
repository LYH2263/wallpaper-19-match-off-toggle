from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.repositories import settings_repo

router = APIRouter()

ALLOWED_KEYS = {"unit", "match_pattern_default"}


class SettingsUpdate(BaseModel):
    values: dict[str, str]


@router.get("/settings")
def settings():
    return settings_repo.get_all()


@router.put("/settings")
def update_settings(body: SettingsUpdate):
    unknown = sorted(set(body.values) - ALLOWED_KEYS)
    if unknown:
        raise HTTPException(400, f"unknown setting keys: {unknown}")
    mp = body.values.get("match_pattern_default")
    if mp is not None and mp not in ("0", "1"):
        raise HTTPException(422, "match_pattern_default must be '0' or '1'")
    return settings_repo.set_values(body.values)
