import socket
import json
import curses
from screens.join_game import insert_IP


def joinGame(screen):
    curses.curs_set(0)
    ip = insert_IP(screen)

    # Setup socket and connect to host
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    error = client.connect_ex((ip, 8080))
    if error != 0:
        screen.addstr(error)
        screen.refresh()

    screen.addstr(f"\t2. Waiting for host to start the game..\n\n")
    screen.refresh()

    # Listen for verification message from host
    from_host = client.recv(4096).decode()
    print(from_host)
    screen.clear()
    screen.refresh()


    # Game loop
    while True:
        # Listen for message from host
        from_host = client.recv(4096).decode()
        print("from_host:\n" + from_host)
        if(from_host == "q"): # If host quit the current online game
            print("< leaving game >")
            break

        # Send message to host
        # msg = '{"id": "client", "board":  " + - - B B B - - +\n- - - - B - - - -\n- - - - W - - - -\nB - - - W - - - B\nB B W W K W W B B\nB - - - W - - - B\n- - - - W - - - -\n- - - - B - - - -\n+ - - B B B - - +"}'
        msg = "no its your turn:)"
        client.send(str.encode(msg))
        if(msg == "q"): # To quit the current online game
            print("< leaving game >")
            break


    client.close()
