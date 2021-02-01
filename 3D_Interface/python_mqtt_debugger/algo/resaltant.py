import math

# Assign names to list indices
# valuesList
F = 0
degrees = 1
x = 2
y = 3
radians = 4
Fx = 5
Fy = 6

# resultantList
Fr = 0
resDegrees = 1

resRadians = 4
Frx = 5
Fry = 6

valuesList = []
Forces = []

def waitingfornothing():
    """
    Just wait for user to press 'Enter'
    For debugging only!
    """
    waitingfornothing = input('...')


def getInput(count):
    """
    Input force and angle separated by a space.
    Forces must have all the same unit.
    Angle has to be degrees.
    If the force system is non-concurrent and non-parallel enter the x and y
    coordinates after the angle.
    Example:
    500 90
    Example with coordinates:
    500 90 10 -15
    """

    values = []
    for i in range(count):
        # handle each force
        givenForce = Forces[i]

        if len(givenForce) == 2:
            givenForce.extend([0, 0])

        # convert all element into float    
        givenForce = [float(element) for element in givenForce]

        # convert degrees to radians
        givenForce.append(math.radians(givenForce[degrees]))

        values.append(givenForce)

    return values


def resolveForce(Force, radians):
    values = [Force * math.cos(radians), (Force * math.sin(radians))]

    return values

def calcResaltant(Forces_list):

    global Forces
    Forces = Forces_list
    n = len(Forces)

    valuesList = []
    valuesList.extend(getInput(n))

    for values in valuesList:
        if len(values) == 5:
            values.extend(resolveForce(values[F], values[radians]))

    return valuesList

def getResultant(Forces):

    global valuesList
    valuesList = calcResaltant(Forces)

    resultant = [0] * 7
    for values in valuesList:
        resultant[Frx] += values[Fx]
        resultant[Fry] += values[Fy]

    resultant[Fr] = math.sqrt(resultant[Frx] ** 2 + resultant[Fry] ** 2)
    resultant[resRadians] = math.atan2(resultant[Fry], resultant[Frx])
    resultant[resDegrees] = math.degrees(resultant[resRadians])

    resultant[x], resultant[y] = \
            getCoordinatesOfResultant(resultant[Fr], resultant[resRadians])

    return resultant

def getCoordinatesOfResultant(resultant, angelOfResultant):

    Mx = 0
    My = 0
    for values in valuesList:
        Mx += values[Fx] * values[x]
        My += values[Fy] * values[y]

    # r is the distance from the origin of ordinates to the point of origin of
    # the resultant
    if (resultant == 0):
        return 0, 0
    r = (Mx - My) / resultant

    slopeResultant = math.tan(angelOfResultant)

    if (slopeResultant == 0):
        slope_r = 0.0
    else: slope_r = -(1/slopeResultant)

    x_of_resultant = math.sqrt(r ** 2 / ( 1 + slope_r ** 2))
    y_of_resultant = math.sqrt(r ** 2 - x_of_resultant ** 2)

    return x_of_resultant, y_of_resultant



