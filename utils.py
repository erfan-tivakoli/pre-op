import numpy as np

def distance_to_line(x1, y1, x2, y2, x3, y3):
    #compute distance from (x3, y3) to line going through (x1,y1) and (x2, y2)

    p1 = np.asarray((x1, y1))
    p2 = np.asarray((x2, y2))
    p3 = np.asarray((x3,y3))
    d = np.linalg.norm(np.cross(p2-p1, p1-p3))/np.linalg.norm(p2-p1)
    return d
