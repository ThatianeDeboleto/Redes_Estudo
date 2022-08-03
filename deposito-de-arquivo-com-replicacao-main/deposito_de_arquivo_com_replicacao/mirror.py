import os
import sys
import threading

from re import match

from deposito_de_arquivo_com_replicacao.config import settings
from deposito_de_arquivo_com_replicacao import utils, enums, protocolo
from deposito_de_arquivo_com_replicacao.server_client import ServerClient


class Mirror(ServerClient):

    def registrar_mirror(self):
        print('Registrando mirror {}'.format(self.id))
        self.send(
            protocolo.SolicitacaoRegistrarMirror(
                comando=enums.Comando.REGISTRAR_MIRROR.value,
                id_mirror=self.id,
            ).encapsular()
        )
        resposta = self.receive()
        if resposta == enums.Retorno.OK.value:
            print('Mirror registrado com sucesso.')
        else:
            print('Erro ao registrar mirror.')
            sys.exit(1)

    def salvar_replica(self, mensagem):
        print('Salvando replica')

        solicitacao = protocolo.ServidorsolicitarReplicarArquivo.desencapsular(mensagem)

        pasta = os.path.join(settings.get('mirror.pasta_mirror'), solicitacao.id_cliente)
        if not os.path.exists(pasta):
            os.makedirs(pasta)

        arquivo_tamanho = int(solicitacao.tamanho_arquivo)
        nome_arquivo = "{}.{}".format(solicitacao.hash_arquivo, solicitacao.nome_arquivo)
        print('Nome do arquivo a ser replicado: {}'.format(nome_arquivo))
        caminho_completo = os.path.join(pasta, nome_arquivo)

        self.send(enums.Retorno.OK.value)
        utils.receber_arquivo_por_socket(
            socket_origem=self.socket,
            caminho_arquivo=caminho_completo,
            tamanho_arquivo=arquivo_tamanho,
            hash_arquivo=solicitacao.hash_arquivo
        )

    def recuperar_arquivo(self, mensagem):

        solicitacao = protocolo.ServidorSolicitarRecuperacaoArquivoMirror.desencapsular(mensagem)
        print('Recuperando arquivo: {}'.format(solicitacao))
        pasta = os.path.join(settings.get('mirror.pasta_mirror'), solicitacao.id_cliente)
        if not os.path.exists(pasta):
            self.socket.send(enums.Retorno.ERRO.value.encode())
            print('Erro ao recuperar arquivo: pasta não encontrada')
            return

        lista_de_arquivos = os.listdir(pasta)

        arquivos_na_pasta_do_cliente = [arquivo.split('.', 1)[1] for arquivo in lista_de_arquivos]
        hashs_arquivos_na_pasta_do_cliente = [arquivo.split('.', 1)[0] for arquivo in lista_de_arquivos]
        print('Arquivos na pasta do cliente: {}'.format(arquivos_na_pasta_do_cliente))
        if solicitacao.nome_arquivo not in arquivos_na_pasta_do_cliente:
            self.socket.send(enums.Retorno.ERRO.value.encode())
            print('Erro ao recuperar arquivo: arquivo não encontrado')
            return

        indice_arquivo = arquivos_na_pasta_do_cliente.index(solicitacao.nome_arquivo)
        hash_arquivo = hashs_arquivos_na_pasta_do_cliente[indice_arquivo]

        caminho_completo = os.path.join(pasta, "{}.{}".format(hash_arquivo, solicitacao.nome_arquivo))
        arquivo_tamanho = os.path.getsize(caminho_completo)

        self.socket.send(enums.Retorno.OK.value.encode())

        utils.enviar_arquivo_por_socket(
            socket_destinatario=self.socket,
            caminho_arquivo=caminho_completo,
            tamanho_arquivo=arquivo_tamanho
        )

def main(args):
    mirror = Mirror.create(args)
    mirror.registrar_mirror()

    print('Rodando. Precione Ctrl+C para sair')
    while True:
        solicitacao = mirror.receive()
        print(solicitacao)
        if match(protocolo.ServidorsolicitarReplicarArquivo.pattern, solicitacao):
            mirror.salvar_replica(solicitacao)
        elif match(protocolo.ServidorSolicitarRecuperacaoArquivoMirror.pattern, solicitacao):
            mirror.recuperar_arquivo(solicitacao)



if __name__ == '__main__':
    main(sys.argv)
    exit()
