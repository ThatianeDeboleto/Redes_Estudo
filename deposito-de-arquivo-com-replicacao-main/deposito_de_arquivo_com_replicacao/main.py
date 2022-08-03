from deposito_de_arquivo_com_replicacao import server, client, mirror


if __name__ == '__main__':
    print('\n1 - Servidor\n2 - Cliente\n3 - Mirror')
    opcao = int(input('Digite a opção desejada: '))
    if opcao == 1:
        server.main([])
    elif opcao == 2:
        client.main([])
    elif opcao == 3:
        mirror.main([])
    else:
        print('Opção inválida')
        exit()
    print('\nFim do programa')
    exit()

