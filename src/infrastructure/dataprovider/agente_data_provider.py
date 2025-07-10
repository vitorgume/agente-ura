from openai import OpenAI
from src.config.secrets import OPENAI_API_KEY
import logging

from src.infrastructure.exceptions.data_provider_exception import DataProviderException

logger = logging.getLogger(__name__)

client = OpenAI(api_key=OPENAI_API_KEY)


class AgenteDataProvider:

    mensagem_erro_enviar_mensagem_ia = "Erro ao enviar mensagem a IA."

    def enviar_mensagem(self, historico) -> str:
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=historico
            )
        except Exception as e:
            logger.exception(self.mensagem_erro_enviar_mensagem_ia)
            raise DataProviderException(self.mensagem_erro_enviar_mensagem_ia)

        return response.choices[0].message.content
