# app/api/routes.py

from fastapi import APIRouter, Request
from pydantic import BaseModel

from app.middleware.sanitization import sanitize_text
from app.core.intent_parser import parse_intent
from app.core.asset_resolver import resolve_assets
from app.core.scene_compiler import compile_scene

router = APIRouter(prefix="/ai")


class CommandRequest(BaseModel):
    text: str


@router.post("/command")
def ai_command(req: CommandRequest, request: Request):
    """
    Main AI entrypoint.
    """

    clean_text = sanitize_text(req.text)

    # IMPORTANT: parse_intent is SYNC
    intent = parse_intent(clean_text)

    assets = resolve_assets(
        intent=intent,
        asset_index=request.app.state.asset_index
    )

    scene = compile_scene(intent, assets)

    return {
        "status": "ok",
        "intent": intent,
        "assets": assets,
        "scene": scene
    }
