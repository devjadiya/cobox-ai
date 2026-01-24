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

    print("\n=== AI COMMAND RECEIVED ===")
    print("Raw text:", req.text)

    clean_text = sanitize_text(req.text)
    print("Sanitized text:", clean_text)

    # IMPORTANT: parse_intent is SYNC
    intent = parse_intent(clean_text)
    print("Parsed intent:", intent)

    assets = resolve_assets(
        intent=intent,
        asset_index=request.app.state.asset_index
    )
    print(f"Resolved {len(assets)} assets")
    for asset in assets:
        print(" - Asset:", asset.get("id"), "| category:", asset.get("category"))

    scene = compile_scene(intent, assets)
    print("Scene compiled:", scene["scene_id"])
    print(f"Actors in scene: {len(scene.get('actors', []))}")

    print("=== AI COMMAND COMPLETE ===\n")

    return {
        "status": "ok",
        "intent": intent,
        "assets": assets,
        "scene": scene
    }
