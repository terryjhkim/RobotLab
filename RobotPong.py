from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, Robot, Color, Create3
from irobot_edu_sdk.music import Note

import math

robot = Create3(Bluetooth("M3GAN"))

def calculateApproachAngle(sensor_data, angles_list):
    """Calculate the angle of the closest object based on sensor data."""
    min_value = min(sensor_data)
    min_index = sensor_data.index(min_value)
    return angles_list[min_index]

@event(robot.when_touched, [True, False]) 
async def handle_left_button(robot):
    await robot.move(0) 
    await robot.set_lights_rgb(255, 0, 0)  
    
@event(robot.when_touched, [False, True]) 
async def handle_right_button(robot):
    await robot.move(0) 
    await robot.set_lights_rgb(255, 0, 0) 

@event(robot.when_bumped, [True, True]) 
async def handle_bump(robot):
    await robot.move(0) 
    await robot.set_lights_rgb(255, 0, 0) 

@event(robot.when_play)
async def play_pong(robot):
    await robot.set_lights(Robot.LIGHT_SPIN, Color(0, 100, 100)) 
    await robot.set_wheel_speeds(15, 15) 

    while True:
        angles = [-65.3, -38, -20, -3, 14.25, 34, 65.3]
        ir_proximity = (await robot.get_ir_proximity()).sensors
        light_color = "cyan"

        for reading in ir_proximity:
            proximity_value = 4095 / (reading + 1)
            print(proximity_value)

            if proximity_value <= 20:
                if light_color == "cyan":
                    await robot.set_lights(Robot.LIGHT_SPIN, Color(255, 0, 255))  # Change to magenta
                    light_color = "magenta"
                else:
                    await robot.set_lights(Robot.LIGHT_SPIN, Color(0, 100, 100))  # Change to cyan
                    light_color = "cyan"

                approach_angle = calculateApproachAngle(ir_proximity, angles)
                if approach_angle < 0:
                    reflection_angle = 180 + 2 * approach_angle
                    await robot.turn_right(reflection_angle)
                else:
                    reflection_angle = 180 - 2 * approach_angle
                    await robot.turn_left(reflection_angle)

                await robot.set_wheel_speeds(15, 15)

robot.play()
