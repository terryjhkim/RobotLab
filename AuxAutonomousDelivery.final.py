
from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note

robot = Create3(Bluetooth(""))

import math as m

#global variables --------------------------------------------------------------------
HAS_ARRIVED = False
HAS_COLLIDED = False
HAS_REALIGNED = False
HAS_FOUND_OBSTACLE = False
destination = (300,0)
ARRIVAL_THRESHOLD = 5.0
IR_ANGLES = [-65.3, -38.0, -20.0, -3.0, 14.25, 34.0, 65.3]
SENSOR2CHECK = 0


#Non-async functions -----------------------------------------------------------------
def getCorrectionAngle(heading):
    correctionAngle=int(heading-90)
    if correctionAngle<=180:
        return correctionAngle
    elif 180<correctionAngle<360:
        return -(360-correctionAngle)


def getAngleToDestination(current_position,destination):
    radians = m.atan2(destination[0]-current_position[0], destination[1]-current_position[1])
    degrees = m.degrees(radians)
    return int(degrees)


def getMinProxApproachAngle(readings, angles):
    maxProximity = readings[0]
    closestAngle = IR_ANGLES[0]
    for i in range(len(readings)):
        if readings[i] > maxProximity:
            maxProximity = readings[i]
            closestAngle = IR_ANGLES[i]
    proximity = 4095/(maxProximity + 1)
    return (proximity, closestAngle)


def checkPositionArrived(current_position, destination, threshold):
    xDis = destination[0] - current_position[0]
    yDis = destination[1] - current_position[1]
    distance = m.sqrt(xDis**2 + yDis**2)
    if distance <= threshold:
        HAS_ARRIVED = True
        return True
    else:
        return False

#async functions --------------------------------------------------------------------

async def realignRobot(robot):
    
    global HAS_REALIGNED

    pos = await robot.get_position()
    x = pos.x
    y = pos.y
    heading = pos.heading

    correctionAngle = getCorrectionAngle(heading)
    await robot.turn_right(correctionAngle)

    destAngle = getAngleToDestination((x, y), destination)
    await robot.turn_right(destAngle)

    HAS_REALIGNED = True
    print("realigned")
        

async def moveTowardGoal(robot):
    global SENSOR2CHECK, IR_ANGLES, HAS_FOUND_OBSTACLE

    await robot.set_wheel_speeds(10,10)
    
    readings = (await robot.get_ir_proximity()).sensors
    (proximity, closestAngle) = getMinProxApproachAngle(readings, IR_ANGLES)
    
    if proximity <= 20:
        if closestAngle > 0:
            await robot.turn_left(90 - closestAngle)
            SENSOR2CHECK = 6
        else:
            await robot.turn_right(90 + closestAngle)
            SENSOR2CHECK = 0
        HAS_FOUND_OBSTACLE = True
        print("has found obstacle")
    else:
        HAS_FOUND_OBSTACLE = False
        print("moving")
                      

async def followObstacle(robot):
    
    await robot.set_wheel_speeds(10, 10)
    global SENSOR2CHECK, HAS_FOUND_OBSTACLE, HAS_REALIGNED 
    
    
    readings = (await robot.get_ir_proximity()).sensors
    (proximity, angle) = getMinProxApproachAngle(readings, SENSOR2CHECK)

    print("proximity: " + str(proximity))
    print("SENSOR2CHECK: " + str(SENSOR2CHECK))
    
    if proximity <= 20:
        HAS_FOUND_OBSTACLE = True
        if SENSOR2CHECK == 0:
            await robot.turn_right(3)
        else:
            await robot.turn_left(3)
        print("following obstacle")
        
    elif proximity > 100:
        HAS_FOUND_OBSTACLE = False
        HAS_REALIGNED = False
        await robot.move(20)
        
        print("moved past obstacle")



@event(robot.when_play)
async def makeDelivery(robot):

    global HAS_COLLIDED, HAS_ARRIVED, HAS_REALIGNED, HAS_FOUND_OBSTACLE
    global destination, ARRIVAL_THRESHOLD
    
    while not HAS_ARRIVED:
        pos = await robot.get_position()
        HAS_ARRIVED = checkPositionArrived((pos.x, pos.y), destination, ARRIVAL_THRESHOLD)
        angle = getAngleToDestination((pos.x, pos.y),destination)

        if HAS_COLLIDED or HAS_ARRIVED:
            break

        print(HAS_FOUND_OBSTACLE)
        print(HAS_REALIGNED)
        print("angleToDest: " + str(angle))
        
        if not HAS_REALIGNED and not HAS_FOUND_OBSTACLE:
            print("1")
            await realignRobot(robot)
            
        if HAS_FOUND_OBSTACLE:
            print("2")
            await followObstacle(robot)

        if not HAS_FOUND_OBSTACLE and HAS_REALIGNED:
            print("3")
            await moveTowardGoal(robot)
            
        print("")

    await robot.set_wheel_speeds(0,0)
    
    if HAS_COLLIDED:
        await robot.set_lights_rgb(255, 0, 0)
    if HAS_ARRIVED:
        await robot.set_lights(Robot.LIGHT_SPIN,Color(0, 255, 0))


#Buttons/bumpers ---------------------------------------------------------------------
        
# LEFT BUTTON
@event(robot.when_touched, [True, False])
async def when_left_button_touched(robot):
    global HAS_COLLIDED
    HAS_COLLIDED = True
    await robot.set_lights_rgb(255, 0, 0)
    await robot.set_wheel_speeds(0,0)

# RIGHT BUTTON
@event(robot.when_touched, [False, True])
async def when_right_button_touched(robot):
    global HAS_COLLIDED
    HAS_COLLIDED = True
    await robot.set_wheel_speeds(0,0)
    await robot.set_lights_rgb(255, 0, 0)
    
# EITHER BUMPER
@event(robot.when_bumped, [True, True]) #[left, right]
async def when_either_bumped(robot):
    global HAS_COLLIDED
    HAS_COLLIDED = True
    await robot.set_wheel_speeds(0,0)
    await robot.set_lights_rgb(255, 0, 0)

robot.play()
