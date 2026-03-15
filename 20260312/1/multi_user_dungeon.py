import cowsay
import sys
from io import StringIO
import shlex
import cmd


def encounter(x, y):
    global monsters, jgsbat
    if monsters[(x, y)][0] == 'jgsbat':
        print(cowsay.cowsay(monsters[(x, y)][2], cowfile=jgsbat))
    else:
        print(cowsay.cowsay(monsters[(x, y)][2], cow=monsters[(x, y)][0]))

'''
cmd = sys.stdin.readline()
while cmd != '':
    cmd = shlex.split(cmd)
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
    elif len(cmd) == 9 and cmd[0] == 'addmon':
        name = cmd[1]
        hello_str = cmd[cmd.index('hello') + 1]
        hp = cmd[cmd.index('hp') + 1]
        xx, yy = cmd[cmd.index('coords') + 1:cmd.index('coords') + 3]
        if xx.isdigit() and yy.isdigit() and 0 <= int(xx) <= 9 and 0 <= int(yy) <= 9:
            if name not in list_cows:
                print('Cannot add unknown monster')
            else:
                print(f'Added monster {name} with health {hp} to ({xx}, {yy}) saying {hello_str}')
                if (int(xx), int(yy)) in monsters:
                    print('Replaced the old monster')
                monsters[(int(xx), int(yy))] = [name, hp, hello_str]
        else:
            print('Invalid arguements')
    elif len(cmd) >= 1 and cmd[0] in ['up', 'down', 'left', 'right', 'addmon']:
        print('Invalid arguements')
    else:
        print('Invalid command')
    cmd = sys.stdin.readline()
'''


class MUD(cmd.Cmd):
    prompt = ''
    x, y = 0, 0
    monsters = {}
    """
    def do_size(self, arg):
        '''
        print file sizes
        '''
        args = split(arg)
        for name in args:
            print(f'{name}: {Path(name).stat().st_size}')
    """
    def do_down(self, arg):
        '''
        moving down on 1 cell
        '''
        if arg == '':
            MUD.y = (MUD.y + 1) % 10
            print(f'Moved to ({MUD.x}, {MUD.y})')
            if (MUD.x, MUD.y) in MUD.monsters:
                encounter(MUD.x, MUD.y)
        else:
            print('Invalid arguements')
    
    def do_up(self, arg):
        '''
        moving up on 1 cell
        '''
        if arg == '':
            MUD.y = (MUD.y + 9) % 10
            print(f'Moved to ({MUD.x}, {MUD.y})')
            if (MUD.x, MUD.y) in MUD.monsters:
                encounter(MUD.x, MUD.y)
        else:
            print('Invalid arguements')
    
    def do_right(self, arg):
        '''
        moving right on 1 cell
        '''
        if arg == '':
            MUD.x = (MUD.x + 1) % 10
            print(f'Moved to ({MUD.x}, {MUD.y})')
            if (MUD.x, MUD.y) in MUD.monsters:
                encounter(MUD.x, MUD.y)
        else:
            print('Invalid arguements')
    
    def do_left(self, arg):
        '''
        moving left on 1 cell
        '''
        if arg == '':
            MUD.x = (MUD.x + 9) % 10
            print(f'Moved to ({MUD.x}, {MUD.y})')
            if (MUD.x, MUD.y) in MUD.monsters:
                encounter(MUD.x, MUD.y)
        else:
            print('Invalid arguements')
    
    def do_EOF(self, arg):
        return 1

if __name__ == '__main__':
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
    print("<<< Welcome to Python-MUD 0.1 >>>")
    MUD().cmdloop()
