import math as m

def getCorrectionAngle(heading):
    if heading <= 270:
        correctionAngle = int(heading - 90)
    else:
        correctionAngle = int(90 + (360 - heading))
    return correctionAngle

"""
print(getCorrectionAngle(135.6))
print(getCorrectionAngle(25))
"""

def getAngleToDestination(currentPosition, destination):
    vector1 = destination[0] - currentPosition[0]
    vector2 = destination[1] - currentPosition[1]

    angle_rad = m.atan2(vector1, vector2)

    angleToDestination = int(m.degrees(angle_rad))

    return angleToDestination
"""
currentPosition = (1, 1)
destination = (5, 3)
print(getAngleToDestination(currentPosition, destination))

currentPosition = (5, 5)
destination = (1, 1)
print(getAngleToDestination(currentPosition, destination))
"""
def getMinProxApproachAngle(readings, angles):
    if len(readings) != len(angles):
        raise ValueError("Lengths of readings and angles lists must be the same.")

    min_prox = float('inf')
    min_angle = None

    for ir_reading, ir_angle in zip(readings, angles):
        proximity = 4095 / (ir_reading + 1)

        if proximity < min_prox:
            min_prox = proximity
            min_angle = ir_angle

    return min_prox, min_angle

"""
IR_ANGLES = [-65.3, -38.0, -20.0, -3.0, 14.25, 34.0, 65.3]
readings = [4, 347, 440, 408, 205, 53, 27]
print(getMinProxApproachAngle(readings, IR_ANGLES))

IR_ANGLES = [-65.3, -38.0, -20.0, -3.0, 14.25, 34.0, 65.3]
readings = [731, 237, 202, 229, 86, 120, 70]
print(getMinProxApproachAngle(readings, IR_ANGLES))
"""

def checkPositionArrived(currentPosition, destination, threshold):
    distance = m.sqrt((destination[0] - currentPosition[0])**2 + (destination[1] - currentPosition[1])**2)

    arrived_to_destination = distance <= threshold

    return arrived_to_destination
"""
print(checkPositionArrived((97, 99), (100, 100), 5.0))
print(checkPositionArrived((50, 50), (45, 55), 5))
"""
