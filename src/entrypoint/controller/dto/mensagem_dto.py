from pydantic import BaseModel

class MensagemDto(BaseModel):
    cliente_id: str
    conversa_id: str
    message: str