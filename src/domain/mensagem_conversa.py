
from dataclasses import dataclass


@dataclass
class MensagemConversa:    
    id: str
    responsavel: str
    conteudo: str
    conversa_id: str