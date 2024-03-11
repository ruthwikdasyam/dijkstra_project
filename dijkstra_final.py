from queue import PriorityQueue
import numpy as np
import matplotlib.pyplot as plt
import heapq
import pygame

import time
start_time = time.time() #  Initiating time

print("\n--------------------------------------------------------------------------\n")
print("                        DIJKSTRA PATH PLANNING                                ")
print("\n--------------------------------------------------------------------------\n")


#__________________________________________________________________________________________________________________
#Defining Actions

def Up(Node_State, Cost_to_Come): # Action to go up
    new_state = Node_State.copy()
    # new_state[0] += 0
    new_state[1] += 1
    cost = 1 + Cost_to_Come
    return cost, new_state

def Up_Right(Node_State, Cost_to_Come):  # Action to go Up-Right
    new_state = Node_State.copy()
    new_state[0] += 1
    new_state[1] += 1
    cost = 1.4 + Cost_to_Come
    return cost, new_state

def Right(Node_State, Cost_to_Come):  # Action to go Right
    new_state = Node_State.copy()
    new_state[0] += 1
    # new_state[1] += 1
    cost = 1 + Cost_to_Come
    return cost, new_state

def Down_Right(Node_State, Cost_to_Come):  # Action to go Down_Right
    new_state = Node_State.copy()
    new_state[0] += 1
    new_state[1] -= 1
    cost = 1.4 + Cost_to_Come
    return cost, new_state

def Down(Node_State, Cost_to_Come):  # Action to go Down
    new_state = Node_State.copy()
    # new_state[0] += 1
    new_state[1] -= 1
    cost = 1 + Cost_to_Come
    return cost, new_state

def Down_Left(Node_State, Cost_to_Come):  # Action to go Down Left
    new_state = Node_State.copy()
    new_state[0] -= 1
    new_state[1] -= 1
    cost = 1.4 + Cost_to_Come
    return cost, new_state

def Left(Node_State, Cost_to_Come):  # Action to go Left
    new_state = Node_State.copy()
    new_state[0] -= 1
    # new_state[1] -= 1
    cost = 1 + Cost_to_Come
    return cost, new_state

def Up_Left(Node_State, Cost_to_Come):  # Action to go Up Left
    new_state = Node_State.copy()
    new_state[0] -= 1
    new_state[1] += 1
    cost = 1.4 + Cost_to_Come
    return cost, new_state


def Actions(Node_State, Cost_to_Come): # Combining all Actions into a single action
    children=[]
    children.append(Up(Node_State, Cost_to_Come))
    children.append(Up_Right(Node_State, Cost_to_Come))
    children.append(Right(Node_State, Cost_to_Come))
    children.append(Down_Right(Node_State, Cost_to_Come))
    children.append(Down(Node_State, Cost_to_Come))
    children.append(Down_Left(Node_State, Cost_to_Come))
    children.append(Left(Node_State, Cost_to_Come))
    children.append(Up_Left(Node_State, Cost_to_Come))
    return children # Returns list of all the children with thwir cost


def backtrack(closedlist): # Function for backtracking
    print(" Backtracking ....")
    states=[] # list to store all points that fall in the way
    parentstate= closedlist[-1][1] # parent state of goal node

    while parentstate != tuple(node1_state): #stopping when parent state is start state
        for node in closed_list:
            if node[2] == parentstate: #if parentstate equal to a node state from closed list
                states.append(parentstate) #storing all parent states
                parentstate = node[1]
                break

    states.reverse()
    return states
#_________________________________________________________________________________________________________________________________________________________
#               END OF FUNCTIONS FOR ACTIONS AND BACKTRACKING 

#Defining Obstacle Space
print(" Preparing Map ..... ")

def obstacle(x,y): # Returns value >= 1, if a point is in obstacle space
    # x=state[0]
    # y=state[1]
    check = 0
    check +=1 if x >= 100 and x < 170 and y >= 100  else 0 # 1 st obstacle
    check +=1 if x >= 275 and x < 350 and y < 400  else 0 # 1 st obstacle

    check +=1 if x >= 900 and x < 1100 and y >= 50  and y < 125 else 0 # U shape obstacle top part
    check +=1 if x >= 900 and x < 1100 and y >= 375 and y < 450 else 0 # U shape obstacle right part
    check +=1 if x >=1020 and x < 1100 and y >= 50  and y < 450 else 0 # U shape obstacle bottom part

    if x<=755 and x>495 and y>=100 and y<400: # equations for lines that surround polygon
        if (y-100)-(75/130)*(x-625) >= 0:
            if (y-325)+ (75/130)*(x-755) <=0:
                if (y-400)-(15/26)*(x-625) <=0:
                    if (y-175)+(15/26)*(x-495) >=0:
                        check +=1

    check +=1 if x <5 or x >= 1195 or y<5 or y >= 495 else 0  # borders of canvas
    return check 


matrix = np.zeros((1200,500)) # Defining a matrix representing canvas 1200 x 500 with zeros

for i in range(1200): # looping through all elements in matrix
        for j in range(500):
            if obstacle(i,j) != 0:  # element changes to 1 if index shows obstacle space
                matrix[i,j]=1

# TO have 5mm clearence means no pixel which is in distance of 5 from obstacle, should be avoided
# Below loop checks for such pixels and adjusts their matrix value to 2 

for i in range(5,1195):  # Loop for bloating
        for j in range(5,495):
            if matrix[i,j]==1: # if it is in obstacle space
              #if this element in obstacle space is in the corners of obstacle, (to save computation)
            #   if matrix[i-1,j-1] == 0 or matrix[i-1,j+1] == 0 or matrix[i+1,j-1] == 0 or matrix[i+1,j+1] == 0 :

                for i1 in range(i-5, i+6):   # clearence of 5         
                    for j1 in range(j-5,j+6):
                        if ((i1-i)**2 + (j1-j)**2) <= 25: # circle radius check
                            if matrix[i1,j1]==0: # if its a unassigned pixel
                                matrix[i1,j1]=2 # assign it to 2

