import asyncio

async def echo(reader, writer):
    while data := await reader.readline():
        cmd = data.decode()
        if len(cmd.split()) >= 2:
            if cmd.split()[0] == 'print':
                writer.write(data.decode().split('print ')[1].encode())
            elif cmd.split()[0] == 'info' and len(cmd.split()) == 2:
                if cmd.split()[1] == 'host':
                    host = writer.get_extra_info('peername')[0] + '\n'
                    writer.write(host.encode())
                elif cmd.split()[1] == 'port':
                    port = str(writer.get_extra_info('peername')[1]) + '\n'
                    writer.write(port.encode())
                else:
                    writer.write('unknown command\n'.encode())
            else:
                writer.write('unknown command\n'.encode())
        else:
            writer.write('unknown command\n'.encode())
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(echo, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())
