from cowsay import cowsay
import sys


def encounter(x, y):
    global monsters
    print(cowsay(monsters[(x, y)]))


x, y = 0, 0
monsters = {}
cmd = sys.stdin.readline()
while cmd != '':
    cmd = cmd.split()
    if len(cmd) == 1:
        if cmd[0] == 'up':
            y = (y + 9) % 10
        elif cmd[0] == 'down':
            y = (y + 1) % 10
        elif cmd[0] == 'left':
            x = (x + 9) % 10
        elif cmd[0] == 'right':
            x = (x + 1) % 10
        else:
            print('Invalid command')
        if cmd[0] in ['up', 'down', 'left', 'right']:
            print(f'Moved to ({x}, {y})')
            if (x, y) in monsters:
                encounter(x, y)
    elif len(cmd) == 4 and cmd[0] == 'addmon':
        if cmd[1].isdigit() and cmd[2].isdigit() and 0 <= int(cmd[1]) <= 9 and 0 <= int(cmd[2]) <= 9:
            print(f'Added monster to ({int(cmd[1])}, {int(cmd[2])}) saying {cmd[3]}')
            if (int(cmd[1]), int(cmd[2])) in monsters:
                print('Replaced the old monster')
            monsters[(int(cmd[1]), int(cmd[2]))] = cmd[3]
        else:
            print('Invalid arguements')
    elif len(cmd) >= 1 and cmd[0] in ['up', 'down', 'left', 'right', 'addmon']:
        print('Invalid arguements')
    else:
        print('Invalid command')
    cmd = sys.stdin.readline()
