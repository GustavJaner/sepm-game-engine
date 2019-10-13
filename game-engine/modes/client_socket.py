import socket
import pickle
import curses
from screens.join_game import insert_IP
from modes.client_game import ClientGame


HEADERSIZE = 10


def client_socket(screen):
    curses.curs_set(0)
    ip = insert_IP(screen)

    # Setup socket and connect to host
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    error = client_socket.connect_ex((ip, 8080))

    # If connection was unsuccessful
    if error != 0:
        screen.addstr(error)
        screen.refresh()
        client_socket.close()
        return

    screen.addstr(f"\t2. Waiting for host to start the game..\n\n")
    screen.refresh()

    # Listen for verification message from host
    host_msg = client_socket.recv(4096).decode()
    screen.addstr(host_msg)
    screen.refresh()
    screen.clear()
    screen.refresh()

    # Start the online Game
    game = ClientGame(screen, client_socket)
    game.game_loop() # Loops until a player presses Q to quit the game session

    # One of the players has ended the online game session
    client_socket.close()
        #
        # full_msg = b''
        # new_msg = True
        # while True:
        #     msg = client_socket.recv(16)
        #     if new_msg:
        #         print("new msg len:",msg[:HEADERSIZE])
        #         msglen = int(msg[:HEADERSIZE])
        #         new_msg = False
        #
        #     print(f"full message length: {msglen}")
        #
        #     full_msg += msg
        #
        #     print(len(full_msg))
        #
        #     if len(full_msg)-HEADERSIZE == msglen:
        #         print("full msg recvd")
        #         print(full_msg[HEADERSIZE:])
        #         print(pickle.loads(full_msg[HEADERSIZE:]))
        #         new_msg = True
        #         full_msg = b""


        # Send message to host
        # msg = '{"id": "client_socket", "board":  " + - - B B B - - +\n- - - - B - - - -\n- - - - W - - - -\nB - - - W - - - B\nB B W W K W W B B\nB - - - W - - - B\n- - - - W - - - -\n- - - - B - - - -\n+ - - B B B - - +"}'
        # msg = "no its your turn:)"
        # client_socket.send(str.encode(msg))
        # if(msg == "q"): # To quit the current online game
        #     print("< leaving game >")
        #     break
