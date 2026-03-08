import cowsay
import sys
from io import StringIO


def encounter(x, y):
    global monsters, jgsbat
    if monsters[(x, y)][0] == 'jgsbat':
        print(cowsay.cowsay(monsters[(x, y)][1], cowfile=jgsbat))
    else:
        print(cowsay.cowsay(monsters[(x, y)][1], cow=monsters[(x, y)][0]))


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
list_cows = cowsay.list_cows()
list_cows.append('jgsbat')
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
    elif len(cmd) == 5 and cmd[0] == 'addmon':
        cmd = [cmd[0], cmd[2], cmd[3], cmd[1], cmd[4]]
        if cmd[1].isdigit() and cmd[2].isdigit() and 0 <= int(cmd[1]) <= 9 and 0 <= int(cmd[2]) <= 9:
            if cmd[3] not in list_cows:
                print('Cannot add unknown monster')
            else:
                print(f'Added monster {cmd[3]} to ({int(cmd[1])}, {int(cmd[2])}) saying {cmd[4]}')
                if (int(cmd[1]), int(cmd[2])) in monsters:
                    print('Replaced the old monster')
                monsters[(int(cmd[1]), int(cmd[2]))] = [cmd[3], cmd[4]]
        else:
            print('Invalid arguements')
    elif len(cmd) >= 1 and cmd[0] in ['up', 'down', 'left', 'right', 'addmon']:
        print('Invalid arguements')
    else:
        print('Invalid command')
    cmd = sys.stdin.readline()
