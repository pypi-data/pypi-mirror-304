# Simple Color Prints
# -----------------------------------
def printgrey(input):
    print(f"\033[30m{input}\033[0m")

def printred(input):
    print(f"\033[31m{input}\033[0m")

def printgreen(input):
    print(f"\033[32m{input}\033[0m")

def printyellow(input):
    print(f"\033[33m{input}\033[0m")

def printorange(input):
    print(f"\033[38;2;255;165;0m{input}\033[0m")

def printblue(input):
    print(f"\033[34m{input}\033[0m")

def printpurple(input):
    print(f"\033[35m{input}\033[0m")

def printcyan(input):
    print(f"\033[36m{input}\033[0m")
# -----------------------------------


# Complex RGB Print
# -----------------------------------
#Used for the RGB Print, Although it just fixes a number to be Less than 255 and greater than 0. RGB values go from 0 - 255.
def colorBound(input):
    if input > 255:
        input = 255
    elif input < 0:
        input = 0
    return input

#Print in ANY RGB Value. Input a 0-255 RGB Color Code and then the string you want to print.
def printRGB(R,G,B,input):
    R = colorBound(R)
    G = colorBound(G)
    B = colorBound(B)
    print(f"\033[38;2;{R};{G};{B}m{input}\033[0m")
# -----------------------------------
