from src.domain.mensagem import Mensagem


def test_mensagem_cliente_id_vindo_de_args():
    mensagem = Mensagem("ola", "conv-1", 123, None, None, "cliente-extra")

    assert mensagem.cliente_id == "cliente-extra"
    assert mensagem.audios_url == []
    assert mensagem.imagens_url == []


def test_mensagem_com_listas_definidas():
    audios = ["a.mp3"]
    imagens = ["img.png"]

    mensagem = Mensagem("hi", "conv-2", "cliente-123", audios_url=audios, imagens_url=imagens)

    assert mensagem.cliente_id == "cliente-123"
    assert mensagem.audios_url == audios
    assert mensagem.imagens_url == imagens


def test_mensagem_sem_cliente_id():
    mensagem = Mensagem("msg", "conv-3")

    assert mensagem.cliente_id == ""
    assert mensagem.audios_url == []
    assert mensagem.imagens_url == []
