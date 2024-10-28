###############################
# hsrogl.bool     Make by H.S.S.
###############################

class ClassInfo():
    def main(self):
        return ["hsrogl.bool","Make by H.S.S.","3582930858@qq.com","License: HSCDL","Cannot edit and update"]

def bl_or(a,b):
    if a==True or b==True:
        return True
    else:
        return False
def bl_xor(a,b):
    if a==True and b==True:
        return False
    else:
        return True
def bl_and(a,b):
    if a==True and b==True:
        return True
    else:
        return False
def bl_xand(a,b):
    if a==True and b==True:
        return True
    else:
        return False

def bl_not(a):
    if a==True:
        return False
    else:
        return True

