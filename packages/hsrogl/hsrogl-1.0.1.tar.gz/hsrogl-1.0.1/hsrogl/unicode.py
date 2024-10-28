###############
# hsrogl.unicode          Make by H.S.S.
###############

"""
HSCDL License

不能开源、修改并上传发售！！！
"""

class ClassInfo():
    def main(self):
        return ["hsrogl.unicode","Make by H.S.S.","3582930858@qq.com","License: HSCDL","Cannot edit and update"]

def inttochr(digit:int):
    return chr(digit)
def hextochr(ahex:str):
    return chr(int(ahex,16))
def chrtohex(char:str):
    if len(char)!=1:
        raise ValueError("Input value must be a simple character")
    else:
        return hex(ord(char))
def chrtoint(char:str):
    if len(char)!=1:
        raise ValueError("Input value must be a simple character")
    else:
        a=str(hex(ord(char)))
        a=a.replace("0x","")
        return int(a,16)  
    