import os
import socket
import hashlib

from uuid import uuid4, UUID
from deposito_de_arquivo_com_replicacao.config import settings
from deposito_de_arquivo_com_replicacao import enums, protocolo


def check_port(port: int) -> bool:
    """
    Verifica se a porta está em uso.

    Args:
        port:

    Returns:

    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(('', port))
        s.close()
        return True
    except socket.error:
        s.close()
        return False


def generate_uuid():
    return str(uuid4())


def is_valid_uuid(uuid_to_test, version=4):
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test


def enviar_arquivo_por_socket(socket_destinatario, caminho_arquivo: str, tamanho_arquivo: int):
    """
    Envia um arquivo por socket.
    Args:
        socket_destinatario:
        caminho_arquivo: str
        tamanho_arquivo: int
    """
    tamanho_fatia = settings.get('geral.tamanho_buffer_arquivo')

    partes = int(tamanho_arquivo / tamanho_fatia)
    resto = tamanho_arquivo - (partes * tamanho_fatia)

    if resto > 0:
        partes += 1

    with open(caminho_arquivo, 'rb') as f:
        for i in range(partes):
            if i == partes - 1:
                parte = f.read(resto)
            else:
                parte = f.read(tamanho_fatia)
            socket_destinatario.send(parte)

    resultado = protocolo.ResultadoRecebimentoDeArquivo.desencapsular(
        socket_destinatario.recv(settings.get('geral.tamanho_buffer_padrao')).decode()
    )
    if resultado.resultado == enums.Retorno.OK.value:
        print('Arquivo enviado com sucesso')
        return True
    else:
        print('Erro ao enviar arquivo')
        return False


def receber_arquivo_por_socket(socket_origem, caminho_arquivo: str, hash_arquivo: str, tamanho_arquivo: int):
    """
    Recebe um arquivo por socket.
    Args:
        socket_origem:
        caminho_arquivo: str
        hash_arquivo: str
        tamanho_arquivo: int
    """

    tamanho_fatia = settings.get('geral.tamanho_buffer_arquivo')

    sha256_hash = hashlib.sha256()
    arquivo_bytes = open(caminho_arquivo, 'wb')
    partes = int(tamanho_arquivo / tamanho_fatia)
    resto = tamanho_arquivo - (partes * tamanho_fatia)

    if resto > 0:
        partes += 1

    for i in range(partes):
        if i == partes - 1:
            parte = socket_origem.recv(resto)
        else:
            parte = socket_origem.recv(tamanho_fatia)

        arquivo_bytes.write(parte)
        sha256_hash.update(parte)

    arquivo_bytes.close()

    if sha256_hash.hexdigest() == hash_arquivo:
        print('Arquivo recebido com sucesso!')
        socket_origem.send(
            protocolo.ResultadoRecebimentoDeArquivo(
                hash_arquivo=hash_arquivo,
                resultado=enums.Retorno.OK.value
            ).encapsular().encode()
        )
        return True
    else:
        socket_origem.send(
            protocolo.ResultadoRecebimentoDeArquivo(
                hash_arquivo=hash_arquivo,
                resultado=enums.Retorno.ERRO.value
            ).encapsular().encode()
        )
        print('Erro ao receber arquivo!')
        os.remove(caminho_arquivo)
        return False
