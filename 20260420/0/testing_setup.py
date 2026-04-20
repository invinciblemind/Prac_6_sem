import echo_srv_sqroots
import socket
import unittest
import sqrootnet
import multiprocessing
import time


class TestMVC(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.proc = multiprocessing.Process(target=echo_srv_sqroots.srv)
        cls.proc.start()
        time.sleep(1)
    
    def setUp(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(('127.0.0.1', 1337))

    def test_process_input_updates_model_and_view(self):
        self.assertEqual(sqrootnet.sqrootnet('1 1 1', self.s), '')
        self.assertEqual(sqrootnet.sqrootnet('1 2 1', self.s), '-1.0')
        self.assertEqual(sqrootnet.sqrootnet('1 10 9', self.s), '-1.0 -9.0')
        self.assertEqual(sqrootnet.sqrootnet('1 1 1 1', self.s), '')
    
    def tearDown(self):
        self.s.close()
    
    def tearDownClass():
        cls.proc.stop()


if __name__ == "__main__":
    unittest.main()
