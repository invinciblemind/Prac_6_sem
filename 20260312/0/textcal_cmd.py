#!/usr/bin/env python3

import cmd
from shlex import split
from pathlib import Path
from calendar import TextCalendar

class Cal(cmd.Cmd):
    prompt = '>>> '
    
    def do_prmonth(self, args):
        '''
        Print a month’s calendar as returned by formatmonth().
        '''
        args = args.split()
        if len(args) != 2:
            print('Incorrect args')
        else:
            arg1, arg2 = args
            if arg1.isdigit() and arg2.isdigit() and 1 <= int(arg2) <= 12:
                arg1, arg2 = int(arg1), int(arg2)
                TextCalendar().prmonth(arg1, arg2)
            else:
                print('Incorrect args')
    def do_pryear(self, arg):
        '''
        Print the calendar for an entire year as returned by formatyear().
        '''
        if arg.isdigit():
            TextCalendar().pryear(int(arg))
        else:
            print('Incorrect args')
    
    def do_EOF(self, arg):
        print('\nbye\n')
        return 1

if __name__ == '__main__':
    Cal().cmdloop()
