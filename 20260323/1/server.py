import asyncio
import shlex
import cowsay


async def echo(reader, writer):
    x, y = 0, 0
    monsters = {}
    list_cows = cowsay.list_cows()
    list_cows.append('jgsbat')
    while data := await reader.readline():
        msg = data.decode()[:-1]
        cmd = shlex.split(msg)
        if msg in ['Invalid command', 'Invalid arguements']:
            writer.write(data)
        elif cmd[0] == 'move':
            x += int(cmd[1])
            y += int(cmd[2])
            reply = f'Moved to ({x}, {y})\n'
            if (x, y) in monsters:
                if monsters[(x, y)][0] == 'jgsbat':
                    reply += f'{monsters[(x, y)][2]}, cowfile=jgsbat'
                else:
                    reply += f'{monsters[(x, y)][2]}, cow={monsters[(x, y)][0]}'
            writer.write(reply.encode())
        elif cmd[0] == 'addmon':
            name = cmd[1]
            hello_str = cmd[cmd.index('hello') + 1]
            hp = cmd[cmd.index('hp') + 1]
            xx, yy = cmd[cmd.index('coords') + 1:cmd.index('coords') + 3]
            if name not in list_cows:
                writer.write('Cannot add unknown monster'.encode())
            else:
                reply = f'Added monster {name} with health {hp} to ({xx}, {yy}) saying {hello_str}\n'
                if (int(xx), int(yy)) in monsters:
                    reply += 'Replaced the old monster'
                writer.write(reply.encode())
                monsters[(int(xx), int(yy))] = [name, int(hp), hello_str]
        elif cmd[0] == 'attack':
            if (x, y) not in monsters:
                writer.write(f'No {cmd[1]} here'.encode())
            elif monsters[(x, y)][0] != cmd[1]:
                writer.write(f'No {cmd[1]} here'.encode())
            else:
                damage = min(int(cmd[2]), monsters[(x, y)][1])
                reply = f'Attacked {monsters[(x, y)][0]}, damage {damage} hp\n'
                monsters[(x, y)][1] -= damage
                if monsters[(x, y)][1] == 0:
                    reply += f'{monsters[(x, y)][0]} died'
                    del monsters[(x, y)]
                else:
                    reply += f'{monsters[(x, y)][0]} now has {monsters[(x, y)][1]}'
                writer.write(reply.encode())
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(echo, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())
