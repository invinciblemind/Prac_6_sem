import cowsay
import sys
from io import StringIO
import shlex
import cmd


def encounter(x, y):
    global jgsbat
    if MUD.monsters[(x, y)][0] == 'jgsbat':
        print(cowsay.cowsay(MUD.monsters[(x, y)][2], cowfile=jgsbat))
    else:
        print(cowsay.cowsay(MUD.monsters[(x, y)][2], cow=MUD.monsters[(x, y)][0]))


class MUD(cmd.Cmd):
    prompt = ''
    x, y = 0, 0
    monsters = {}
    
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
    
    def do_addmon(self, arg):
        '''
        adding a monster on the cell with hello phrase and hp
        '''
        command = shlex.split(arg)
        if len(command) == 8:
            name = command[0]
            hello_str = command[command.index('hello') + 1]
            hp = command[command.index('hp') + 1]
            xx, yy = command[command.index('coords') + 1:command.index('coords') + 3]
            if xx.isdigit() and yy.isdigit() and hp.isdigit() and 0 <= int(xx) <= 9 and 0 <= int(yy) <= 9:
                if name not in MUD.list_cows:
                    print('Cannot add unknown monster')
                else:
                    print(f'Added monster {name} with health {hp} to ({xx}, {yy}) saying {hello_str}')
                    if (int(xx), int(yy)) in MUD.monsters:
                        print('Replaced the old monster')
                    MUD.monsters[(int(xx), int(yy))] = [name, int(hp), hello_str]
            else:
                print('Invalid arguements')
        else:
            print('Invalid arguements')
    
    def do_attack(self, arg):
        '''
        attacking a monster on the current cell
        '''
        if arg == '':
            if (MUD.x, MUD.y) in MUD.monsters:
                damage = min(10, MUD.monsters[(MUD.x, MUD.y)][1])
                print(f'Attacked {MUD.monsters[(MUD.x, MUD.y)][0]}, damage {damage} hp')
                MUD.monsters[(MUD.x, MUD.y)][1] -= damage
                if MUD.monsters[(MUD.x, MUD.y)][1] == 0:
                    print(f'{MUD.monsters[(MUD.x, MUD.y)][0]} died')
                    del MUD.monsters[(MUD.x, MUD.y)]
                else:
                    print(f'{MUD.monsters[(MUD.x, MUD.y)][0]} now has {MUD.monsters[(MUD.x, MUD.y)][1]}')
            else:
                print('No monster here')
        else:
            print('Invalid arguements')
    
    def default(self, arg):
        print('Invalid command')
    
    def do_EOF(self, arg):
        return 1


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
MUD.list_cows = list_cows
if __name__ == '__main__':
    print("<<< Welcome to Python-MUD 0.1 >>>")
    MUD().cmdloop()
