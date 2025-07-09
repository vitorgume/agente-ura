from pydantic import BaseModel

class MensagemDto(BaseModel):
    user_id: str
    conversa_id: str
    message: str