from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from src.config.database import Base

class MensagemConversaEntity(Base):
    __tablename__ = "mensagens_conversa"

    id = Column(String(255), primary_key=True)
    responsavel = Column(String(50), nullable=False)  # 'usuario' ou 'agente'
    conteudo = Column(String(2000), nullable=False)
    conversa_id = Column(String(255), ForeignKey("conversas_agente.id"), nullable=False)

    # Relacionamento reverso
    conversa = relationship("ConversaEntity", back_populates="mensagens")
