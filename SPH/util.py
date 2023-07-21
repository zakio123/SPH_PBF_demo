import math
from const import *
def kernel(c,r1,r2):
    dist = distance(r1,r2)
    if (dist < h_2) :
        return c * math.pow(h_2 - dist,3)
    else :
        return 0
    
def distance(r1,r2):
    r = r1 - r2
    r = 100 * r 
    d = r[0] * r[0] + r[1] * r[1] + r[2] * r[2]#np.linalg.norm(r1-r2, ord=2)
    d = d / 10000
    return d