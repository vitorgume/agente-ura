from openai import OpenAI
from src.config.secrets import OPENAI_API_KEY
import logging
import json

from src.domain.mensagem_agente import MensagemAgente
from src.domain.qualificacao_agente import QualificacaoAgente
from src.infrastructure.exceptions.data_provider_exception import DataProviderException

logger = logging.getLogger(__name__)

client = OpenAI(api_key=OPENAI_API_KEY)


class AgenteDataProvider:

    mensagem_erro_enviar_mensagem_ia = "Erro ao enviar mensagem a IA."

    def enviar_mensagem(self, historico) -> MensagemAgente:
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=historico,
                temperature = 0
            )
            content = response.choices[0].message.content
            logger.info("Resposta bruta da IA: %s", content)

            if not content or content.strip() == "":
                logger.error("Resposta vazia da IA.")
                raise DataProviderException("Resposta da IA vazia.")

            try:
                data = json.loads(content)
            except json.JSONDecodeError as e:
                logger.error("Erro de JSON: %s", content)
                raise DataProviderException("Resposta da IA não é um JSON válido.")

            qualificacao = QualificacaoAgente(
                qualificado=data["qualificacao"]["qualificado"],
                nome=data["qualificacao"]["nome"],
                segmento=data["qualificacao"]["segmento"],
                regiao=data["qualificacao"]["regiao"],
                descricao_material=data["qualificacao"]["descricao_material"]
            )

            return MensagemAgente(resposta=data["resposta"], qualificacao=qualificacao)

        except Exception as e:
            logger.exception("Erro ao enviar mensagem à IA: %s", e)
            raise DataProviderException(self.mensagem_erro_enviar_mensagem_ia)
