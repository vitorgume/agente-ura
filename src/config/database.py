from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Ajuste os dados de acesso ao seu banco MySQL
DATABASE_URL = "mysql+pymysql://usuario:senha@localhost:3306/agente_ura"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
