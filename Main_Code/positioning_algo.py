from math import atan, sqrt, acos, pi

# dot product of two vectors
def dot_poduct(a, b):
        return ((a[0] * b[0]) + (a[1] * b[1]))

# get the modulus of a vector
def modulus(a):
        return sqrt(pow(a[0],2) + pow(a[1], 2))

# angle between two vectors
def angle(a, b):
        return acos(abs(dot_poduct(a,b) / (modulus(a) * modulus(b)))) 

# distance between two points
def distance(p0, p1):
        return sqrt(pow(p0[1] - p1[1], 2) + pow(p0[0] - p1[0], 2))

# function to calculate the turning angles
def positions(start_pos, head_pos, end_pos, end_angle):
        # points and vectors are in the diagram
        x0, y0 = start_pos[0], start_pos[1]
        xd, yd = end_pos[0], end_pos[1]
        xfl, yfl = head_pos[0][0], head_pos[0][1]
        xfr, yfr = head_pos[1][0], head_pos[1][1]
        xd, yd = end_pos[0], end_pos[1]
        xf, yf = (xfr + xfl) / 2, (yfr + yfl) / 2

        a = [xd - x0, yd - y0]
        b = [xf - x0, yf - y0]

        # calculating the angle between vector a and vector b
        angle_s = angle(a, b)
        angle_m = pi - angle_s

        # definig vector c and vector d
        c = [x0 - xd, y0 - yd]
        d = [xf - xd, yf - yd]

        # calculating distances 
        dist_A = distance(start_pos, end_pos) # to return 
        dist_B = distance(end_pos, [xf, yf]) # karnaya
        dist_C = distance(start_pos, [xf, yf])

        # logic to find the angle to turn (theta or (pi - theta))
        if(dist_B**2 > (dist_A ** 2 + dist_C ** 2)):
                start_turn = angle_m        
        else: start_turn = angle_s

        # calculating the direciton of turning (clockwise or anti clockwise)
        if(distance([xfr, yfr], end_pos) > distance([xfl, yfl], end_pos)):
                start_turn = - start_turn
        elif(distance([xfr, yfr], end_pos) == distance([xfl, yfl], end_pos)):
                if(distance([xf, yf], end_pos) == distance(start_pos, end_pos)):
                        start_turn  = pi

        # neglect the small angles
        min_angle = 0.03491
        min_distance = 10

        start_turn = start_turn if abs(start_turn) > min_angle else 0
        dist_A = dist_A if dist_A > min_distance else 0

        # returning the start turning angle, distance to travel, end turning angle
        return (round(start_turn, 4), round(dist_A, 4), round(end_angle, 4))


