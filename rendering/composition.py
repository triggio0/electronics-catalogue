import curses
import tomllib
from pathlib import Path
from .helpers import safe_addstr, draw_transparent

ART_PATH = Path(__file__).resolve().parent.parent / "graphics" / "book_art.toml"
SECTIONS = ["res", "cap", "ind", "dio", "led", "bjt", "msf", "rly", "fus", "pot", "msc"]

MIN_BOOK_H = 10
MIN_BOOK_W = 10

def handle_resize(stdscr, current_sect):
    std_h, std_w = stdscr.getmaxyx()
    UPPER_BORDER, LOWER_BORDER, SIDES_BORDER = (4, 3, 5)
    book_h, book_w = (std_h - (UPPER_BORDER + LOWER_BORDER), std_w - 2*SIDES_BORDER)
    book_y, book_x = (UPPER_BORDER, SIDES_BORDER)
    if book_w % 2 == 1: book_w -=1
    if book_h < MIN_BOOK_H: invalid_size(stdscr)
    if book_w < MIN_BOOK_W: invalid_size(stdscr)
    book_win = curses.newwin(book_h, book_w, book_y, book_x)
    compose_book(book_win)
    
    tabs_h, tabs_w = (book_h - 2 - 5, 6) # set tabs_w =5 for 3 tabs, =6 for 4
    tabs_y, tabs_x = (2, book_w - tabs_w ) # relative to book
    tabs_win = book_win.derwin(tabs_h, tabs_w, tabs_y, tabs_x)
    compose_tabs(tabs_win, current_sect)

    stdscr.clear()
    stdscr.noutrefresh()
    
    book_win.noutrefresh()
    tabs_win.noutrefresh()



def invalid_size(stdscr):
    safe_addstr(stdscr, 0, 0, "Terminal too small")
    stdscr.noutrefresh()

def load_book_art():
    with open(ART_PATH, "rb") as f:
            return tomllib.load(f)
BOOK_ART = load_book_art()

def compose_book(win: curses.window):
    win_height, win_width = win.getmaxyx()
    win_width -= 1 # remove this line if 3 tabs are being used
    if win_width%2 == 0:
        raise Exception("book width not valid!")

    for i in range(4):
        safe_addstr(win, win_height - i - 2, 0, f"{'─'*win_width}")
    safe_addstr(win, 0, 0, f"{'─'*win_width}")
    for h in range(win_height-1):
        safe_addstr(win, h, win_width//2, '│')
        for i in range(5):
            safe_addstr(win, h, i, '│')
            safe_addstr(win, h, win_width - i - 1, '│')

    for el, data in BOOK_ART.items():
        start = (0, 0)
        lines = data["text"].splitlines()
        w, h = (len(lines[0]), len(lines))
        match el:
            case "tl": start = (0, 0)
            case "tc": start = (0, (win_width - w) // 2)
            case "tr": start = (0, win_width - w)
            case "bl": start = (win_height - h, 0)
            case "bc": start = (win_height - h, (win_width - w) // 2)
            case "br": start = (win_height - h, win_width - w)
            case _: continue
        for i, line in enumerate(lines):
            safe_addstr(win, start[0] + i, start[1], line)
            # todo: add color


def load_tab_art():
    with open(ART_PATH, "rb") as f:
        return tomllib.load(f)["tab"]["text"].splitlines()
TAB_LINES = load_tab_art()

def compose_tabs(win: curses.window, current_sect: int):
    MAX_VISIBLE = 4
    n = len(SECTIONS)
    if not 0 <= current_sect < n:
        raise ValueError(f"compose_tabs: invalid current_sect {current_sect}")

    win_height, _ = win.getmaxyx()
    full_h = len(TAB_LINES)
    pitch = full_h - 1
    displayed = min(MAX_VISIBLE, n - current_sect)

    R = max(0, win_height - full_h - (MAX_VISIBLE - 1) * pitch)
    m = n - MAX_VISIBLE
    if m > 0:
        s = min(pitch, R / m) # realistic if tall, spread if short
        top = s * min(current_sect, m) + pitch * max(0, current_sect - m)
    else:
        top = pitch * current_sect
    top = round(top)

    top = max(0, min(top, win_height - full_h - (displayed - 1) * pitch))

    for i in range(displayed - 1, -1, -1):
        y, x = top + i * pitch, i
        for row, line in enumerate(TAB_LINES):
            safe_addstr(win, y + row, x, line)

        label = SECTIONS[current_sect + i]
        for row, ch in enumerate(label):
            safe_addstr(win, y + 1 + row, x + 1, ch)

