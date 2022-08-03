from re import match
from abc import abstractmethod


class Protocolo:

    pattern = None

    @abstractmethod
    def encapsular(self):
        pass

    @staticmethod
    @abstractmethod
    def desencapsular(mensagem: str):
        pass


class ClienteSolicitacaoDepositarArquivo(Protocolo):

    pattern = '^id_cliente:(.*)\|qtd_replicas:(\d+)\|tamanho_arquivo:(\d+)\|hash_arquivo:(.*)\|nome_arquivo:(.*)$'

    def __init__(self, id_cliente, qtd_replicas, tamanho_arquivo, hash_arquivo, nome_arquivo):
        self.id_cliente = id_cliente
        self.qtd_replicas = qtd_replicas
        self.tamanho_arquivo = tamanho_arquivo
        self.hash_arquivo = hash_arquivo
        self.nome_arquivo = nome_arquivo

    def encapsular(self):
        return "id_cliente:{}|qtd_replicas:{}|tamanho_arquivo:{}|hash_arquivo:{}|nome_arquivo:{}".format(
            self.id_cliente, self.qtd_replicas, self.tamanho_arquivo, self.hash_arquivo, self.nome_arquivo
        )

    @staticmethod
    def desencapsular(mensagem):
        id_cliente, qtd_replicas, tamanho_arquivo, hash_arquivo, nome_arquivo = match(
            ClienteSolicitacaoDepositarArquivo.pattern,
            mensagem
        ).groups()
        return ClienteSolicitacaoDepositarArquivo(
            id_cliente=id_cliente,
            qtd_replicas=qtd_replicas,
            tamanho_arquivo=tamanho_arquivo,
            hash_arquivo=hash_arquivo,
            nome_arquivo=nome_arquivo
        )


class ClienteSolicitacaoRecuperarArquivo(Protocolo):

    pattern = '^id_cliente:(.*)\|nome_arquivo:(.*)$'

    def __init__(self, id_cliente, nome_arquivo):
        self.id_cliente = id_cliente
        self.nome_arquivo = nome_arquivo

    def encapsular(self):
        return "id_cliente:{}|nome_arquivo:{}".format(
            self.id_cliente, self.nome_arquivo
        )

    @staticmethod
    def desencapsular(mensagem):
        id_cliente, nome_arquivo = match(
            ClienteSolicitacaoRecuperarArquivo.pattern,
            mensagem
        ).groups()
        return ClienteSolicitacaoRecuperarArquivo(
            id_cliente=id_cliente,
            nome_arquivo=nome_arquivo
        )


class ServidorSolicitaEnvioArquivoRecuperadoParaCliente(Protocolo):

    pattern = '^tamanho_arquivo:(\d+)\|hash_arquivo:(.*)$'

    def __init__(self, tamanho_arquivo, hash_arquivo):
        self.tamanho_arquivo = tamanho_arquivo
        self.hash_arquivo = hash_arquivo

    def encapsular(self):
        return "tamanho_arquivo:{}|hash_arquivo:{}".format(
            self.tamanho_arquivo, self.hash_arquivo
        )

    @staticmethod
    def desencapsular(mensagem):
        tamanho_arquivo, hash_arquivo = match(
            ServidorSolicitaEnvioArquivoRecuperadoParaCliente.pattern,
            mensagem
        ).groups()
        return ServidorSolicitaEnvioArquivoRecuperadoParaCliente(
            tamanho_arquivo=tamanho_arquivo,
            hash_arquivo=hash_arquivo,
        )


class SolicitacaoRegistrarMirror(Protocolo):

    pattern = '^comando:([a-z]{1})\|id_mirror:(.*)$'

    def __init__(self, comando, id_mirror):
        self.comando = comando
        self.id_mirror = id_mirror

    def encapsular(self):
        return "comando:{}|id_mirror:{}".format(
            self.comando, self.id_mirror
        )

    @staticmethod
    def desencapsular(mensagem):
        comando, id_mirror = match(
            SolicitacaoRegistrarMirror.pattern,
            mensagem
        ).groups()
        return SolicitacaoRegistrarMirror(
            comando=comando,
            id_mirror=id_mirror
        )


