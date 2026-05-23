#!/usr/bin/env python3
"""MUD scripting utility for automated testing."""

import cmd
import sys
import time
import socket
import shlex
import threading
import argparse


class MUDShell(cmd.Cmd):
    """MUD command shell for scripted interaction with server."""

    def __init__(self, sock, stdin=None):
        """
        Initialize MUD shell.

        Args:
            sock: Connected socket to MUD server
            stdin: File object for input (default: sys.stdin)
        """
        super().__init__(stdin=stdin)
        self.sock = sock
        self.last_command_time = 0
        self.min_interval = 1.0  # Minimum 1 second between commands
        
        # Configure for file input
        if stdin is not None:
            self.prompt = ''
            self.use_rawinput = False

    def do_bless(self, arg):
        """
        Send bless command to server.

        Usage: bless <name>
        Prints: "Be blessed, <name>!"
        """
        if not arg:
            print("Usage: bless <name>")
            return
        
        # Rate limiting
        self._rate_limit()
        
        # Send to server (adapt for MUD protocol)
        message = f"sayall Be blessed, {arg}!"
        self.sock.sendall((message + '\n').encode())
        
        # Also print locally for script output
        print(f"Be blessed, {arg}!")

    def do_sendto(self, arg):
        """
        Send sendto command to server.

        Usage: sendto <direction>
        Prints: "Go to <direction>!"
        """
        if not arg:
            print("Usage: sendto <direction>")
            return
        
        # Rate limiting
        self._rate_limit()
        
        # Map directions to move commands
        direction_map = {
            'up': 'move 0 -1',
            'down': 'move 0 1',
            'left': 'move -1 0',
            'right': 'move 1 0'
        }
        
        if arg in direction_map:
            self.sock.sendall((direction_map[arg] + '\n').encode())
        else:
            self.sock.sendall((f"sayall Go to {arg}!\n").encode())
        
        print(f"Go to {arg}!")

    def do_quit(self, arg):
        """Exit the shell."""
        print("Goodbye!")
        self.sock.sendall("quit\n".encode())
        return True

    def do_EOF(self, arg):
        """Handle EOF (Ctrl+D or end of file)."""
        print()
        return True

    def _rate_limit(self):
        """Ensure minimum interval between commands."""
        elapsed = time.time() - self.last_command_time
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self.last_command_time = time.time()

    def default(self, line):
        """Handle unknown commands."""
        print(f"Unknown command: {line}")


def receive_messages(sock, stop_event):
    """Background thread to receive and display server messages."""
    while not stop_event.is_set():
        try:
            sock.settimeout(1.0)
            reply = sock.recv(1024).rstrip().decode()
            if reply:
                print(f"\n[Server] {reply}")
                # Reprint prompt if needed
                if hasattr(receive_messages, 'prompt'):
                    print(receive_messages.prompt, end='', flush=True)
        except socket.timeout:
            continue
        except:
            break


def connect_to_server(host='localhost', port=1337):
    """Connect to MUD server."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    return sock


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='MUD scripting utility')
    parser.add_argument('--file', help='Script file to execute (.mood)')
    args = parser.parse_args()

    # Connect to server
    try:
        sock = connect_to_server()
    except ConnectionRefusedError:
        print("Error: Cannot connect to MUD server on localhost:1337")
        sys.exit(1)

    # Get username
    username = input("Enter username: ")
    sock.sendall((username + '\n').encode())
    
    response = sock.recv(1024).decode().strip()
    if response == "DENIED":
        print("Username already taken")
        sock.close()
        sys.exit(1)
    print(f"Connected as {username}")

    # Setup background receiver
    stop_event = threading.Event()
    receiver = threading.Thread(target=receive_messages, args=(sock, stop_event))
    receiver.daemon = True
    receiver.start()

    # Create shell with appropriate input source
    if args.file:
        try:
            with open(args.file, 'r') as script_file:
                shell = MUDShell(sock, stdin=script_file)
                print(f"Executing script: {args.file}")
                shell.cmdloop()
        except FileNotFoundError:
            print(f"Error: File '{args.file}' not found")
            sock.close()
            sys.exit(1)
    else:
        shell = MUDShell(sock)
        shell.prompt = 'mud> '
        shell.cmdloop()

    # Cleanup
    stop_event.set()
    sock.close()


if __name__ == "__main__":
    main()
