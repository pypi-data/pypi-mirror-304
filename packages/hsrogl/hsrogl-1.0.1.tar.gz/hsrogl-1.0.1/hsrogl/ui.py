###############################
# hsrogl.ui     Make by H.S.S.
###############################


class ClassInfo():
    def main(self):
        return ["hsrogl.ui","Make by H.S.S.","3582930858@qq.com","License: HSCDL","Cannot edit and update"]

def Pause(tip:str=""):
    input(f"{tip}\033[8m")
    print("\033[0m")

def Pause_NoExpress(tip:str=""):
    input(f"{tip}")

def CheckSkill(value):
    if value==False:
        raise ValueError("Return error")
    else:
        return "Currect!"
        
def Select(data:list=["apple","banana"],
            puttext:str="? ",
            prompt:str=": ",
            cancelkey:str="cancel",
            keyformat:bool=True):
    if keyformat==True:
        a=""
        for i in data:
            a+=i
            a+="|"
        a+=cancelkey
        plat=f"({a})"
    else:
        plat=""
    stc=input(f"{puttext}{plat}{prompt}")
    for i in data:
        if stc==i:
            return stc
        else:
            pass
    if stc==cancelkey:
        return None
    else:
        return False
    
def InputSplit(value:str="",split:str=" ",times:int=-1):
    if times==-1:
        return value.split(split)
    else:
        return value.split(split,times)

def Loop(ranges:int=1):
    for i in range(ranges):
        print("",end="\n")

def _Msgbox(data,text):
    print(f"[] {data}: {text}")

def _Reportbox_id(errid:int=0,prompt:str=": Because",text:str=""):
    arg={
        1:"SYSTEM_ERROR",
        2:"ARGS_ERROR",
        3:"SELECT_ERROR",
        4:"SELECTION_ERROR",
        5:"FUNCTION_ERROR",
        6:"SELECT_ERROR",
        7:"PATH_ERROR",
        8:"COMMAND_ERROR",
        9:"ADDONS_ERROR",
        10:"FILES_ERROR",
        11:"LARGE_ERROR",
        12:"LOAD_ERROR",
        13:"LEXER_ERROR",
        0:"UNKNOWN_ERROR",
        1001:"TRUECOLOR_WARNING",
        1002:"LEXER_WARNING",
        1003:"SYSTEM_WARNING",
    }
    print(f"[] Report by {arg[errid]} {prompt} {text}")

def _Reportbox(errid:str="UNKNOWN_ERROR",prompt:str=": Because",text:str=""):
    print(f"[] Report by {errid} {prompt} {text}")

def Msg_Usage(text):
    _Msgbox("Usage",text)
def Msg_Content(text):
    _Msgbox("Content",text)
def Msg_Info(text):
    _Msgbox("Info",text)
def Msg_Warning(text):
    _Msgbox("Warning",text)
def Msg_Error(text):
    _Msgbox("Error",text)

def Flash(text,times=0.2):
    import time
    for i in range(len(text)):
        print(TextFormat.replace(TextFormat)+text[0:i])
        time.sleep(times)
class TextFormat():
    def replace(self):return "\033[r"
    def clear(self):return "\033[2J"
    def red(self):return "\033[31m"
    def green(self):return "\033[32m"
    def yellow(self):return "\033[33m"
    def blue(self):return "\033[34m"
    def magenta(self):return "\033[35m"
    def cyan(self):return "\033[36m"
    def white(self):return "\033[37m"
    def black(self):return "\033[30m"
    def bold(self):return "\033[1m"
    def underline(self):return "\033[4m"
    def italic(self):return "\033[3m"
    def blink(self):return "\033[5m"
    def reverse(self):return "\033[7m"
    def c2(self):return "\033[2m"
    def hidden(self):return "\033[8m"
    def c9(self):return "\033[9m"
    def reset(self):return "\033[0m"
    def c21(self):return "\033[21m"
    def c24(self):return "\033[24m"
    def c23(self):return "\033[23m"
    def c29(self):return "\033[29m"
    def c22(self):return "\033[22m"
    def red_back(self):return "\033[41m"
    def green_back(self):return "\033[42m"
    def yellow_back(self):return "\033[43m"
    def blue_back(self):return "\033[44m"
    def magenta_back(self):return "\033[45m"
    def cyan_back(self):return "\033[46m"
    def white_back(self):return "\033[47m"
    def black_back(self):return "\033[40m"
    def reset_back(self):return "\033[49m"
    def cursor_hide(self):return "\033[?25l"
    def cursor_show(self):return "\033[?25h"
    def fore_rgb(self,r,g,b):return f"\033[38;2;{r};{g};{b}m"
    def back_rgb(self,r,g,b):return f"\033[48;2;{r};{g};{b}m"

