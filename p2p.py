import asyncio

'''
async determina que a função vai ser executada de forma assíncrona
await determina que a vai haver espera nesse ponto, aguardando um retorno futuro
'''
#função para enviar msg, chamada pelo cliente
async def enviar_msg(writer):
    nome = input("Nome: ")
    #write escreve a mensagem pro socket e drain limpa o buffer, caso tenha sido armazenada
    writer.write(nome.encode())
    await writer.drain()
    while True:
        #to_thread permite que o input seja processado em outra thread, saindo da principal. Assim o input não bloqueia o programa
        message = await asyncio.to_thread(input, "> ")
        #encode para transformar de String para bytes 
        writer.write(message.encode())
        await writer.drain()

#função para receber msg, chamada pelo servidor
async def receber_msg(reader, writer):
    nome = (await reader.read(100)).decode()
    #O loop mantém a escuta de mensagens novas funcionando, se não houver mensagem ele para
    while True:
        data = await reader.read(100)
        if not data:
            break
        message = data.decode()
        print(f"\n[{nome}] enviou: {message}", end="")

#callback do start_server precisa do reader e writer
async def iniciar_serv():
    #Inicia servidor com socket, recebe uma função que será transformada em task e inicia ela
    #ele também retorna um StreamReader e um StreamWriter como canais de escuta e escrita
    #Por isso o uso de reader e writer é obrigatório
    server = await asyncio.start_server(receber_msg, '0.0.0.0', 8888)
    async with server:
        print("Chat p2p")
        #serve forever aceita conexões até que ela seja finalizada
        await server.serve_forever()

async def iniciar_cliente(ip, porta):
    #inicia a conexão com o servidor especificado por IP e porta
    reader, writer = await asyncio.open_connection(ip, porta)

    #async.gather mantém as duas funções dentro dele executando simultaneamente
    await asyncio.gather(
        enviar_msg(writer),
        receber_msg(reader, writer)
    )

async def main():
    ip = input("Digite o IP: ")
    porta = int(input("Digite a porta: "))
    
    await asyncio.gather(
        #mantém as duas funções executando juntas e coloca o servidor pra iniciar como uma task
        #como task, ele consegue aguardar uma corrotina
        asyncio.create_task(iniciar_serv()),
        #await iniciar_serv()
        iniciar_cliente(ip, porta)
    )
asyncio.run(main())