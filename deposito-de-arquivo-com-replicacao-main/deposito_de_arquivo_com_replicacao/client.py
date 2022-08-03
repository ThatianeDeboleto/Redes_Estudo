import os
import sys
import hashlib

from re import match
from deposito_de_arquivo_com_replicacao.config import settings
from deposito_de_arquivo_com_replicacao import enums, utils, protocolo
from deposito_de_arquivo_com_replicacao.server_client import ServerClient


class Client(ServerClient):

    def depositar_arquivo(self):
        self.send(enums.Comando.DEPOSITAR_ARQUIVO.value)
        replicas_disponiveis = int(self.receive())
        arquivo = str(input('Digite o caminho do arquivo: '))
        print('Replicas disponíveis: {}'.format(replicas_disponiveis))
        replicas = int(input('Digite quantas replicas: '))
        if replicas > replicas_disponiveis:
            print('Não há replicas disponíveis')
            return

        arquivo_nome = arquivo.split('/')[-1]
        arquivo_tamanho = os.path.getsize(arquivo)

        sha256_hash = hashlib.sha256()
        with open(arquivo, 'rb') as f:
            for byte_block in iter(lambda: f.read(settings.get('geral.tamanho_buffer_arquivo')), b''):
                sha256_hash.update(byte_block)

        arquivo_hash = sha256_hash.hexdigest()

        solicitacao = protocolo.ClienteSolicitacaoDepositarArquivo(
            id_cliente=self.id,
            qtd_replicas=replicas,
            nome_arquivo=arquivo_nome,
            hash_arquivo=arquivo_hash,
            tamanho_arquivo=arquivo_tamanho
        ).encapsular()
        self.send(solicitacao)

        utils.enviar_arquivo_por_socket(
            socket_destinatario=self.socket,
            tamanho_arquivo=arquivo_tamanho,
            caminho_arquivo=arquivo
        )

    def recuperar_arquivo(self):
        self.send(enums.Comando.RECUPERAR_ARQUIVO.value)
        arquivo_nome = str(input('Digite nome do arquivo: '))

        solicitacao = protocolo.ClienteSolicitacaoRecuperarArquivo(
            id_cliente=self.id,
            nome_arquivo=arquivo_nome
        ).encapsular()
        self.send(solicitacao)

        resultado = self.receive()
        if resultado == enums.Retorno.ERRO.value:
            print('Arquivo não encontrado')
            return
        elif match(protocolo.ServidorSolicitaEnvioArquivoRecuperadoParaCliente.pattern, resultado):
            print('Arquivo disponível')
            dados_arquivo_recuperado = protocolo.ServidorSolicitaEnvioArquivoRecuperadoParaCliente.desencapsular(
                mensagem=resultado
            )

            caminho_arquivo = os.path.join(
                settings.get('client.pasta_recuperados'),
                arquivo_nome
            )
            tamanho_arquivo = int(dados_arquivo_recuperado.tamanho_arquivo)

            utils.receber_arquivo_por_socket(
                socket_origem=self.socket,
                tamanho_arquivo=tamanho_arquivo,
                caminho_arquivo=caminho_arquivo,
                hash_arquivo=dados_arquivo_recuperado.hash_arquivo
            )

    def listar_arquivos(self):
        solicitacao = protocolo.ClienteSolicitacaoListarArquivos(
            comando=enums.Comando.LISTAR_ARQUIVOS.value,
            id_cliente=self.id
        ).encapsular()
        self.send(solicitacao)
        resultado = self.receive()
        if resultado == enums.Retorno.ERRO.value:
            print('Não há arquivos disponíveis')
            return
        else:
            print('Arquivos disponíveis:\n')
            print(resultado.replace(',', '\n'))
            print('\n')

    def alterar_replicas(self):
        arquivo_nome = str(input('Digite nome do arquivo: '))
        replicas = int(input('Digite quantas replicas: '))
        solicitacao = protocolo.ClienteSolicitacaoAlterarReplicas(
            comando=enums.Comando.ALTERAR_REPLICAS.value,
            id_cliente=self.id,
            nome_arquivo=arquivo_nome,
            qtd_replicas=replicas
        ).encapsular()
        self.send(solicitacao)
        print('Replicas alteradas com sucesso')


def main(args):
    client = Client.create(args)

    while True:
        print('d - Depositar arquivo\nr - Recuperar arquivo\nl - Listar arquivos\na - Alterar replicas\ns - Sair')
        comando = str(input('Digite o comando: '))

        if comando == enums.Comando.ENCERRAR_CONEXAO.value:
            break
        elif comando == enums.Comando.DEPOSITAR_ARQUIVO.value:
            client.depositar_arquivo()
        elif comando == enums.Comando.RECUPERAR_ARQUIVO.value:
            client.recuperar_arquivo()
        elif comando == enums.Comando.ALTERAR_REPLICAS.value:
            client.alterar_replicas()
        elif comando == enums.Comando.LISTAR_ARQUIVOS.value:
            client.listar_arquivos()
        else:
            print('Comando inválido')

    client.close()


if __name__ == '__main__':
    main(sys.argv)
    exit()
