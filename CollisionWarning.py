from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note

# robot is the instance of the robot that will allow us to call
# its methods and to define events with the @event decorator.
robot = Create3(Bluetooth("M3GAN")) 

# LEFT BUTTON
@event(robot.when_touched, [True, False])  # User buttons: [(.), (..)]
async def when_left_button_touched(robot):
    await robot.set_wheel_speeds(0,0)
    await robot.set_lights_rgb(255, 0, 0)
    pass


# RIGHT BUTTON
@event(robot.when_touched, [False, True])  # User buttons: [(.), (..)]
async def when_right_button_touched(robot):
    await robot.set_wheel_speeds(0,0)
    await robot.set_lights_rgb(255, 0, 0)
    pass


# EITHER BUMPER
@event(robot.when_bumped, [True, True])  # [left, right]
async def when_either_bumped(robot):
    await robot.set_wheel_speeds(0,0)
    await robot.set_lights_rgb(255, 0, 0)
    pass


@event(robot.when_play)
async def avoidCollision(robot):
    global proximity
    await robot.set_wheel_speeds(8,8)
    while True:
        ir_reading = (await robot.get_ir_proximity()).sensors
        proximity = 4095/(ir_reading[3]+1)

        if proximity <= 5.0:
            await robot.set_wheel_speeds(0,0)
            await robot.set_lights_rgb(255, 0, 0)
            await robot.play_note(Note.D7, 1)
        elif proximity <= 30.0:
            await robot.set_wheel_speeds(1, 1)
            await robot.set_lights(Robot.LIGHT_BLINK,Color(255, 155, 0))
            await robot.play_note(Note.D6, 0.1)
        elif proximity <= 100.0:
            await robot.set_wheel_speeds(4, 4)
            await robot.set_lights(Robot.LIGHT_BLINK,Color(255, 255, 0))
            await robot.play_note(Note.D5, 0.1)
        elif proximity >= 100.0:
            await robot.set_wheel_speeds(8, 8)
            await robot.set_lights(Robot.LIGHT_BLINK,Color(0, 255, 0))

    pass


# start the robot
robot.play()
