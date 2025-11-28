import logging
from pathlib import Path
from typing import Tuple, Union, List, Dict, Any

from src.domain.conversa import Conversa
from src.domain.mensagem import Mensagem
from src.infrastructure.dataprovider.agente_data_provider import AgenteDataProvider

logger = logging.getLogger(__name__)


class AgenteUseCase:

    def __init__(self, agente_data_provider: AgenteDataProvider):
        self.agente_data_provider = agente_data_provider

    def _carregar_prompt_padrao(self) -> str:
        caminho = Path("src/resources/system_prompt_agent_chat.txt")
        with open(caminho, "r", encoding="utf-8") as file:
            return file.read()

    def processar(self, mensagem: Mensagem, conversa: Conversa) -> Tuple[str, str]:
        logger.info("Processando mensagem para o agente. Mensagem: %s Conversa: %s", mensagem, conversa)

        historico = [
            {
                "role": "system",
                "content": self._carregar_prompt_padrao()
            }
        ]

        for m in conversa.mensagens:
            role = "user" if m.responsavel == "usuario" else "assistant"
            historico.append({"role": role, "content": m.conteudo})

        conteudo_usuario, conteudo_historico = self._preparar_conteudo_usuario(mensagem)
        historico.append({"role": "user", "content": conteudo_usuario})

        resposta = self.agente_data_provider.enviar_mensagem(historico)

        logger.info("Mensagem processada pelo agente com sucesso. Resposta: %s", resposta)

        return resposta, conteudo_historico

    def _preparar_conteudo_usuario(self, mensagem: Mensagem) -> Tuple[Union[str, List[Dict[str, Any]]], str]:
        texto_base = mensagem.message or ""

        transcricoes = []
        for indice, audio_url in enumerate(mensagem.audios_url, start=1):
            transcricao = self.agente_data_provider.transcrever_audio(audio_url)
            transcricoes.append(f"[Audio {indice}] {transcricao}")

        if transcricoes:
            bloco = "\n\n".join(transcricoes)
            if texto_base.strip():
                texto_base = f"{texto_base}\n\nTranscricoes de audio:\n{bloco}"
            else:
                texto_base = f"Transcricoes de audio:\n{bloco}"

        imagens_data_uri = []
        for imagem_url in mensagem.imagens_url:
            imagens_data_uri.append(self.agente_data_provider.baixar_imagem_como_data_uri(imagem_url))

        conteudo_historico = texto_base
        if imagens_data_uri:
            complemento = f"[{len(imagens_data_uri)} imagem(ns) anexada(s)]"
            conteudo_historico = f"{texto_base}\n\n{complemento}" if texto_base else complemento

        if imagens_data_uri:
            conteudo_modelo: Union[str, List[Dict[str, Any]]] = []
            texto_para_modelo = texto_base.strip() or "Analise as imagens enviadas e responda ao usuario."
            conteudo_modelo.append({"type": "text", "text": texto_para_modelo})
            for data_uri in imagens_data_uri:
                conteudo_modelo.append({"type": "image_url", "image_url": {"url": data_uri}})
        else:
            conteudo_modelo = texto_base or "Responda ao usuario."

        if not conteudo_historico:
            conteudo_historico = conteudo_modelo if isinstance(conteudo_modelo, str) else "Midia enviada pelo usuario."

        return conteudo_modelo, conteudo_historico
