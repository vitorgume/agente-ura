from src.domain.conversa import Conversa
from src.infrastructure.database import Database
from src.infrastructure.exceptions.data_provider_exception import DataProviderException

class ConversaDataProvider:
    
    def salvar(self, conversa: Conversa):
        session = SessionLocal()
        try:
            session.merge(conversa) 
            session.commit()
        except Exception as e:
            session.rollback()
            raise DataProviderException("Erro ao salvar conversa")
        finally:
            session.close()
    
    def consulta_por_id(self, id: str) -> Conversa:
        session = SessionLocal()
        try:
            return session.query(Conversa).filter(Conversa.id == id).first()
        except SQLAlchemyError as e:
            raise ErroDePersistencia("Erro ao consultar conversa")
        finally:
            session.close()