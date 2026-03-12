#!/usr/bin/env python3

import cmd
from shlex import split
from pathlib import Path

class SizeCmd1(cmd.Cmd):
    prompt = '==> '
    
    def do_size(self, arg):
        '''
        print file sizes
        '''
        args = split(arg)
        for name in args:
            print(f'{name}: {Path(name).stat().st_size}')
    
    def do_EOF(self, arg):
        print('\nbye\n')
        return 1

if __name__ == '__main__':
    SizeCmd1().cmdloop()
