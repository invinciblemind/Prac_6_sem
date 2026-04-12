"""Server program."""

import asyncio
import cowsay
import shlex
from io import StringIO
import random
import threading


clients = {}
client_writers = {}
coords_clients = {}
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
dct = {(0, 1): 'down', (0, -1): 'up', (1, 0): 'right', (-1, 0): 'left'}


async def monster_moving():
    """Move monsters."""
    while True:
        await asyncio.sleep(30)
        if monsters:
            xn, yn = random.choice(list(monsters.items()))[0]
            xp, yp = random.choice([[0, 1], [0, -1], [1, 0], [-1, 0]])
            while (xn + xp, yn + yp) in monsters:
                xn, yn = random.choice(list(monsters.items()))[0]
                xp, yp = random.choice([[0, 1], [0, -1], [1, 0], [-1, 0]])
            monsters[(xn + xp, yn + yp)] = monsters[(xn, yn)]
            del monsters[(xn, yn)]
            
            for username, writer in client_writers.items():
                try:
                    writer.write(f"{monsters[(xn + xp, yn + yp)][0]} moved one cell {dct[(xp, yp)]}\n".encode())
                    await writer.drain()
                except:
                    pass
            
            for queue, pos in coords_clients.items():
                if pos == [xn + xp, yn + yp]:
                    for name, q in clients.items():
                        if q == queue:
                            monster = monsters[(xn + xp, yn + yp)]
                            if monster[0] == 'jgsbat':
                                reply = cowsay.cowsay(monster[2], cowfile=jgsbat)
                            else:
                                reply = cowsay.cowsay(monster[2], cow=monster[0])
                            try:
                                writer_obj = client_writers.get(name)
                                if writer_obj:
                                    writer_obj.write(f"{reply}\n".encode())
                                    await writer_obj.drain()
                            except:
                                pass
                            break


def run_monster_moving():
    """Launch monster_moving function."""
    new_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(new_loop)
    new_loop.run_until_complete(monster_moving())


async def chat(reader, writer):
    """Realise all dialogs."""
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
    client_writers[username] = writer
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(clients[username].get())
    q = 0
    
    coords_clients[clients[username]] = [0, 0]
    
    while not reader.at_eof():
        done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)
        for task in done:
            if task is send:
                msg = task.result().decode()[:-1]
                cmd = shlex.split(msg)
                if msg in ['Invalid command', 'Invalid arguements']:
                    send = asyncio.create_task(reader.readline())
                    await clients[username].put(msg)
                elif cmd[0] == 'move':
                    coords_clients[clients[username]][0] = (coords_clients[clients[username]][0] + 10 + int(cmd[1])) % 10
                    coords_clients[clients[username]][1] = (coords_clients[clients[username]][1] + 10 + int(cmd[2])) % 10
                    reply = f'Moved to ({coords_clients[clients[username]][0]}, {coords_clients[clients[username]][1]})\n'
                    if (coords_clients[clients[username]][0], coords_clients[clients[username]][1]) in monsters:
                        if monsters[(coords_clients[clients[username]][0], coords_clients[clients[username]][1])][0] == 'jgsbat':
                            reply += cowsay.cowsay(monsters[(coords_clients[clients[username]][0], coords_clients[clients[username]][1])][2], cowfile=jgsbat)
                        else:
                            reply += cowsay.cowsay(monsters[(coords_clients[clients[username]][0], coords_clients[clients[username]][1])][2], cow=monsters[(coords_clients[clients[username]][0], coords_clients[clients[username]][1])][0])
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
                    if (coords_clients[clients[username]][0], coords_clients[clients[username]][1]) not in monsters:
                        send = asyncio.create_task(reader.readline())
                        await clients[username].put(f'No {cmd[1]} here')
                    elif monsters[(coords_clients[clients[username]][0], coords_clients[clients[username]][1])][0] != cmd[1]:
                        send = asyncio.create_task(reader.readline())
                        await clients[username].put(f'No {cmd[1]} here')
                    else:
                        damage = min(int(cmd[2]), monsters[(coords_clients[clients[username]][0], coords_clients[clients[username]][1])][1])
                        reply = f'Attacked {monsters[(coords_clients[clients[username]][0], coords_clients[clients[username]][1])][0]}, damage {damage} hp\n'
                        monsters[(coords_clients[clients[username]][0], coords_clients[clients[username]][1])][1] -= damage
                        if monsters[(coords_clients[clients[username]][0], coords_clients[clients[username]][1])][1] == 0:
                            reply += f'{monsters[(coords_clients[clients[username]][0], coords_clients[clients[username]][1])][0]} died'
                            del monsters[(coords_clients[clients[username]][0], coords_clients[clients[username]][1])]
                        else:
                            reply += f'{monsters[(coords_clients[clients[username]][0], coords_clients[clients[username]][1])][0]} now has {monsters[(coords_clients[clients[username]][0], coords_clients[clients[username]][1])][1]}'
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
            elif task is receive:
                receive = asyncio.create_task(clients[username].get())
                writer.write(f"{task.result()}\n".encode())
                await writer.drain()
        if q == 1:
            break
    send.cancel()
    receive.cancel()
    print(me, "DONE")
    del coords_clients[clients[username]]
    del clients[username]
    del client_writers[username]
    for out in clients.values():
        await out.put(f'{username} left')
    active_users.remove(username)
    writer.close()
    await writer.wait_closed()


async def main():
    """Start of server."""
    timer = threading.Thread(target=run_monster_moving, daemon=True)
    timer.start()
    
    server = await asyncio.start_server(chat, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
