import unittest
from unittest.mock import MagicMock, patch
from io import StringIO

from mood.client.__main__ import run

class TestClientCommands(unittest.TestCase):
    def setUp(self):
        self.stdout_patcher = patch('sys.stdout', new_callable=StringIO)
        self.mock_stdout = self.stdout_patcher.start()

        self.readline_patcher = patch('readline.get_line_buffer', return_value='')
        self.readline_patcher.start()

        self.mock_thread = MagicMock()
        self.thread_patcher = patch('threading.Thread', return_value=self.mock_thread)
        self.thread_patcher.start()

    def tearDown(self):
        self.stdout_patcher.stop()
        self.readline_patcher.stop()
        self.thread_patcher.stop()

    def _run_with_commands(self, commands, username='testuser'):
        mock_sock = MagicMock()
        # Всегда возвращаем ACCEPTED, чтобы клиент продолжил работу
        mock_sock.recv.return_value = b"ACCEPTED\n"

        with patch('socket.socket') as mock_socket_class:
            mock_socket_class.return_value = mock_sock
            with patch('builtins.input', side_effect=commands + [EOFError]):
                run(username)

        return mock_sock

    # === Тесты движения ===
    def test_move_up(self):
        mock_sock = self._run_with_commands(['up'])
        mock_sock.sendall.assert_any_call(b'move 0 -1\n')
        mock_sock.sendall.assert_any_call(b'quit\n')

    def test_move_left(self):
        mock_sock = self._run_with_commands(['left'])
        mock_sock.sendall.assert_any_call(b'move -1 0\n')
        mock_sock.sendall.assert_any_call(b'quit\n')

    # === Тесты атаки ===
    def test_attack_no_weapon(self):
        mock_sock = self._run_with_commands(['attack dragon'])
        mock_sock.sendall.assert_any_call(b'attack dragon 10\n')
        mock_sock.sendall.assert_any_call(b'quit\n')

    def test_attack_with_sword(self):
        mock_sock = self._run_with_commands(['attack dragon with sword'])
        mock_sock.sendall.assert_any_call(b'attack dragon 10\n')
        mock_sock.sendall.assert_any_call(b'quit\n')

    def test_attack_with_spear(self):
        mock_sock = self._run_with_commands(['attack dragon with spear'])
        mock_sock.sendall.assert_any_call(b'attack dragon 15\n')
        mock_sock.sendall.assert_any_call(b'quit\n')

    # === Ошибочные команды атаки ===
    def test_attack_invalid_no_args(self):
        mock_sock = self._run_with_commands(['attack'])
        mock_sock.sendall.assert_any_call(b'Invalid command\n')
        mock_sock.sendall.assert_any_call(b'quit\n')

    def test_attack_invalid_weapon(self):
        mock_sock = self._run_with_commands(['attack dragon with gun'])
        mock_sock.sendall.assert_any_call(b'Invalid command\n')
        mock_sock.sendall.assert_any_call(b'quit\n')

    # === Некорректная команда addmon ===
    def test_addmon_invalid_coords(self):
        cmd = 'addmon troll hello "Hello!" hp 100 coords 10 10'
        mock_sock = self._run_with_commands([cmd])
        mock_sock.sendall.assert_any_call(b'Invalid arguements\n')
        mock_sock.sendall.assert_any_call(b'quit\n')

if __name__ == "__main__":
    unittest.main()
