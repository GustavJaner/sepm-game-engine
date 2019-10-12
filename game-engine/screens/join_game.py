import curses


def insert_IP(screen):
    screen.clear()
    screen.scrollok(1)

    ip = ""

    underscores = "_" * 50
    selected = 1

    while True:
        curses.curs_set(0)
        screen.clear()

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

        screen.addstr(f"\n\n\n\tInsert the IP address of the game you want to join:\n")

        str2print = ip.ljust(50, "_")

        screen.addstr(f"\n\t{str2print}\n")

        if selected >= 2:
            screen.addstr(f"\n\n\n\tConnecting to the game with IP address:\n\t{ip}\n\n")
            screen.refresh()

            return ip

        ch = screen.getch()

        # Delete key
        if ch == 127:
            ip = ip[:-1]

        # New line
        elif ch == 10:
            if ip != "":
                selected += 1

        # Any other char will be concatenated
        else:
            if len(ip) < 50:
                ip += chr(ch)
