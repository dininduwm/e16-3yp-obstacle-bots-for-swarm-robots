import math

img_x = 640
img_y = 480 


# distance calculation
def distanceTwoPoints(p1, p2):
    return math.sqrt((((p1[0]-p2[0])**2) + ((p1[1]-p2[1])**2)))

# remapping destinations
def remapDes(arr):
    for data in arr:
        data['x'] = int(data['x']/30*img_x)
        data['y'] = int(data['y']/30*img_y)

# finction to convert for points to center point + angle
def convert(points):
    # grabing the points
    p1 = points[0]
    p2 = points[1]
    p3 = points[2]
    p4 = points[3]

    # calculating the center point
    center = [int((p1[0]+p2[0]+p3[0]+p4[0])/4), int((p1[1]+p2[1]+p3[1]+p4[1])/4)]
    return [center, [p2, p3]]