import socket
import pickle
import curses
from multiprocessing.connection import Client
from screens.join_game import insert_IP
from modes.client_game import ClientGame




def client_socket(screen):
    curses.curs_set(0)
    ip = insert_IP(screen)
    host_port = 8080

    # Setup socket and connect to host
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket = Client((ip, host_port))

    screen.addstr(f"\t2. Waiting for host to start the game..\n\n")
    screen.refresh()

    # Listen for verification message from host
    host_msg = client_socket.recv()
    screen.addstr(host_msg)
    screen.refresh()
    screen.clear()
    screen.refresh()

    # Start the online Game
    game = ClientGame(screen, client_socket)
    game.game_loop() # Loops until a player presses Q to quit the game session

    # One of the players has ended the online game session
    client_socket.close()
