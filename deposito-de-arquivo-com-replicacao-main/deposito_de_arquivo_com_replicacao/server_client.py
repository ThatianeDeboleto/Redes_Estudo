import signal
import socket

from deposito_de_arquivo_com_replicacao import utils
from deposito_de_arquivo_com_replicacao.config import settings


class ServerClient:
    def __init__(self, server_client_id, ip, port):
        self.id = server_client_id
        self.ip = ip
        self.port = port
        self.socket = None
        self.connected = False

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.ip, self.port))
        self.connected = True

    def send(self, message):
        if isinstance(message, str):
            message = message.encode()
        self.socket.send(message)

    def receive(self):
        return self.socket.recv(settings.get('geral.tamanho_buffer_padrao')).decode()

    def close(self):
        self.socket.close()
        self.connected = False

    def signal_handler(self):
        print('Encerrando...')
        self.close()
        exit()

    @classmethod
    def create(cls, args):

        host = args[1] if len(args) > 1 else str(input('Digite o host: '))
        port = int(args[2]) if len(args) > 2 else int(input('Digite a porta: '))

        server_client_id = str(args[3]) \
            if len(args) > 3 \
            else str(input('Digite o id, pode deixar em branco para criar uma nova sessão: '))

        if server_client_id == '':
            server_client_id = utils.generate_uuid()
            print('Seu id: {}'.format(server_client_id))
            print('Guarde o id para futuras sessões')
        elif utils.is_valid_uuid(server_client_id) is False:
            print('id inválido')
            return

        server_client = cls(server_client_id, host, port)
        server_client.connect()

        signal.signal(signal.SIGINT, lambda signum, frame: server_client.signal_handler())

        return server_client
