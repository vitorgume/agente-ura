from src.infrastructure.entity.conversa_entity import ConversaEntity
from src.infrastructure.mapper.mensagem_conversa_mapper import MensagemConversaMapper
from src.domain.conversa import Conversa


class ConversaMapper:
    
    def __init__(self, mensagem_conversa_mapper: MensagemConversaMapper):
        self.mensagem_conversa_mapper = mensagem_conversa_mapper
    
    def paraEntity(self, conversa: Conversa) -> ConversaEntity:
        conversaEntity = ConversaEntity(
            conversa.id,
            list(map(self.mensagem_conversa_mapper.paraEntity, conversa.mensagens)),
            conversa.cliente_id
        )
        return conversaEntity
    
    def paraDomain(self, conversa_entity: ConversaEntity) -> Conversa:
        conversa = Conversa(
            conversa_entity.id,
            list(map(self.mensagem_conversa_mapper.paraDomain, conversa_entity.mensagens)),
            conversa_entity.cliente_id
        )
        return conversa
