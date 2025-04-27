import asyncio
import queue

async def enviar_msg(writer):
    nome = input("Nome: ")
    writer.write(nome.encode())
    await writer.drain()
    while True:
        message = await asyncio.to_thread(input, "> ")
        writer.write(message.encode())
        await writer.drain()
    
async def receber_msg(reader, writer):
    nome = (await reader.read(100)).decode()
    while True:
        data = await reader.read(100)
        if not data:
            break
        message = data.decode()
        print(f"\n[{nome}] enviou: {message}", end="",flush=True)

    
async def iniciar_serv():
    server = await asyncio.start_server(receber_msg, '0.0.0.0', 8888)
    async with server:
        print("Chat p2p")
        await server.serve_forever()

async def iniciar_cliente(ip, porta):
    reader, writer = await asyncio.open_connection(ip, porta)

    await asyncio.gather(
        enviar_msg(writer),
        receber_msg(reader, writer)
    )

async def main():
    ip = input("Digite o IP: ")
    porta = int(input("Digite a porta: "))
    
    await asyncio.gather(
        asyncio.create_task(iniciar_serv()),
        #await iniciar_serv()
        iniciar_cliente(ip, porta)
    )
asyncio.run(main())