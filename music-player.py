import curses
import os
from concurrent.futures import ProcessPoolExecutor
import time
import json

executor = ProcessPoolExecutor(max_workers=4)

stdscr = curses.initscr()


Y, X = stdscr.getmaxyx()
x = 0
y = 0
d = 0
menu = 0
mode = "move"

curses.start_color()
curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
red = curses.color_pair(1)
yellow = curses.color_pair(2)

def draw_menu(y):
    Y, X = stdscr.getmaxyx()
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
    elif menu == 1:
        stdscr.addstr(int(Y/20) + int(Y/10), int(X/16), " - music")
        stdscr.addstr(int(Y/20) + int(Y/10) + 2, int(X/16), " - playlist", yellow)
        stdscr.addstr(int(Y/20) + int(Y/10) + 4, int(X/16), " - download")
        stdscr.addstr(int(Y/20) + int(Y/10) + 6, int(X/16), " - settings")
        stdscr.addstr(int(Y/20) + int(Y/10) + 8, int(X/16), " - quit")
    elif menu == 2:
        stdscr.addstr(int(Y/20) + int(Y/10), int(X/16), " - music")
        stdscr.addstr(int(Y/20) + int(Y/10) + 2, int(X/16), " - playlist")
        stdscr.addstr(int(Y/20) + int(Y/10) + 4, int(X/16), " - download", yellow)
        stdscr.addstr(int(Y/20) + int(Y/10) + 6, int(X/16), " - settings")
        stdscr.addstr(int(Y/20) + int(Y/10) + 8, int(X/16), " - quit")

def draw_music(musics, y, d):
    Y, X = stdscr.getmaxyx()
    ymax = int(Y/2 - 1)
    for i in range(ymax - 1):
        if i < len(musics) - d:
            if y <= 1:
                if d >= 1:
                    d = d - 1
                    y =  y + 1
            if y >= ymax - 2:
                d = d + 1
                y =  y - 1
            if i == y:
                stdscr.addstr(int(Y/12) + 2*i, int(X/3), str(musics[i+d]), red)
            else:
                stdscr.addstr(int(Y/12) + 2*i, int(X/3), str(musics[i+d]))

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

def draw_filename():
    stdscr.addstr(int(Y/8), int(X/2), "playlist name : ", yellow)
    stdscr.refresh()
    search = ""
    c = ''
    while c != "\n":
        c = stdscr.getkey()
        search = search + c
        stdscr.addstr(int(Y/8), int(X/2), "playlist name : ", yellow)
        stdscr.addstr(search, red)
        stdscr.refresh()
    stdscr.clear()
    playlists = os.listdir("./playlist")
    draw_menu(y)
    draw_playlist(musics, playlists, y)
    stdscr.refresh()
    return(search)

def draw_playlist(musics, playlists, y):
    Y, X = stdscr.getmaxyx()
    for i in range(len(playlists)):
        if i < int(Y/2 - 1):
            if i == y:
                stdscr.addstr(int(Y/12) + 2*i, int(X/3), str(playlists[i]), red)
            else:
                stdscr.addstr(int(Y/12) + 2*i, int(X/3), str(playlists[i]))
    with open("playlist/{}".format(playlists[y], "r")) as f:
        songs = f.readlines()
        for i in range(len(songs)):
            if i < int(Y/2 - 1):
                songs[i] = songs[i][:-1]
                stdscr.addstr(int(Y/12) + 2*i, int(X/2), str(songs[i]))


def draw_playlists_maker(musics, y, filename):
    stdscr.clear()
    draw_menu(y)
    for i in range(len(musics)):
        if i == y:
            stdscr.addstr(int(Y/12) + 2*i, int(X/4), str(musics[i]), red)
        else:
            stdscr.addstr(int(Y/12) + 2*i, int(X/4), str(musics[i]))
    stdscr.refresh()
    key = ""
    ymax = len(musics) - 2
    y = 0
    playlist = []
    while key != "\n":
        key = stdscr.getkey()
        stdscr.clear()
        draw_menu(y)
        if key == "k":
            if y > 0:
                y = y - 1
        elif key == "j":
            if y <= ymax:
                y = y + 1
        elif key == "q":
            quit()
        
        if key == "l":
            playlist.append(musics[y])

        for i in range(len(musics)):
            if i == y:
                stdscr.addstr(int(Y/12) + 2*i, int(X/4), str(musics[i]), red)
            else:
                stdscr.addstr(int(Y/12) + 2*i, int(X/4), str(musics[i]))
        for i in range(len(playlist)):
            stdscr.addstr(int(Y/12) + 2*i, int(X/1.5), str(playlist[i]))
        stdscr.refresh()
    with open('playlist/{}.json'.format(filename[:-1]), 'w') as f:
        for i in playlist:
            f.write(i + "\n")

