from colorama import Fore, init
import win32api
import cmath
import math
import os

class Console:
    def __init__(self):
        self = self
    
    def print(text, color, justify):
        init()

        if color == None:
            color = ''
        if color == 'red':
            color = Fore.RED

        if justify == None:
            print(color+text)

        if justify == 'center':
            x = 120/2 - len(text) / 2
            print(int(x) * ' '+str(color+text))

# Math Functions
def area(length, width):
    return length * width

def bmi(weight_lb, height_feet):
    inches = height_feet * 12
    return weight_lb / inches**2 * 703

def cos(angle):
    return math.cos(angle)

def distance(x1, x2, y1, y2):
    return math.sqrt((x2-x1)**2+(y2-y1)**2)

def expgrowth(start, rate, time):
    if rate > 0:
        return start * (1+rate/100)**time
    if rate < 0:
        return start * (1-rate*100)**time

def time(distance, speed):
    return distance/speed

def midpoint(x1, x2, y1, y2):
    return [x1+x2/2, y1+y2/2]

def quadratic(a, b, c):
    w = (b**2) - (4*a*c)
    sol1 = (-b-cmath.sqrt(w))/(2*a)
    sol2 = (-b+cmath.sqrt(w))/(2*a)
    return sol1, sol2

def volume(length, width, height):
    return length * width * height

# PC Functions
def fps():
    return win32api.EnumDisplaySettings(None, 0).DisplayFrequency

def username():
    return os.getlogin()

def mousePos():
    return win32api.GetCursorPos()[0], win32api.GetCursorPos()[1]