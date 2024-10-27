import math
def  parallelogram(b,h):
    return 2*(b+h)
def triangle(a,b,c):
    return a + b + c	
def rectangle(a,b):
    return 2*(a+b)
def square(a):
    return 4*a
def trapezoid(a,b,c,d):
    return a + b + c + d	
def kite(a,b):
    p=2*a + 2*b
    return p
def rhombus(a):
    return 4 * a	
def hexagon(a):
    return 6 *a
def circle(r):
    return 2*3.14*r
def ellipse(r1,r2):
    r=(r1**2+r2**2)/2
    return 2*math.pi*math.sqrt(r)
def regular_polygon(a,b):
    return a*b

