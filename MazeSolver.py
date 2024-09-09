from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note

import AuxMazeSolver as aux
import math as m

# === CREATE ROBOT OBJECT
robot = Create3(Bluetooth("T-X"))

# === FLAG VARIABLES
HAS_COLLIDED = False
HAS_ARRIVED = False

# === BUILD MAZE DICTIONARY
N_X_CELLS = 4
N_Y_CELLS = 4
CELL_DIM = 50
MAZE_DICT = aux.createMazeDict(N_X_CELLS, N_Y_CELLS, CELL_DIM)
MAZE_DICT = aux.addAllNeighbors(MAZE_DICT, N_Y_CELLS, N_Y_CELLS)

# === DEFINING ORIGIN AND DESTINATION
PREV_CELL = None
START = (0,0)
CURR_CELL = START
DESTINATION = (0,3)
MAZE_DICT[CURR_CELL]["visited"] = True

# === PROXIMITY TOLERANCES
WALL_THRESHOLD = 80


# ==========================================================
# FAIL SAFE MECHANISMS

# EITHER BUTTON
@event(robot.when_touched, [True, True])  # User buttons: [(.), (..)]
async def when_either_button_touched(robot):
    global HAS_COLLIDED
    HAS_COLLIDED = True
    await robot.set_wheel_speeds(0,0)
    await robot.set_lights_rgb(255, 0, 0)


# EITHER BUMPER
@event(robot.when_bumped, [True, True])  # [left, right]
async def when_either_bumped(robot):
    global HAS_COLLIDED
    HAS_COLLIDED = True
    await robot.set_wheel_speeds(0,0)
    await robot.set_lights_rgb(255, 0, 0)


# ==========================================================
# MAZE NAVIGATION AND EXPLORATION

# === NAVIGATE TO CELL
async def navigateToNextCell(robot, nextCell, orientation):
    global MAZE_DICT, PREV_CELL, CURR_CELL, CELL_DIM

    pos = await robot.get_position()
    heading = pos.heading
    correctionAngle=int(heading-90)
    if correctionAngle<=180:
        await robot.turn_right(correctionAngle)
    elif 180<correctionAngle<360:
        await robot.turn_left(360-correctionAngle)
    orientation='N'
    

    x=nextCell[0]-CURR_CELL[0]
    y=nextCell[1]-CURR_CELL[1]
    radiant=m.atan2(x,y)
    angle=int(m.degrees(radiant))
    
    if angle<0:
        await robot.turn_right(angle)
        await robot.move(CELL_DIM)
    elif angle>0:
        await robot.turn_right(angle)
        await robot.move(CELL_DIM)
    elif angle==0:
        await robot.move(CELL_DIM)

    MAZE_DICT[CURR_CELL]['visited']=True
    PREV_CELL=CURR_CELL
    CURR_CELL=nextCell

    

# === EXPLORE MAZE

@event(robot.when_play)
async def navigateMaze(robot):
    global HAS_COLLIDED, HAS_ARRIVED
    global PREV_CELL, CURR_CELL, START, DESTINATION
    global MAZE_DICT, N_X_CELLS, N_Y_CELLS, CELL_DIM, WALL_THRESHOLD
    
    while HAS_COLLIDED==False and HAS_ARRIVED==False:
        
        pos = await robot.get_position()
        heading = pos.heading
        readings=(await robot.get_ir_proximity()).sensors

        HAS_ARRIVED=aux.checkCellArrived(CURR_CELL, DESTINATION)
    
        if HAS_ARRIVED==True:
            print(CURR_CELL)
            await robot.set_wheel_speeds(0,0)
            await robot.set_lights(Robot.LIGHT_SPIN,Color(0, 255, 0))
            break
        
        orientation = aux.getRobotOrientation(heading)
        potentialNeighbors=aux.getPotentialNeighbors(CURR_CELL, orientation)

        wallsAroundCell=aux.getWallConfiguration(readings[0],readings[3],readings[6],WALL_THRESHOLD)
        navNeighbors=aux.getNavigableNeighbors(wallsAroundCell, potentialNeighbors, PREV_CELL, N_X_CELLS, N_Y_CELLS)
        MAZE_DICT=aux.updateMazeNeighbors(MAZE_DICT, CURR_CELL, navNeighbors)
        MAZE_DICT=aux.updateMazeCost(MAZE_DICT, START, DESTINATION)
        print(MAZE_DICT[CURR_CELL]['neighbors'])
        print(orientation)
        print(CURR_CELL)
        print("\n")
        
        
        
        nextCell=aux.getNextCell(MAZE_DICT, CURR_CELL)
        await navigateToNextCell(robot, nextCell, orientation)
       
        


# start the robot
robot.play()
