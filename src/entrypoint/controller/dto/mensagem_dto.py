from pydantic import BaseModel, Field
from typing import List

class MensagemDto(BaseModel):
    cliente_id: str = Field(alias="cliente_id")
    conversa_id: str = Field(alias="conversa_id")
    message: str
    audios_url: List[str] = []
    imagens_url: List[str] = []


    class Config:
        populate_by_name = True