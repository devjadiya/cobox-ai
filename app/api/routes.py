# app/api/routes.py
from fastapi import APIRouter, Request
from pydantic import BaseModel

from app.middleware.sanitization import sanitize_text
from app.llm.deepseek_client import DeepSeekClient
from app.core.asset_resolver import resolve_assets
from app.core.scene_compiler import compile_scene
from fastapi import APIRouter
from pydantic import BaseModel
from app.core.hud import build_hud_state

router = APIRouter(prefix="/ai")

router = APIRouter()

class HUDRequest(BaseModel):
    segment: int
    coins: int

@router.post("/hud")
def get_hud_state(req: HUDRequest):
    return build_hud_state(
        segment_index=req.segment,
        coins_collected=req.coins
    )

class CommandRequest(BaseModel):
    text: str


@router.post("/command")
async def handle_command(req: CommandRequest, request: Request):
    text = sanitize_text(req.text)

    llm = DeepSeekClient()
    intent = await llm.parse_intent(text)

    assets = resolve_assets(intent, request.app.state.asset_index)
    scene = compile_scene(intent, assets)

    return {
        "intent": intent,
        "assets": assets,
        "scene": scene,
        "meta": {
            "version": "0.1.0",
            "warnings": []
        }
    }
