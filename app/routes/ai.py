from fastapi import APIRouter
from app.models.request import AIRequest
from app.services.scene_factory import create_scene_from_text

router = APIRouter()

@router.post("/ai/instant")
def instant(req: AIRequest):
    return create_scene_from_text(req.text)
