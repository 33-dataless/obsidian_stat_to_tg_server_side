from pydantic import BaseModel, Field
from data.event import Event

class Payload(BaseModel):
    event: Event
    snapshot: dict[str, int] = Field(default_factory=dict)
