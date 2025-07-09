from dataclasses import dataclass


@dataclass
class MensagemAgente:
    user_id: str
    conversa_id: str
    message: str