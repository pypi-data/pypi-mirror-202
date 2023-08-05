import sys
import time
import random
import simple_colors
import pydoc

def help():
    try:
        print(simple_colors.red("Help at pypi.org website in description"))
    except:
        print("-HELP - Something failed")
def red(input):
    try:
        print(simple_colors.red(input))
    except:
        print("-RED - Something failed")

def green(input):
    try:
        print(simple_colors.green(input))
    except:
        print("-GREEN - Something failed")

def blue(input):
    try:
        print(simple_colors.blue(input))
    except:
        print("-BLUE - Something failed")

def black(input):
    try:
        print(simple_colors.black(input))
    except:
        print("-BLACK - Something failed")


def yellow(input):
    try:
        print(simple_colors.yellow(input))
    except:
        print("-YELLOW - Something failed")


def magenta(input):
    try:
        print(simple_colors.magenta(input))
    except:
        print("-MAGENTA - Something failed")


def cyan(input):
    try:
        print(simple_colors.cyan(input))
    except:
        print("-CYAN - Something failed")

