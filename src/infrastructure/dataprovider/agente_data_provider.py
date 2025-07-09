from src.domain.mensagem_conversa import MensagemConversa
from src.config.secrets import OPENAI_API_KEY
import openai

openai.api_key = OPENAI_API_KEY

class AgenteDataProvider:
    
    def enviar_mensagem(self, mensagem: str, mensagens: list[MensagemConversa]) -> str:
         # Constrói o histórico no formato da OpenAI
        historico = [
            {
                "role": "system",
                "content": "Você é um atendente virtual da URA, cordial, direto e prestativo. Sempre responda de forma clara, curta e objetiva. Caso não saiba algo, peça que a pessoa aguarde para ser redirecionada ao suporte humano."
            }
        ]

        # Adiciona o histórico da conversa
        for m in mensagens:
            role = "user" if m.responsavel == "usuario" else "assistant"
            historico.append({"role": role, "content": m.conteudo})

        # Adiciona a nova mensagem do usuário
        historico.append({"role": "user", "content": mensagem})

        # Chama o modelo
        response = openai.ChatCompletion.create(
            model="gpt-4",  # ou "gpt-3.5-turbo"
            messages=historico
        )

        # Retorna a resposta gerada
        return response["choices"][0]["message"]["content"]