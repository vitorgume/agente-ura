from sqlalchemy import Column, String, Boolean, SmallInteger
from sqlalchemy.dialects.mysql import BINARY, TINYINT
from src.config.database import Base

class ClienteEntity(Base):
    __tablename__ = "clientes"

    id_cliente = Column(BINARY(16), primary_key=True, index=True)
    nome = Column(String(255), nullable=True)
    telefone = Column(String(255), nullable=True)
    inativo = Column(Boolean, nullable=False)
    regiao = Column(TINYINT(unsigned=True), nullable=True)
    segmento = Column(TINYINT(unsigned=True), nullable=True)
