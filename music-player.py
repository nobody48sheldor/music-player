import curses
import os
from concurrent.futures import ProcessPoolExecutor
import time

executor = ProcessPoolExecutor(max_workers=4)

stdscr = curses.initscr()


Y, X = stdscr.getmaxyx()
x = 0
y = 0
menu = 0
mode = "move"

curses.start_color()
curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
red = curses.color_pair(1)
yellow = curses.color_pair(2)

def draw_menu(y):
    stdscr.addstr(int(Y/20), int(X/12), "MENU", curses.A_BOLD)
    if x == 0:
        if y == 0:
           stdscr.addstr(int(Y/20) + int(Y/10), int(X/16), " - music", red)
        else:
           stdscr.addstr(int(Y/20) + int(Y/10), int(X/16), " - music")
        if y == 1:
            stdscr.addstr(int(Y/20) + int(Y/10) + 2, int(X/16), " - playlist", red)
        else:
            stdscr.addstr(int(Y/20) + int(Y/10) + 2, int(X/16), " - playlist")
        if y == 2:
            stdscr.addstr(int(Y/20) + int(Y/10) + 4, int(X/16), " - download", red)
        else:
            stdscr.addstr(int(Y/20) + int(Y/10) + 4, int(X/16), " - download")
        if y == 3:
            stdscr.addstr(int(Y/20) + int(Y/10) + 6, int(X/16), " - settings", red)
        else: 
            stdscr.addstr(int(Y/20) + int(Y/10) + 6, int(X/16), " - settings")
        if y == 4:
            stdscr.addstr(int(Y/20) + int(Y/10) + 8, int(X/16), " - quit", red)
        else:
            stdscr.addstr(int(Y/20) + int(Y/10) + 8, int(X/16), " - quit")
    elif menu == 0:
        stdscr.addstr(int(Y/20) + int(Y/10), int(X/16), " - music", yellow)
        stdscr.addstr(int(Y/20) + int(Y/10) + 2, int(X/16), " - playlist")
        stdscr.addstr(int(Y/20) + int(Y/10) + 4, int(X/16), " - download")
        stdscr.addstr(int(Y/20) + int(Y/10) + 6, int(X/16), " - settings")
        stdscr.addstr(int(Y/20) + int(Y/10) + 8, int(X/16), " - quit")
    elif menu == 2:
        stdscr.addstr(int(Y/20) + int(Y/10), int(X/16), " - music")
        stdscr.addstr(int(Y/20) + int(Y/10) + 2, int(X/16), " - playlist")
        stdscr.addstr(int(Y/20) + int(Y/10) + 4, int(X/16), " - download", yellow)
        stdscr.addstr(int(Y/20) + int(Y/10) + 6, int(X/16), " - settings")
        stdscr.addstr(int(Y/20) + int(Y/10) + 8, int(X/16), " - quit")


def draw_music(musics, y):
    for i in range(len(musics)):
        if i == y:
            stdscr.addstr(int(Y/12) + 2*i, int(X/3), str(musics[i]), red)
        else:
            stdscr.addstr(int(Y/12) + 2*i, int(X/3), str(musics[i]))

def draw_info(music):
    pass

def draw_download():
    pass

def draw_search():
    stdscr.addstr(int(Y/8), int(X/2), "search : ", yellow)
    stdscr.refresh()
    search = ""
    c = ''
    while c != "\n":
        c = stdscr.getkey()
        search = search + c
        stdscr.addstr(int(Y/8), int(X/2), "search : ", yellow)
        stdscr.addstr(search, red)
        stdscr.refresh()
    return(search)

def search(query):
    os.chdir("music")
    stdscr.clear()
    stdscr.refresh()
    os.system('youtube-dl -x --audio-quality 0 --restrict-filename "ytsearch:{}" '.format(query))
    os.chdir("..")

draw_menu(y)
stdscr.refresh()

while True:
    key = ""
    musics = os.listdir("./music")

    if x == 0:
        ymax = 3
    elif x == 1:
        if y == 0:
            ymax = len(musics) - 2

    key = stdscr.getkey()
    if mode == "move":
        if key == "k":
            if y > 0:
                y = y - 1
        elif key == "j":
            if y <= ymax:
                y = y + 1
        elif key == "q":
            quit()

    stdscr.clear()
    draw_menu(y)

    if x == 1:
        if menu == 0:
            draw_music(musics, y)
            if key == "h":
                x = 0
                y = 0
                stdscr.clear()
                draw_menu(y)
            if key == "l":
                stdscr.clear()
                executor.submit(os.system, "alacritty -e mpv --no-video ./music/{} &".format(musics[y]))
                draw_info(musics[y])
        if menu == 2:
            if key == "h":
                x = 0
                y = 2
                stdscr.clear()
                draw_menu(y)
            if key == "s":
                mode = "search"
                query = draw_search()
                mode = "move"
                stdscr.refresh()
                search(query)
                x = 0
                y = 2

    if x == 0:
        if y == 0:
            if key == "l":
                menu = 0
                x = 1
                draw_menu(y)
                draw_music(musics, y)
        if y == 1:
            pass
        if y == 2:
            if key == "l":
                menu = 2
                x = 1
                draw_menu(y)
                draw_download()
                stdscr.addstr(int(Y/12), int(X/2), "press 's' to search")
                stdscr.addstr(int(Y/8), int(X/2), "search : ")
                stdscr.refresh()
        if y == 3:
            pass
        if y == 4:
            if key == "l":
                quit()

    stdscr.refresh()
