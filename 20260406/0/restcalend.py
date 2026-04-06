import calendar
import sys


def restmonth(year, month):
    lines = calendar.TextCalendar().formatmonth(year, month).split('\n')
    strk = f'.. table:: {" ".join(lines[0].split())}'
    line2 = lines[2].split()
    line2 = [(r'\  ' * (7 - len(line2)))[:-1]] + line2
    line2 = '  '.join(line2)
    lines[2] = line2
    lines = ['', '== == == == == == =='] + [lines[1]] + ['== == == == == == =='] + lines[2:-1] + ['== == == == == == ==']
    lines = list(map(lambda x: '    ' + x, lines))
    lines = [strk] + lines
    cal = '\n'.join(lines)
    return cal


cal = restmonth(int(sys.argv[1]), int(sys.argv[2]))
f = open('/Users/maxbig/Prac_6_sem/20260406/0/doc/calend.rst', 'w')
f.write(cal)
f.close()
