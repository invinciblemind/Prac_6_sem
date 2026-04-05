#!/usr/bin/env python3
import asyncio
import cowsay
import shlex
from io import StringIO


clients = {}
active_users = set()

monsters = {}
list_cows = cowsay.list_cows()
list_cows.append('jgsbat')
jgsbat = cowsay.read_dot_cow(StringIO("""
$the_cow = <<EOC;
         $thoughts
          $thoughts
    ,_                    _,
    ) '-._  ,_    _,  _.-' (
    )  _.-'.|\\\\--//|.'-._  (
     )'   .'\\/o\\/o\\/'.   `(
      ) .' . \\====/ . '. (
       )  / <<    >> \\  (
        '-._/``  ``\\_.-'
  jgs     __\\\\'--'//__
         (((""`  `"")))
EOC
"""))

async def chat(reader, writer):
    me = "{}:{}".format(*writer.get_extra_info('peername'))
    print(me)
    try:
        username = (await reader.readline()).decode().strip()
        if username in active_users:
            writer.write("DENIED\n".encode())
            await writer.drain()
            writer.close()
            return
        for out in clients.values():
            await out.put(f'{username} is connected')
        active_users.add(username)
        writer.write("ACCEPTED\n".encode())
        await writer.drain()
    except:
        writer.close()
        return
    clients[username] = asyncio.Queue()
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(clients[username].get())
    q = 0
    
    x, y = 0, 0
    
    while not reader.at_eof():
        done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)
        for q in done:
            if q is send:
                msg = q.result().decode()[:-1]
                cmd = shlex.split(msg)
                if msg in ['Invalid command', 'Invalid arguements']:
                    send = asyncio.create_task(reader.readline())
                    await clients[username].put(msg)
                elif cmd[0] == 'move':
                    x = (x + 10 + int(cmd[1])) % 10
                    y = (y + 10 + int(cmd[2])) % 10
                    reply = f'Moved to ({x}, {y})\n'
                    if (x, y) in monsters:
                        if monsters[(x, y)][0] == 'jgsbat':
                            reply += cowsay.cowsay(monsters[(x, y)][2], cowfile=jgsbat)
                        else:
                            reply += cowsay.cowsay(monsters[(x, y)][2], cow=monsters[(x, y)][0])
                    send = asyncio.create_task(reader.readline())
                    await clients[username].put(reply)
                elif cmd[0] == 'addmon':
                    name = cmd[1]
                    hello_str = cmd[cmd.index('hello') + 1]
                    hp = cmd[cmd.index('hp') + 1]
                    xx, yy = cmd[cmd.index('coords') + 1:cmd.index('coords') + 3]
                    if name not in list_cows:
                        send = asyncio.create_task(reader.readline())
                        await clients[username].put('Cannot add unknown monster')
                    else:
                        reply = f'Added monster {name} with health {hp} to ({xx}, {yy}) saying {hello_str}\n'
                        if (int(xx), int(yy)) in monsters:
                            reply += 'Replaced the old monster'
                        monsters[(int(xx), int(yy))] = [name, int(hp), hello_str]
                        send = asyncio.create_task(reader.readline())
                        for out in clients.values():
                            await out.put(reply)
                elif cmd[0] == 'attack':
                    if (x, y) not in monsters:
                        send = asyncio.create_task(reader.readline())
                        await clients[username].put(f'No {cmd[1]} here')
                    elif monsters[(x, y)][0] != cmd[1]:
                        send = asyncio.create_task(reader.readline())
                        await clients[username].put(f'No {cmd[1]} here')
                    else:
                        damage = min(int(cmd[2]), monsters[(x, y)][1])
                        reply = f'Attacked {monsters[(x, y)][0]}, damage {damage} hp\n'
                        monsters[(x, y)][1] -= damage
                        if monsters[(x, y)][1] == 0:
                            reply += f'{monsters[(x, y)][0]} died'
                            del monsters[(x, y)]
                        else:
                            reply += f'{monsters[(x, y)][0]} now has {monsters[(x, y)][1]}'
                        send = asyncio.create_task(reader.readline())
                        for out in clients.values():
                            await out.put(reply)
                elif cmd[0] == 'sayall':
                    reply = f'{username}: {cmd[1]}'
                    send = asyncio.create_task(reader.readline())
                    for out in clients.values():
                        if out != clients[username]:
                            await out.put(reply)
                elif cmd[0] == 'quit':
                    q = 1
                    break
            elif q is receive:
                receive = asyncio.create_task(clients[username].get())
                writer.write(f"{q.result()}\n".encode())
                await writer.drain()
        if q == 1:
            break
    send.cancel()
    receive.cancel()
    print(me, "DONE")
    del clients[username]
    for out in clients.values():
        await out.put(f'{username} left')
    active_users.remove(username)
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(chat, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())
