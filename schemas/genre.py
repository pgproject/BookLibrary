from pydantic import BaseModel
from pydantic import ConfigDict

class GenreCreate(BaseModel):
    name: str

class GenreResponses(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)