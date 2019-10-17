import socket
import pickle
import curses
from screens.join_game import insert_IP
from modes.client_game import ClientGame


from multiprocessing.connection import Client


def client_socket(screen):
    curses.curs_set(0)
    ip = insert_IP(screen)
    host_port = 8080

    # Setup socket and connect to host
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #error = client_socket.connect_ex((ip, host_port))

    client_socket = Client((ip, host_port))


    # If connection was unsuccessful
    # if error != 0:
    #     #screen.addstr(error)
    #     #screen.refresh()
    #     print(error)
    #     screen.getch()
    #     client_socket.close()
    #     return

    screen.addstr(f"\t2. Waiting for host to start the game..\n\n")
    screen.refresh()

    # Listen for verification message from host
    host_msg = client_socket.recv().decode()
    screen.addstr(host_msg)
    screen.refresh()
    screen.clear()
    screen.refresh()

    # Start the online Game
    game = ClientGame(screen, client_socket)
    game.game_loop() # Loops until a player presses Q to quit the game session

    # One of the players has ended the online game session
    client_socket.close()
