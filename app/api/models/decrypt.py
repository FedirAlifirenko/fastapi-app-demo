from pydantic import BaseModel


class DecryptRequest(BaseModel):
    device_id: int
    content_id: int


class DecryptResponse(BaseModel):
    payload: str
