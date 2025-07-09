from sqlalchemy import Column, String
from src.infrastructure.config.database import Base

class Conversa(Base):
    __tablename__ = "conversas_agente"

    id = Column(String(255), primary_key=True, index=True)
    responsavel = Column(String(255))
    conteudo = Column(String(2000))
    conversa_id = Column(String(255))
