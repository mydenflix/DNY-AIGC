"""Release notification feed route."""

from __future__ import annotations

from dataclasses import asdict

from fastapi import APIRouter, Depends, Query, Request

from novelvideo.api.auth import get_api_user
from novelvideo.api.schemas import OkResponse
from novelvideo.ports import get_release_feed_port

router = APIRouter()


def normalize_locale(value: str | None) -> str:
    # Release notes ship id/zh/en. Product UI default is Indonesian.
    if not value:
        return "id"
    primary = value.split(",", 1)[0].split(";", 1)[0].split("-", 1)[0].strip().lower()
    if primary in {"id", "in"}:
        return "id"
    if primary == "zh":
        return "zh"
    if primary == "en":
        return "en"
    return "id"


@router.get("/release-notifications", response_model=OkResponse)
async def get_release_notifications(
    request: Request,
    locale: str | None = Query(default=None),
    _user: dict = Depends(get_api_user),
) -> OkResponse:
    resolved_locale = normalize_locale(locale or request.headers.get("accept-language"))
    feed = await get_release_feed_port().current(locale=resolved_locale)
    return OkResponse(data=asdict(feed))
