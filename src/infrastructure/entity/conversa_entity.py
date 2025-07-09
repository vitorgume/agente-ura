from sqlalchemy import Column, String
from src.config.database import Base
from sqlalchemy.orm import relationship

class ConversaEntity(Base):
    __tablename__ = "conversas_agente"

    id = Column(String(255), primary_key=True, index=True)
    cliente_id = Column(String(255), nullable=False)

    # Relacionamento com mensagens
    mensagens = relationship("MensagemConversaEntity", back_populates="conversa", cascade="all, delete-orphan")
