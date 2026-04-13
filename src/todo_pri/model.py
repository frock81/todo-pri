from pydantic import BaseModel, Field


class Score(BaseModel):
    value: int = Field(..., ge=0, le=5)
    urgency: int = Field(..., ge=0, le=5)
    ease: int = Field(..., ge=0, le=5)
