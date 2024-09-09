from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note

# robot is the instance of the robot that will allow us to call
# its methods and to define events with the @event decorator.
robot = Create3(Bluetooth("M3GAN"))

CORRECT_CODE = "341124"
COUNTBUMPED = ""
# LEFT BUTTON
@event(robot.when_touched, [True, False])  # User buttons: [(.), (..)]
async def when_left_button_touched(robot):
    global COUNTBUMPED
    COUNTBUMPED += "1"

    if len(COUNTBUMPED) == len(CORRECT_CODE):
        await robot.play_note(Note.C5,1)
        await checkUserCode(robot)

    else:
        await robot.play_note(400,1)

    

# RIGHT BUTTON
@event(robot.when_touched, [False, True])  # User buttons: [(.), (..)]
async def when_right_button_touched(robot):
    global COUNTBUMPED
    COUNTBUMPED += "2"
    
    if len(COUNTBUMPED) == len(CORRECT_CODE):
        await robot.play_note(Note.D5,1)
        await checkUserCode(robot)

    else:
        await robot.play_note(500,1)


# LEFT BUMP
@event(robot.when_bumped, [True, False])  # [left, right]
async def when_left_bumped(robot):
    global COUNTBUMPED
    COUNTBUMPED += "3"
  
    if len(COUNTBUMPED) == len(CORRECT_CODE):
        await robot.play_note(Note.E5,1)
        await checkUserCode(robot)

    else:
        await robot.play_note(600,1)


# RIGHT BUMP
@event(robot.when_bumped, [False, True]) # [left, right]
async def when_right_bumped(robot):
    global COUNTBUMPED
    COUNTBUMPED += "4"
    
    if len(COUNTBUMPED) == len(CORRECT_CODE):
        await robot.play_note(Note.D5,1)
        await checkUserCode(robot)

    else:
        await robot.play_note(700,1)

async def checkUserCode(robot):
    global COUNTBUMPED
    if COUNTBUMPED == CORRECT_CODE:
        await robot.turn_right(45)
        await robot.turn_left(90)
        await robot.turn_right(180)
        await robot.turn_left(90)
        await robot.set_lights(Robot.LIGHT_BLINK, color(0, 400, 0))
        await robot.play_note(400,0.5)
        await robot.play_note(450,0.5)
        await robot.play_note(500,0.5)
        await robot.play_note(550,0.5)
        
    elif COUNTBUMPED != CORRECT_CODE:
        COUNTBUMPED = ""
        await robot.set_lights(Robot.LIGHT_BLINK, color(400, 0, 0))
        await robot.play_note(500,0.5)
        await robot.play_note(450,0.5)
        await robot.play_note(400,0.5)
        print("failed")
    pass


@event(robot.when_play)
async def play(robot):
    global COUNTBUMPED
    pass


robot.play()
