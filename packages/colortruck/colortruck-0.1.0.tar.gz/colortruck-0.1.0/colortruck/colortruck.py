import os
import ctypes

class Truckcolors:
    def __init__(self):
        self.BLACK="\033[30m"
        self.RED = "\033[31m"
        self.GREEN = "\033[32m"
        self.YELLOW = "\033[33m"
        self.BLUE = "\033[34m"
        self.PURPLE="\033[35m"
        self.LIGHT_BLUE="\033[36m"
        self.GREY="\033[37m"
        self.DARK="\033[90m"
        self.DARK_RED="\033[91m"
        self.DARK_GREEN="\033[92m"
        self.DARK_YELLOW="\033[93m"
        self.DARK_BLUE="\033[94m"
        self.DARK_PURPLE="\033[95m"
        self.DARK_LIGHT_BLUE="\033[96m"
        self.DARK_WHITE="\033[97m"
        self.BG_BLACK="\033[40m"
        self.BG_RED="\033[41m"
        self.BG_GREEN="\033[42m"
        self.BG_YELLOW="\033[43m"
        self.BG_BLUE="\033[44m"
        self.BG_PURPLE="\033[45m"
        self.BG_LIGH_BLUE="\033[46m"
        self.BG_WHITE="\033[47m"
        self.RESET = "\033[0m"
        self.BOLD="\033[1m"
        self.LIGHT_PRINT="\033[2m"
        self.UDERLINE="\033[4m"
        self.CROSSOUT="\033[9m"
    def exe_cover(self):
        if os.name == 'nt':
            try:
                kernel32 = ctypes.windll.kernel32
                handle = kernel32.GetStdHandle(-11)
                mode = ctypes.c_uint()
                kernel32.GetConsoleMode(handle, ctypes.byref(mode))
                kernel32.SetConsoleMode(handle, mode.value | 0x0001 | 0x0004)
            except:
                pass

