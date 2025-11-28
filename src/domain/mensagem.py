from dataclasses import dataclass
from typing import List

@dataclass
class Mensagem:
    cliente_id: str
    conversa_id: str
    message: str
    audios_url: List[str]
    imagens_url: List[str]
