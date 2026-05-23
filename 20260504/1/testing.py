import sys

sys.path.append('/Users/maxbig/Prac_6_sem/20260420/1/mood/server')
sys.path.append('/Users/maxbig/Prac_6_sem/20260420/1/mood/client')

import server as srv
import socket
import unittest
import __main__ as cli
import multiprocessing
import time
import subprocess


class TestMVC(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.proc = multiprocessing.Process(target=srv.start_server)
        cls.proc.start()
        time.sleep(1)
    
    def setUp(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(('127.0.0.1', 1337))

    def test1_monster_place(self):
        test = "addmon cheese coords 1 2 hp 111 hello 'hiii'"
        output = subprocess.check_output(f"echo '{test}' | python mood/client/__main__.py max", shell=True, text=True)
        corr = 'ACCEPTED\n\nAdded monster cheese with health 111 hps to (1, 2) saying hiii\n'
        self.assertEqual(output, corr)
    
    def test2_meeting_with_monster(self):
        test = "down\ndown\nright"
        output = subprocess.check_output(f"echo '{test}' | python mood/client/__main__.py max", shell=True, text=True)
        corr = r'''ACCEPTED

Moved to (0, 1)

Moved to (0, 2)

Moved to (1, 2)
 ______ 
< hiii >
 ------ 
   \
    \
      _____   _________
     /     \_/         |
    |                 ||
    |                 ||
   |    ###\  /###   | |
   |     0  \/  0    | |
  /|                 | |
 / |        <        |\ \
| /|                 | | |
| |     \_______/   |  | |
| |                 | / /
/||                 /|||
   ----------------|
        | |    | |
        ***    ***
       /___\  /___\
'''
        self.assertEqual(output, corr)
    
    def test3_attack_on_monster(self):
        test = "down\ndown\nright\nattack cheese with axe"
        output = subprocess.check_output(f"echo '{test}' | python mood/client/__main__.py max", shell=True, text=True)
        corr = r'''ACCEPTED

Moved to (0, 1)

Moved to (0, 2)

Moved to (1, 2)
 ______ 
< hiii >
 ------ 
   \
    \
      _____   _________
     /     \_/         |
    |                 ||
    |                 ||
   |    ###\  /###   | |
   |     0  \/  0    | |
  /|                 | |
 / |        <        |\ \
| /|                 | | |
| |     \_______/   |  | |
| |                 | / /
/||                 /|||
   ----------------|
        | |    | |
        ***    ***
       /___\  /___\

Attacked cheese, damage 20 hps
cheese now has 91 hps
'''
        self.assertEqual(output, corr)
    
    def tearDown(self):
        self.s.close()
    
    @classmethod
    def tearDownClass(cls):
        cls.proc.kill()


if __name__ == "__main__":
    unittest.main()
