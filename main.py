import time
import curses
from rendering.composition import handle_resize




def main(stdscr):
    try:
        curses.curs_set(0)      # hide cursor
    except curses.error:
        pass

    stdscr.nodelay(True)
    current_sect = 0
    handle_resize(stdscr, current_sect)
    

    while True:
        curses.doupdate()

        key = stdscr.getch()
        if key == -1: pass
        elif key == curses.KEY_RESIZE: 
            handle_resize(stdscr, current_sect)
        
        



        time.sleep(0.01)

    
    

if __name__ == "__main__":
    curses.wrapper(main)