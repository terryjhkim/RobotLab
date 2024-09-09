from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note

import math as m


# robot is the instance of the robot that will allow us to call
# its methods and to define events with the @event decorator.
robot = Create3(Bluetooth("M3GAN"))


def getApproachAngle(readings, angles):
    minReading = readings[0]
    proximityAngle = angles[0]
    for i in range(len(readings)):
        sensorReading = readings[i]
        if sensorReading < minReading:
            minReading = sensorReading
            closestAngle = angles[i]
            proximityAngle = angles[i]
    return proximityAngle

# LEFT BUTTON
@event(robot.when_touched, [True, False])  # User buttons: [(.), (..)]
async def when_left_button_touched(robot):
    await robot.move(0)
    await robot.set_lights_rgb(255, 0, 0)
  


# RIGHT BUTTON
@event(robot.when_touched, [False, True])  # User buttons: [(.), (..)]
async def when_right_button_touched(robot):
    await robot.move(0)
    await robot.set_lights_rgb(255, 0, 0)


# EITHER BUMPER
@event(robot.when_bumped, [True, True])  # [left, right]
async def when_either_bumped(robot):
    await robot.move(0)
    await robot.set_lights_rgb(255, 0, 0)
 


@event(robot.when_play)
async def robotPong(robot):
    await robot.set_lights(Robot.LIGHT_SPIN, Color(0,100,100))
    await robot.set_wheel_speeds(15, 15)
    
    while True:
        angles = [-65.3, -38, -20, -3, 14.25, 34, 65.3]
        ir_reading = (await robot.get_ir_proximity()).sensors
        light_color = "cyan"

        for i in range(len(ir_reading)):
            proximity = 4095/(ir_reading[i]+1)
            print(proximity)

            if proximity <= 20:
                if light_color == "cyan":
                    await robot.set_lights(Robot.LIGHT_SPIN, Color(255, 0, 255))
                    light_color = "magenta"
                elif light_color == "magenta":
                    await robot.set_lights(Robot.LIGHT_SPIN, Color(0, 100, 100))
                    light_color = "cyan"

                approachAngle = getApproachAngle(ir_reading, angles)
                if approachAngle < 0:
                    reflectionAngle = 180 + 2 * approachAngle
                    await robot.turn_right(reflectionAngle)
                    await robot.set_wheel_speeds(15,15)
                else:
                    reflectionAngle = 180 - 2 * approachAngle
                    await robot.turn_left(reflectionAngle)
                    await robot.set_wheel_speeds(15,15)
    

    
# ask for desired
robot.play()
