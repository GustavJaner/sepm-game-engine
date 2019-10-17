import curses


def waiting_for_other_player(screen, serv, host_ip):
    screen.clear()
    screen.scrollok(1)

    while True:

        screen.addstr("""
         _   _  _   _          ____     _     __  __  _____
        | | | || | | |        / ___|   / \   |  \/  || ____|
        | | | || | | | _____ | |  _   / _ \  | |\/| ||  _|
        | |_| || |_| ||_____|| |_| | / ___ \ | |  | || |___
         \___/  \___/         \____|/_/   \_\|_|  |_||_____|

        ====================================================
        """)

        screen.addstr("\n\n\t\t\t  ")
        screen.addstr("Play online", curses.A_BOLD)
        screen.refresh()

        screen.addstr("\n\n\n\t  ")
        screen.addstr(f"1. Successfully created a new game server with IP address:\n\t     {host_ip}")
        screen.addstr("\n\n\t  ")
        screen.addstr("2. Waiting for another player to join the game..")
        screen.addstr("\n\n\t  ")
        screen.refresh()

        client_socket = serv.accept()
        screen.addstr(f"3. Another player has joined your game!\n")
        # screen.addstr(f"3. Another player has joined your game with IP address:\n\t     {client_ip}")
        screen.refresh()

        screen.addstr(f"\n\n\n\t-------------- Press any key to start --------------\n\n")
        screen.getch()

        screen.clear()
        screen.refresh()

        return client_socket