#_________________________________________________________________________________________________________________________________________________________
#END OF OBSTACLE SPACE

#Defining initial and final nodes
                                
invalid_start = True
while invalid_start:
    print("\n_____START NODE ______")
    start_node_input_x = int(input("Start Node 'X' : "))
    start_node_input_y = int(input("Start Node 'Y' : "))
    if start_node_input_x>=0 and start_node_input_x<1200 and start_node_input_y>=0 and start_node_input_x<500 and matrix[start_node_input_x, start_node_input_y] == 0:
            invalid_start = False
            node1_state = [start_node_input_x, start_node_input_y]
    else:
        print("Invalid Start Node, Input again")

invalid_goal = True
while invalid_goal:
    print("\n_____GOAL NODE ______")
    goal_node_input_x = int(input("Goal Node 'X' : "))
    goal_node_input_y = int(input("Goal Node 'Y' : "))
    if goal_node_input_x>=0 and goal_node_input_x<1200 and goal_node_input_y>=0 and goal_node_input_y<500 and matrix[goal_node_input_x, goal_node_input_y] == 0:
            invalid_goal = False   
            goal_state = [goal_node_input_x, goal_node_input_y]
    else:
        print("Invalid Goal Node, Input again")
    
print("__________________________")
print("  Nodes Accepted  ")
print("  Computing Path .....  ")


#_________________________________________________________________________________________________________________________________________________________
#END OF DEFINING START AND END GOAL

#Defining initial and final nodes

# node1_state = [5,5] #state of start point
# goal_state = [200,400] #state of Goal point
closed_list = []
closed_list_states= set()

open_list = PriorityQueue() #priority queue for open list
open_list.put([0, node1_state, node1_state]) # adding start node to open list

#_________________________________________________________________________________________________________________________________________________________
#    START OF LOOP


loop = True
while loop: 
    if open_list.qsize() !=0: # cheking if open list is empty
        current_node_cost, parent_node, current_node_state = open_list.get() #extracting node with least cost
    else:
        print("No Solution Found") # returning no solution if open list is empty
        break
    
    closed_list.append((current_node_cost, tuple(parent_node), tuple(current_node_state))) # adding popped node into closed list
    closed_list_states.add(tuple(current_node_state)) # adding its state to closed list states list
    # print(current_node.Node_Index)
    if current_node_state == goal_state: #checking if the current state is goal state
        print("\nGoal Reached")
        # print(current_node_cost, parent_node, tuple(current_node_state))
        points_list = backtrack(closed_list) # perform backtracking if goal state is reached
        break
    
    # children_set -> nodes and cost obtained from all children
    children_set = Actions(current_node_state, current_node_cost) # performing actions to get children

    for cost_child,child in children_set:
        if matrix[child[0],child[1]] == 0 : # checking if child is in the obstacle space
            if tuple(child) not in closed_list_states: # checking if the state is in the closed states list
                
                in_open_list = False
                # commands to check open list, and get the index of that node in openlist
                if open_list.qsize() != 0:  #if open list is not empty
                    open_list_states_set = list(np.array(open_list.queue,dtype= object)[:,2])
                    if child in open_list_states_set:
                            in_open_list = True
                            index = open_list_states_set.index(child)   # #finding index of child node, from open list

                            if cost_child < open_list.queue[index][0]:  # comparing cost
                                open_list.queue[index][0] = cost_child  # updating its cost
                                open_list.queue[index][1] = current_node_state  # updating its state

                if in_open_list == False: # if the state is not in open list, then creating a state, adding it to open list
                        new_node = [cost_child, current_node_state, child]
                        open_list.put(new_node)
                    
#_________________________________________________________________________________________________________________________________________________________
#    END OF LOOP

print("Process finished --- %s seconds ---\n" % (time.time() - start_time)) # DIsplays run time
#_________________________________________________________________________________________________________________________________________________________
#    INITIALIZING PYGAME

pygame.init()
#initializing window
window = pygame.display.set_mode((1200,500)) # window size
window.fill((200,200,200)) # filling it with color
#initializing color
white=(220,220,220)
black = (0,0,0)
red = (225,50,50)
blue = (105,135,235)

# LOOP to transform matrix into this window
for i in range(1200):
    for j in range(500):
        if matrix[i,j]==1: # 1 -> black color showing obstacles
            window.set_at((i,499-j),red)
        elif matrix[i,j]==2: # 2-> RED showing bloating part
            window.set_at((i,499-j),black)

pygame.display.flip() #updating window

#______________________________________WINDOW IS CREATED

# Loop to reflect all explored nodes from closed list to pyagme windoe


for i,node in enumerate(closed_list): 
        statexy = node[2]
        window.set_at((statexy[0],499-statexy[1]),blue) # performing (499-x) to account for origin changes
        if i%80==0: # rate to reflect the updates on the window
            pygame.display.flip()

time.sleep(1)
# LOop to reflect the points in the path on the pygame window
for i, point in enumerate(points_list):
        time.sleep(0.01)
        window.set_at((point[0],499-point[1]),black) # performing (499-x) to account for origin changes
        pygame.display.flip()



print(" ------------------------ SUCCESSFULLT TRACKED ------------------------")
print("------- DIJKSTRA by RD")

#LOOP to keep pygame running untill manually closed
run = True
while run: 
    for event in pygame.event.get():
     if event.type ==pygame.QUIT:
        run = False
    pygame.display.update()

pygame.quit()

#_________________________________________________________________________________________________________________________________________________________
#    END OF PYGAME