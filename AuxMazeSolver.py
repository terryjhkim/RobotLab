from collections import deque


def createMazeDict(nXCells, nYCells, cellDim):
    mazeDict={}
    for x in range(nXCells):
        for y in range(nYCells):
            small={}
            small['position']=(x*cellDim,y*cellDim)
            small['neighbors']=[]
            small['visited']=False
            small['cost']=0
            mazeDict[(x,y)]=small
    return mazeDict
                        



def addAllNeighbors(mazeDict, nXCells, nYCells):
    for ((x,y),small) in mazeDict.items():
        if x-1 in range(nXCells):
            small['neighbors']+=[(x-1,y)]
        if y+1 in range(nYCells):
            small['neighbors']+=[(x,y+1)]
        if x+1 in range(nXCells):
            small['neighbors']+=[(x+1,y)]
        if y-1 in range(nYCells):
            small['neighbors']+=[(x,y-1)]
    return mazeDict


def getRobotOrientation(heading):
    mina=361
    e1=heading
    e2=360-heading
    n=abs(90-heading)
    w=abs(180-heading)
    s=abs(270-heading)
    order=[n,w,s,e1,e2]
    angles=['N','W','S','E']
    for i in range(len(order)):
        if order[i]<mina:
            mina=order[i]
            index=i
    if index==3 or index==4:
        return 'E'
    else:
        return angles[index]




def getPotentialNeighbors(currentCell, orientation):
    (x,y)=currentCell
    potentialNeighbors=[(x-1,y),(x,y+1),(x+1,y),(x,y-1)]
    if orientation=='E':
        potentialNeighbors=potentialNeighbors[1:]+[potentialNeighbors[0]]
    elif orientation=='S':
        potentialNeighbors=potentialNeighbors[2:]+potentialNeighbors[0:2]
    elif orientation=='W':
        potentialNeighbors=[potentialNeighbors[-1]]+potentialNeighbors[:-1]
    return potentialNeighbors





def isValidCell(cellIndices, nXCells, nYCells):
    (x,y)=cellIndices
    if x in range(nXCells) and y in range(nYCells):
        return True
    else:
        return False
    



def getWallConfiguration(IR0,IR3,IR6,threshold):
    wallsAroundCell=[]
    inputList=[4095/(IR0+1),4095/(IR3+1),4095/(IR6+1)]
    for i in inputList:
        if i <=threshold:
            wallsAroundCell.append(True)
        else:
            wallsAroundCell.append(False)
    return wallsAroundCell




def getNavigableNeighbors(wallsAroundCell, potentialNeighbors, prevCell, nXCells, nYCells):
    navNeighbors=[]
    if prevCell!=None:
        navNeighbors.append(prevCell)
    for i in range(3):
        if wallsAroundCell[i]==False:
            if 0<=potentialNeighbors[i][0]<nXCells and 0<=potentialNeighbors[i][1]<nYCells:
                navNeighbors.append(potentialNeighbors[i])    
    return navNeighbors
    

def updateMazeNeighbors(mazeDict, currentCell, navNeighbors):
    for cell in mazeDict[currentCell]['neighbors']:
        if currentCell not in navNeighbors and currentCell in mazeDict[cell]['neighbors']:
            mazeDict[cell]['neighbors'].remove(currentCell)
    mazeDict[currentCell]['neighbors']=navNeighbors
    return mazeDict

def getNextCell(mazeDict, currentCell):
    nList=mazeDict[currentCell]['neighbors']
    minCost=100000

    notVisited=[]
    for cell in nList:
        visited=mazeDict[cell]['visited']
        if visited==False:
            notVisited.append(cell)
    if len(notVisited)!=0:
        for cell in notVisited:
            cost=mazeDict[cell]['cost']
            if cost<minCost:
                minCost=cost
                nextMove=cell
    else:
        for cell in nList:
            cost=mazeDict[cell]['cost']
            if cost<minCost:
                minCost=cost
                nextMove=cell
    return nextMove
        


def checkCellArrived(currentCell, destination):
    (x,y)=currentCell
    (xf,yf)=destination
    if x==xf and y==yf:
        return True
    else:
        return False
       


"""
The following implementation of the Flood Fill algorithm is
tailored for maze navigation. It updates the movement cost for
each maze cell as the robot learns about its environment. As
the robot moves and discovers navigable adjacent cells, it
gains new information, leading to frequent updates in the
maze's data structure. This structure tracks the layout and
traversal costs. With each step and discovery, the algorithm
recalculates the cost to reach the destination, adapting to
newly uncovered paths. This iterative process of moving,
observing, and recalculating continues until the robot reaches
its destination, ensuring an optimal path based on the robot's
current knowledge of the maze.
"""
def updateMazeCost(mazeDict, start, goal):
    for (i,j) in mazeDict.keys():
        mazeDict[(i,j)]["flooded"] = False
    queue = deque([goal])
    mazeDict[goal]['cost'] = 0
    mazeDict[goal]['flooded'] = True
    while queue:
        current = queue.popleft()
        current_cost = mazeDict[current]['cost']
        for neighbor in mazeDict[current]['neighbors']:
            if not mazeDict[neighbor]['flooded']:
                mazeDict[neighbor]['flooded'] = True
                mazeDict[neighbor]['cost'] = current_cost + 1
                queue.append(neighbor)
    return mazeDict

"""
This function prints the information from the dictionary as
a grid and can help you troubleshoot your implementation.
"""
def printMazeGrid(mazeDict, nXCells, nYCells, attribute):
    for y in range(nYCells - 1, -1, -1):
        row = '| '
        for x in range(nXCells):
            cell_value = mazeDict[(x, y)][attribute]
            row += '{} | '.format(cell_value)
        print(row[:-1])
