from pydantic import BaseModel

class AIRequest(BaseModel):
    text: str
