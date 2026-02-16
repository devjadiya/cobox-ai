from fastapi import FastAPI

app = FastAPI(title="Cobox AI")

@app.get("/")
def root():
    return {"status": "Cobox AI backend running"}

@app.get("/health")
def health():
    return {"ok": True}