def draw_edit(playlist, musics):
    songs = []
    with open('playlist/{}'.format(playlist), 'r') as f:
        songs = f.readlines()
    for i in  range(len(songs)):
        songs[i] = songs[i][:-1]
    stdscr.refresh()
    key = ""
    y = 0
    while key != "\n":
        stdscr.clear()
        draw_menu(y)
        for i in range(len(songs)):
            if y == i:
                stdscr.addstr(int(Y/12) + 2*i, int(X/3), str(songs[i]), red)
            else:
                stdscr.addstr(int(Y/12) + 2*i, int(X/3), str(songs[i]))
        key = stdscr.getkey()
        if key == "j":
            if y < len(songs) - 1:
                y = y + 1
        if key == "k":
            if y > 0:
                y = y - 1
        if key == "l":
            song = songs[y]
            stdscr.clear()
            draw_menu(y)
            stdscr.addstr(int(Y/12) + 2*y, int(2*X/3), str(song))
            for i in range(len(songs) - (y + 1)):
                songs[y + i] = songs[y + i + 1]
            songs.pop(len(songs) - 1)
            for i in range(len(songs)):
                stdscr.addstr(int(Y/12) + 2*i, int(X/3), str(songs[i]))
            while True:
                key = stdscr.getkey()
                stdscr.clear()
                draw_menu(y)
                if key == "j":
                    if y < len(songs):
                        y = y + 1
                if key == "k":
                    if y > 0:
                        y = y - 1
                if key == "h":
                    songs.append(songs[len(songs) - 1])
                    for i in range(len(songs) - (y+1)):
                        songs[len(songs) - (i+1)] = songs[len(songs) - (i+2)]
                    songs[y] = song
                    key = ""
                    break
                stdscr.addstr(int(Y/12) + 2*y, int(2*X/3), str(song))
                for i in range(len(songs)):
                    stdscr.addstr(int(Y/12) + 2*i, int(X/3), str(songs[i]))
        if key == "+":
            y = 0
            stdscr.clear()
            draw_menu(y)
            for i in range(len(musics)):
                if y == i:
                    stdscr.addstr(int(Y/12) + 2*i, int(X/3), str(musics[i]), red)
                else:
                    stdscr.addstr(int(Y/12) + 2*i, int(X/3), str(musics[i]))
            while key != "\n":
                key = stdscr.getkey()
                if key == "j":
                    if y < len(musics) - 1:
                        y = y + 1
                if key == "k":
                    if y > 0:
                        y = y - 1
                if key == "h":
                    y = 0
                    stdscr.clear()
                    draw_menu(y)
                    break
                for i in range(len(musics)):
                    if y == i:
                        stdscr.addstr(int(Y/12) + 2*i, int(X/3), str(musics[i]), red)
                    else:
                        stdscr.addstr(int(Y/12) + 2*i, int(X/3), str(musics[i]))
                stdscr.refresh()
            songs.append(musics[y])
            key = ""
            y = 0

        if key == "d":
            for i in range(len(songs) - (y + 1)):
                songs[y + i] = songs[y + i + 1]
            songs.pop(len(songs) - 1)
        if key == "h":
            stdscr.clear()
            draw_menu(y)
            y = 0
            draw_playlist(musics, playlists, y)
            stdscr.refresh()
            break
        if key == "q":
            quit()
        stdscr.refresh()
    with open('playlist/{}'.format(playlist), 'w') as f:
        for i in songs:
            f.write(i + "\n")

def search(query):
    stdscr.clear()
    stdscr.refresh()
    executor.submit(os.system, "cd music && alacritty -e youtube-dl -x --audio-quality 0 --restrict-filename 'ytsearch:{}' && cd .. &".format(query))

def play(playlist):
    cmd = "alacritty -e mpv "
    with open('playlist/{}'.format(playlist), 'r') as f:
        playing = f.readlines()
    for i in  range(len(playing)):
        playing[i] = playing[i][:-1]
    for i in range(len(playing)):
            cmd = cmd + "./music/" + playing[i] + " "
    executor.submit(os.system, cmd)

draw_menu(y)
stdscr.refresh()

while True:
    Y, X = stdscr.getmaxyx()
    key = ""
    musics = os.listdir("./music")
    playlists = os.listdir("./playlist")

    if x == 0:
        ymax = 3
    if x == 1:
        if menu == 0:
            ymax = len(musics) - 2
        elif menu == 1:
            ymax = len(playlists) - 2

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
            stdscr.clear()
            draw_menu(0)
            draw_music(musics, y, d)
            if key == "h":
                x = 0
                y = 0
                d = 0
                stdscr.clear()
                draw_menu(y)
            if key == "l":
                stdscr.clear()
                executor.submit(os.system, "alacritty -e mpv ./music/{} &".format(musics[y]))
                draw_info(musics[y])
            if key == "d":
                os.remove("music/{}".format(musics[y]))
                y = 0
                stdscr.clear()
                playlists = os.listdir("./playlist")
                musics = os.listdir("./music")
                draw_menu(y)
                draw_music(musics, y, d)
                stdscr.refresh()

        if menu == 1:
            draw_playlist(musics, playlists, y)
            if key == "h":
                x = 0
                y = 1
                stdscr.clear()
                draw_menu(y)
            if key == "l":
                play(playlists[y])
            if key == "n":
                stdscr.clear()
                draw_menu(y)
                stdscr.refresh()

                filename = draw_filename()

                draw_playlists_maker(musics, y, filename)
                draw_menu(y)
                stdscr.refresh()
                stdscr.clear()
                playlists = os.listdir("./playlist")
                draw_menu(y)
                stdscr.refresh()
            if key == "e":
                stdscr.clear()
                draw_menu(y)
                draw_edit(playlists[y], musics)
                stdscr.clear()
                draw_menu(y)
                draw_playlist(musics, playlists, y)
                stdscr.refresh()
            if key == "d":
                os.remove("playlist/{}".format(playlists[y]))
                y = 0
                stdscr.clear()
                playlists = os.listdir("./playlist")
                draw_menu(y)
                draw_playlist(musics, playlists, y)
                stdscr.refresh()
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
                d = 0
                draw_menu(y)
                draw_music(musics, y, d)
        if y == 1:
            if key == "l":
                menu = 1
                x = 1
                y = 0
                draw_menu(y)
                draw_playlist(musics, playlists, y)
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
