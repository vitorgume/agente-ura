from unittest.mock import Mock

import pytest

from src.application.usecase.agente_use_case import AgenteUseCase
from src.domain.conversa import Conversa
from src.domain.mensagem import Mensagem
from src.infrastructure.dataprovider.agente_data_provider import AgenteDataProvider


@pytest.fixture
def provider_mock():
    return Mock(spec=AgenteDataProvider)

@pytest.fixture
def use_case(provider_mock):
    return AgenteUseCase(agente_data_provider=provider_mock)

class FakeMensagem:
    def __init__(self, responsavel, conteudo):
        self.responsavel = responsavel
        self.conteudo = conteudo

def test_carregar_prompt_padrao(tmp_path, monkeypatch, provider_mock):
    texto = "PROMPT DEFAULT"
    prompt_file = tmp_path / "system_prompt_agent_chat.txt"
    prompt_file.write_text(texto, encoding="utf-8")

    monkeypatch.setattr(
        "src.application.usecase.agente_use_case.Path",
        lambda *args, **kwargs: prompt_file
    )

    uc = AgenteUseCase(provider_mock)
    resultado = uc._carregar_prompt_padrao()
    assert resultado == texto

def test_carregar_prompt_padrao_file_not_found(use_case, monkeypatch):
    monkeypatch.setattr(
        "builtins.open",
        lambda *args, **kwargs: (_ for _ in ()).throw(FileNotFoundError())
    )
    with pytest.raises(FileNotFoundError):
        use_case._carregar_prompt_padrao()

def test_processar_sem_historico(monkeypatch, provider_mock, use_case):
    monkeypatch.setattr(use_case, "_carregar_prompt_padrao", lambda: "PROMPT")
    conversa = Mock(spec=Conversa)
    conversa.mensagens = []
    provider_mock.enviar_mensagem.return_value = "RESPOSTA_OK"

    retorno = use_case.processar("Olá, tudo bem?", conversa)

    assert retorno == "RESPOSTA_OK"
    provider_mock.enviar_mensagem.assert_called_once_with([
        {"role": "system",    "content": "PROMPT"},
        {"role": "user",      "content": "Olá, tudo bem?"},
    ])

def test_processar_com_historico(monkeypatch, provider_mock, use_case):
    monkeypatch.setattr(use_case, "_carregar_prompt_padrao", lambda: "PROMPT")
    m1 = FakeMensagem("usuario", "Oi")
    m2 = FakeMensagem("bot",     "Tudo certo")
    conversa = Mock(spec=Conversa)
    conversa.mensagens = [m1, m2]
    provider_mock.enviar_mensagem.return_value = "RESPOSTA_FINAL"

    retorno = use_case.processar("Como posso ajudar?", conversa)

    esperado = [
        {"role": "system",    "content": "PROMPT"},
        {"role": "user",      "content": "Oi"},
        {"role": "assistant", "content": "Tudo certo"},
        {"role": "user",      "content": "Como posso ajudar?"},
    ]
    provider_mock.enviar_mensagem.assert_called_once_with(esperado)
    assert retorno == "RESPOSTA_FINAL"

def test_processar_provedor_exception(monkeypatch, provider_mock, use_case):
    monkeypatch.setattr(use_case, "_carregar_prompt_padrao", lambda: "PROMPT")
    conversa = Mock(spec=Conversa)
    conversa.mensagens = []

    provider_mock.enviar_mensagem.side_effect = RuntimeError("falha no provider")
    with pytest.raises(RuntimeError) as exc:
        use_case.processar("Teste de exceção", conversa)
    assert "falha no provider" in str(exc.value)


def test_processar_com_objeto_mensagem(monkeypatch, provider_mock, use_case):
    monkeypatch.setattr(use_case, "_carregar_prompt_padrao", lambda: "PROMPT")
    monkeypatch.setattr(use_case, "_preparar_conteudo_usuario", lambda msg: (["conteudo-estruturado"], "historico"))

    conversa = Mock(spec=Conversa)
    conversa.mensagens = []
    provider_mock.enviar_mensagem.return_value = "RETORNO"

    mensagem = Mensagem(message="oi", conversa_id="conv-id")
    retorno = use_case.processar(mensagem, conversa)

    assert retorno == "RETORNO"
    provider_mock.enviar_mensagem.assert_called_once_with([
        {"role": "system", "content": "PROMPT"},
        {"role": "user", "content": ["conteudo-estruturado"]},
    ])


def test_preparar_conteudo_usuario_com_midias(provider_mock, use_case):
    provider_mock.transcrever_audio.side_effect = ["texto audio"]
    provider_mock.baixar_imagem_como_data_uri.side_effect = ["data:image/png;base64,AAA"]

    mensagem = Mensagem(
        message="Ola",
        conversa_id="c1",
        audios_url=["http://audio/1.mp3", "  ", None],
        imagens_url=["http://img/1.png", ""],
    )

    conteudo_modelo, conteudo_historico = use_case._preparar_conteudo_usuario(mensagem)

    provider_mock.transcrever_audio.assert_called_once_with("http://audio/1.mp3")
    provider_mock.baixar_imagem_como_data_uri.assert_called_once_with("http://img/1.png")

    assert isinstance(conteudo_modelo, list)
    assert conteudo_modelo[0]["type"] == "text"
    assert "texto audio" in conteudo_modelo[0]["text"]
    assert conteudo_modelo[1]["image_url"]["url"] == "data:image/png;base64,AAA"
    assert "[1 imagem(ns) anexada(s)]" in conteudo_historico
    assert "Transcricoes de audio" in conteudo_historico


def test_preparar_conteudo_usuario_sem_conteudo(provider_mock, use_case):
    mensagem = Mensagem(message="", conversa_id="c2")

    conteudo_modelo, conteudo_historico = use_case._preparar_conteudo_usuario(mensagem)

    provider_mock.transcrever_audio.assert_not_called()
    provider_mock.baixar_imagem_como_data_uri.assert_not_called()
    assert conteudo_modelo == "Responda ao usuario."
    assert conteudo_historico == "Responda ao usuario."
