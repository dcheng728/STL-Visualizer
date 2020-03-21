from itertools import islice
from random import random
import time
import math
import random

pi = 3.14159265359
e = 2.7182818284590452353602874713527

def angle(point1, point2):
    d1 = math.sqrt(point1[0]**2+point1[1]**2+point1[2]**2)
    d2 = math.sqrt(point2[0]**2+point2[1]**2+point2[2]**2)

    point3 = [point2[0]-point1[0],point2[1]-point1[1],point2[2]-point1[2]]
    d3 = math.sqrt(point3[0]**2+point3[1]**2+point3[2]**2)

    thing = (d1*d1 + d2*d2 - d3*d3)/(2*d1*d2)
    if thing > 1:
        thing = 2-thing
    angle = math.acos(thing)
    return angle*180/pi

time_start=time.time()
for n in range(50000):
    angle([random.randint(0,1000),random.randint(0,1000),random.randint(0,1000)],[random.randint(0,1000),random.randint(0,1000),random.randint(0,1000)])
time_end=time.time()
print(time_end-time_start)

