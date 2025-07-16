from sqlalchemy import Column, String, DateTime, Boolean, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import BINARY
from src.config.database import Base
from src.infrastructure.entity.mensagem_conversa_entity import MensagemConversaEntity
from src.infrastructure.entity.vendedor_entity import VendedorEntity
from src.infrastructure.entity.cliente_entity import ClienteEntity

class ConversaEntity(Base):
    __tablename__ = "conversas_agente"

    id_conversa = Column(BINARY(16), primary_key=True, index=True)
    data_criacao = Column(DateTime(timezone=True), nullable=True)
    finalizada = Column(Boolean, default=False)
    inativa = Column(Boolean, default=False)
    cliente_id_cliente = Column(BINARY(16), ForeignKey("clientes.id_cliente"), nullable=True)
    vendedor_id_vendedor = Column(BigInteger, ForeignKey("vendedores.id_vendedor"), nullable=True)

    mensagens = relationship("MensagemConversaEntity", back_populates="conversa", cascade="all, delete-orphan")
