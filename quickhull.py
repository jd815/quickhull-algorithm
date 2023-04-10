import math
def quickhull(v):
    #Calculating the convex hull of a set of variables v
    #param v: set of coordinates(x,y) x and y should be floats
    #return: set of coordinates(x,y) which are the nodes of the convex hull

    #return v if there are only two coordinates
    if len(v) <= 2:
        return v
    convex_hull = []

    #finding the min and max points of x
    sort = sorted(v, key=lambda x: x[0])
    p1 = sort[0]
    p2 = sort[-1]

    convex_hull = convex_hull + [p1, p2]

    #removing the points from the list since they have already been added
    sort.pop(0)
    sort.pop(-1)

    #sorting points above and below the line
    above, below = create_segment(p1, p2, sort)
    convex_hull = convex_hull + quickhull2(p1, p2, above, "above")
    convex_hull = convex_hull + quickhull2(p1, p2, below, "below")

    return convex_hull

def quickhull2 (p1, p2, segment, flag):
    #param p1: first coordinate on the line
    #param p2: second coordinate on the line
    #param segment: rest of the points in the segment
    #param flag: String saying above or below
    
    #exit case for recursion
    if segment == [] or p1 is None or p2 is None:
        return []

    convex_hull = []

    #calculating the distance of every point from the line to find the farthest point
    farthest_distance = -1
    farthest_point = None
    for point in segment:
        distance = find_distance(p1, p2, point)
        if distance > farthest_distance:
            farthest_distance = distance
            farthest_point = point

    convex_hull = convex_hull + [farthest_point]

    #point is now in the convex hull so remove it from segment
    segment.remove(farthest_point)

    #determine the segments formed from two lines p1-farthest_point and p2-farthest_point
    point1above, point1below = create_segment(p1, farthest_point, segment)
    point2above, point2below = create_segment(p2, farthest_point, segment)

    #only use the segments in the same direction, the opposite direction is contained in the covnex hull
    if flag == "above":
        convex_hull = convex_hull + quickhull2(p1, farthest_point, point1above, "above")
        convex_hull = convex_hull + quickhull2(farthest_point, p2, point2above, "above")
        
    else:
        convex_hull = convex_hull + quickhull2(p1, farthest_point, point1below, "below")
        convex_hull = convex_hull + quickhull2(farthest_point, p2, point2below, "below")

    return convex_hull

def create_segment(p1, p2, v):
    #segment a set of coordinates to be below a line p1-p2
    #param p1: first coordinate on the line
    #param p2: second coordinate on the line
    #param v: list of coordinates represented by tuples (x,y)

    above = []
    below = []

    #line vertical so there are no points above or below it
    if p2[0] - p1[0] == 0:
        return above, below

    #calculate m and c from y=mx +c
    #m = y2-y1 / x2-x1
    #c = y-mx
    m = (p2[1] - p1[1]) / (p2[0] - p1[0])
    c = p1[1] - m * p1[0]

    #loop through each coordinate and place it into the correct list

    for coordinate in v:
        #y > mx + c means it is above the line
        if coordinate[1] > m*(coordinate[0]) + c:
            above.append(coordinate)
        elif coordinate[1] < m*(coordinate[0]) + c:
            below.append(coordinate)

    return above, below

def find_distance (p1, p2, p3):
    #Find the distance between a line p1-p2 and a point p3
    #param p1: the first coordinate on the line
    #param p2: the second coordinate on the line
    #param p3: the point to measure the distance from
    #return: the distance between the line and the point

    #using ax + by + c = 0
    a = p1[1] - p2[1]
    b = p2[0] - p1[0]
    c = p1[0]*p2[1] - p2[0]*p1[1]

    #formula for distance of a point from the line
    return abs(a*p3[0] + b*p3[1] + c)/math.sqrt(a*a + b*b)