class ServidorsolicitarReplicarArquivo(Protocolo):

    pattern = '^id_cliente:(.*)\|tamanho_arquivo:(\d+)\|hash_arquivo:(.*)\|nome_arquivo:(.*)$'

    def __init__(self, id_cliente, tamanho_arquivo, hash_arquivo, nome_arquivo):
        self.id_cliente = id_cliente
        self.tamanho_arquivo = tamanho_arquivo
        self.hash_arquivo = hash_arquivo
        self.nome_arquivo = nome_arquivo

    def encapsular(self):
        return "id_cliente:{}|tamanho_arquivo:{}|hash_arquivo:{}|nome_arquivo:{}".format(
            self.id_cliente, self.tamanho_arquivo, self.hash_arquivo, self.nome_arquivo
        )

    @staticmethod
    def desencapsular(mensagem):
        id_cliente, tamanho_arquivo, hash_arquivo, nome_arquivo = match(
            ServidorsolicitarReplicarArquivo.pattern,
            mensagem
        ).groups()
        return ServidorsolicitarReplicarArquivo(
            id_cliente=id_cliente,
            tamanho_arquivo=tamanho_arquivo,
            hash_arquivo=hash_arquivo,
            nome_arquivo=nome_arquivo
        )


class ServidorSolicitarRecuperacaoArquivoMirror(Protocolo):
    pattern = '^comando:([a-z]{1})\|id_cliente:(.*)\|tamanho_arquivo:(\d+)\|hash_arquivo:(.*)\|nome_arquivo:(.*)$'

    def __init__(self, comando, id_cliente, tamanho_arquivo, hash_arquivo, nome_arquivo):
        self.comando = comando
        self.id_cliente = id_cliente
        self.tamanho_arquivo = tamanho_arquivo
        self.hash_arquivo = hash_arquivo
        self.nome_arquivo = nome_arquivo

    def encapsular(self):
        return "comando:{}|id_cliente:{}|tamanho_arquivo:{}|hash_arquivo:{}|nome_arquivo:{}".format(
            self.comando, self.id_cliente, self.tamanho_arquivo, self.hash_arquivo, self.nome_arquivo
        )

    @staticmethod
    def desencapsular(mensagem):
        comando, id_cliente, tamanho_arquivo, hash_arquivo, nome_arquivo = match(
            ServidorSolicitarRecuperacaoArquivoMirror.pattern,
            mensagem
        ).groups()
        return ServidorSolicitarRecuperacaoArquivoMirror(
            comando=comando,
            id_cliente=id_cliente,
            tamanho_arquivo=tamanho_arquivo,
            hash_arquivo=hash_arquivo,
            nome_arquivo=nome_arquivo
        )


class ResultadoRecebimentoDeArquivo(Protocolo):

    pattern = '^hash_arquivo:(.*)\|resultado:(\d+)$'

    def __init__(self, hash_arquivo, resultado):
        self.hash_arquivo = hash_arquivo
        self.resultado = resultado

    def encapsular(self):
        return "hash_arquivo:{}|resultado:{}".format(
            self.hash_arquivo, self.resultado
        )

    @staticmethod
    def desencapsular(mensagem):
        hash_arquivo, resultado = match(
            ResultadoRecebimentoDeArquivo.pattern,
            mensagem
        ).groups()
        return ResultadoRecebimentoDeArquivo(
            hash_arquivo=hash_arquivo,
            resultado=resultado
        )


class ClienteSolicitacaoAlterarReplicas(Protocolo):

    pattern = '^comando:(a)\|id_cliente:(.*)\|nome_arquivo:(.*)\|qtd_replicas:(\d+)$'

    def __init__(self, comando, id_cliente, nome_arquivo, qtd_replicas):
        self.comando = comando
        self.id_cliente = id_cliente
        self.nome_arquivo = nome_arquivo
        self.qtd_replicas = qtd_replicas

    def encapsular(self):
        return "comando:{}|id_cliente:{}|nome_arquivo:{}|qtd_replicas:{}".format(
            self.comando, self.id_cliente, self.nome_arquivo, self.qtd_replicas
        )

    @staticmethod
    def desencapsular(mensagem):
        comando, id_cliente, nome_arquivo, qtd_replicas = match(
            ClienteSolicitacaoAlterarReplicas.pattern,
            mensagem
        ).groups()
        return ClienteSolicitacaoAlterarReplicas(
            comando=comando,
            id_cliente=id_cliente,
            nome_arquivo=nome_arquivo,
            qtd_replicas=qtd_replicas
        )


class ClienteSolicitacaoListarArquivos(Protocolo):

    pattern = '^comando:(l)\|id_cliente:(.*)$'

    def __init__(self, comando, id_cliente):
        self.comando = comando
        self.id_cliente = id_cliente

    def encapsular(self):
        return "comando:{}|id_cliente:{}".format(
            self.comando, self.id_cliente
        )

    @staticmethod
    def desencapsular(mensagem):
        comando, id_cliente = match(
            ClienteSolicitacaoListarArquivos.pattern,
            mensagem
        ).groups()
        return ClienteSolicitacaoListarArquivos(
            comando=comando,
            id_cliente=id_cliente
        )
