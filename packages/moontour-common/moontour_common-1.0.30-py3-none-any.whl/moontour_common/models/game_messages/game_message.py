from pydantic import BaseModel, validator


class GameMessage(BaseModel):
    room_id: str
    type: str = None

    @validator("type", always=True)
    def compute_type(cls, _):
        return cls.__name__
