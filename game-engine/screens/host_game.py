import curses


def waiting_for_other_player(screen, serv):
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
        screen.addstr("1. Successfully created a new game server")
        screen.addstr("\n\t  ")
        screen.addstr("2. Waiting for another player to join the game..")
        screen.addstr("\n\t  ")
        screen.refresh()

        conn, addr = serv.accept()
        screen.addstr("3. Another player has joined your game!\n")
        screen.refresh()

        screen.addstr(f"\n\n\n\t-------------- Press any key to start --------------\n\n")
        screen.getch()

        screen.clear()
        screen.refresh()

        return conn, addr
