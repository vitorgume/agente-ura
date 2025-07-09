from src.infrastructure.entity.mensagem_conversa_entity import MensagemConversaEntity
from src.domain.mensagem_conversa import MensagemConversa


class MensagemConversaMapper:
    
    def paraEntity(self, mensagem: MensagemConversa) -> MensagemConversaEntity:
        mensagemConversaEntity = MensagemConversaEntity(
            mensagem.id,
            mensagem.responsavel,
            mensagem.conteudo,
            mensagem.conversa_id
        )
        return mensagemConversaEntity
    
    def paraDomain(self, mensagemConversaEntity: MensagemConversaEntity) -> MensagemConversa:
        mensagemConversa = MensagemConversa(
            mensagemConversaEntity.id,
            mensagemConversaEntity.responsavel,
            mensagemConversaEntity.conteudo,
            mensagemConversaEntity.conversa_id
        )
        return mensagemConversa
