from enum import Enum


class Comando(Enum):
    """
    Enum com os comandos que podem ser enviados para o servidor.
    """
    DEPOSITAR_ARQUIVO = 'd'
    RECUPERAR_ARQUIVO = 'r'
    ENCERRAR_CONEXAO = 's'
    REGISTRAR_MIRROR = 'm'
    ALTERAR_REPLICAS = 'a'
    LISTAR_ARQUIVOS = 'l'

class Retorno(Enum):
    """
    Enum com os retornos que podem ser enviados para o cliente.
    """
    OK = '1'
    ERRO = '0'
