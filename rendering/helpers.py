import curses

def safe_addstr(win, y, x, s):
    h, w = win.getmaxyx()
    if y < 0 or y >= h or x >= w:
        return
    if x < 0:
        s, x = s[-x:], 0
    s = s[: w - x]
    try:
        win.addstr(y, x, s)
    except curses.error:
        pass

def draw_transparent(win, y, x, line):
    for dx, ch in enumerate(line):
        if ch != " ":
            safe_addstr(win, y, x + dx, ch)