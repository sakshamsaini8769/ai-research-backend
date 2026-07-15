from pydantic import BaseModel


class ResearchRequest(BaseModel):
    topic: str


class ModifyRequest(BaseModel):
    report: str
    instruction: str


class VoiceRequest(BaseModel):
    prompt: str