# app/main.py
from fastapi import FastAPI
from app.api.routes import router
from app.core.asset_loader import load_assets

app = FastAPI(title="Cobox AI Command Service")

@app.on_event("startup")
def startup():
    app.state.asset_index = load_assets()

app.include_router(router)
