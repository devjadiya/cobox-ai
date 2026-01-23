# app/main.py

from fastapi import FastAPI
from app.api.routes import router
from app.core.asset_loader import load_asset_index

app = FastAPI(
    title="Cobox AI Command Service",
    version="0.2.0"
)


@app.on_event("startup")
def startup():
    app.state.asset_index = load_asset_index()


@app.get("/")
def health():
    return {
        "status": "ok",
        "assets_loaded": {
            k: len(v) for k, v in app.state.asset_index.items()
        }
    }


app.include_router(router)
