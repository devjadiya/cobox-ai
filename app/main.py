# app/main.py

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any
import logging

from app.core.asset_loader import load_asset_index
from app.core.intent_parser import parse_intent
from app.core.asset_resolver import resolve_assets
from app.core.scene_compiler import compile_scene

from app.schemas.scene import CommandResponse

# --------------------------------------------------
# Logging
# --------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("cobox-ai")

# --------------------------------------------------
# App
# --------------------------------------------------
app = FastAPI(
    title="Cobox AI Command Service",
    version="0.2.0",
    description="AI → Scene → Unreal pipeline"
)

# --------------------------------------------------
# Models
# --------------------------------------------------
class CommandRequest(BaseModel):
    text: str


# --------------------------------------------------
# Startup
# --------------------------------------------------
ASSET_INDEX: Dict[str, Any] = {}


@app.on_event("startup")
def startup():
    global ASSET_INDEX
    ASSET_INDEX = load_asset_index()
    logger.info("[startup] Assets loaded: %s",
        {k: len(v) for k, v in ASSET_INDEX.items()}
    )


# --------------------------------------------------
# Health
# --------------------------------------------------
@app.get("/")
def health():
    return {"status": "ok"}


# --------------------------------------------------
# AI Command Endpoint
# --------------------------------------------------
@app.post("/ai/command", response_model=CommandResponse)
def ai_command(req: CommandRequest):
    logger.info("\n=== AI COMMAND RECEIVED ===")
    logger.info("Raw text: %s", req.text)

    # 1️⃣ Parse intent
    intent = parse_intent(req.text)
    logger.info("Parsed intent: %s", intent)

    # 2️⃣ Resolve assets
    assets = resolve_assets(intent, ASSET_INDEX)
    logger.info("Resolved %d assets", len(assets))
    for a in assets:
        logger.info(" - Asset: %s | category: %s", a["id"], a["category"])

    # 3️⃣ Compile scene
    scene = compile_scene(intent, assets)
    logger.info("Scene compiled: %s", scene["scene_id"])
    logger.info("Actors in scene: %d", len(scene["actors"]))

    logger.info("=== AI COMMAND COMPLETE ===\n")

    # 4️⃣ Response
    return {
        "status": "ok",
        "intent": intent,
        "assets": assets,
        "scene": scene
    }
