from pydantic import BaseModel

class StartChatResponse(BaseModel):
    lead_id: int


class ChatMessageRequest(BaseModel):
    lead_id: int
    message: str


class ChatMessageResponse(BaseModel):
    reply: str
    intent: str
    sentiment: str
    score: int
    status: str
