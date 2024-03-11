from queue import PriorityQueue
import numpy as np
import matplotlib.pyplot as plt
import heapq
import pygame

import time
start_time = time.time()


no_of_nodes = 0

class node_class:
    all_states = []
    def __init__(self, Cost_to_Come : float, Node_Index: int, Parent_Index: int, Node_State: np.array) -> None:
        #Assign to Self Object
        self.Cost_to_Come = Cost_to_Come  # Cost to come
        self.Node_Index = Node_Index # Node index
        self.Parent_Index = Parent_Index # parent node index
        self.Node_State = Node_State  # Node state - coordinate values
        global no_of_nodes
        node_class.all_states.append(self)
        no_of_nodes += 1

    def __repr__(self):
        return f"{self.Cost_to_Come}, {self.Node_Index}, {self.Parent_Index}, {self.Node_State}" # Defining representation of object to be its state, index and parent index

    def __lt__(self, other):
        # First, try to compare based on Cost_to_Come
        if self.Cost_to_Come != other.Cost_to_Come:
            return self.Cost_to_Come < other.Cost_to_Come
        # If costs are equal, then compare based on Node_Index
        return self.Node_Index < other.Node_Index


    #Defining Actions
    def Up(self):
        new_state = self.Node_State.copy()
        # new_state[0] += 0
        new_state[1] += 1
        cost = 1 + self.Cost_to_Come
        return cost, new_state
    
    def Up_Right(self):
        new_state = self.Node_State.copy()
        new_state[0] += 1
        new_state[1] += 1
        cost = 1.4 + self.Cost_to_Come
        return cost, new_state
    
    def Right(self):
        new_state = self.Node_State.copy()
        new_state[0] += 1
        # new_state[1] += 1
        cost = 1 + self.Cost_to_Come
        return cost, new_state
    
    def Down_Right(self):
        new_state = self.Node_State.copy()
        new_state[0] += 1
        new_state[1] -= 1
        cost = 1.4 + self.Cost_to_Come
        return cost, new_state
    
    def Down(self):
        new_state = self.Node_State.copy()
        # new_state[0] += 1
        new_state[1] -= 1
        cost = 1 + self.Cost_to_Come
        return cost, new_state
    
    def Down_Left(self):
        new_state = self.Node_State.copy()
        new_state[0] -= 1
        new_state[1] -= 1
        cost = 1.4 + self.Cost_to_Come
        return cost, new_state
    
    def Left(self):
        new_state = self.Node_State.copy()
        new_state[0] -= 1
        # new_state[1] -= 1
        cost = 1 + self.Cost_to_Come
        return cost, new_state
    
    def Up_Left(self):
        new_state = self.Node_State.copy()
        new_state[0] -= 1
        new_state[1] += 1
        cost = 1.4 + self.Cost_to_Come
        return cost, new_state
    
    def Actions(self):
        children=[]
        children.append(self.Up())
        children.append(self.Up_Right())
        children.append(self.Right())
        children.append(self.Down_Right())
        children.append(self.Down())
        children.append(self.Down_Left())
        children.append(self.Left())
        children.append(self.Up_Left())
        return children

    def backtrack(self):
        states=[]
        states.append(self.Node_State)
        index = self.Parent_Index
        while index != 1:
            state_ = node_class.all_states[index-1].Node_State
            states.append(state_)
            index = node_class.all_states[index-1].Parent_Index
        states.reverse()
        return states
#_________________________________________________________________________________________________________________________________________________________
#END OF CLASS

#Defining Obstacle Space

def obstacle(x,y):
    # x=state[0]
    # y=state[1]
    check = 0
    # if x > 95 and x < 105 and y > 95 and (x-100)**2 + (y-100)**2 > 25 and (x-175)**2 + (y-100)**2 > 25:
    check +=1 if x >= 100 and x < 170 and y >= 100  else 0 # 1 st obstacle
    # if x > 270 and x < 355 and y < 405 and (x-275)**2 + (y-400)**2 > 25 and (x-350)**2 + (y-400)**2 > 25:
    check +=1 if x >= 275 and x < 350 and y < 400  else 0 # 1 st obstacle

    check +=1 if x >= 900 and x < 1100 and y >= 50  and y < 125 else 0 # U shape obstacle top part
    check +=1 if x >= 900 and x < 1100 and y >= 375 and y < 450 else 0 # U shape obstacle right part
    check +=1 if x >=1020 and x < 1100 and y >= 50  and y < 450 else 0 # U shape obstacle bottom part

    #((625, 100), (755, 175), (755, 325), (625, 400), (495, 325),(495, 175))
    if x<=755 and x>495 and y>=100 and y<400:
        if (y-100)-(75/130)*(x-625) >= 0:
            if (y-325)+ (75/130)*(x-755) <=0:
                if (y-400)-(15/26)*(x-625) <=0:
                    if (y-175)+(15/26)*(x-495) >=0:
                        check +=1

    check +=1 if x <5 or x >= 1195 or y<5 or y >= 495 else 0  # borders
    return check 


matrix = np.zeros((1200,500))

for i in range(1200):
        for j in range(500):
            if obstacle(i,j) != 0:
                matrix[i,j]=1

for i in range(5,1195):
        for j in range(5,495):
            if matrix[i,j]==1:
              if matrix[i-1,j-1] == 0 or matrix[i-1,j+1] == 0 or matrix[i+1,j-1] == 0 or matrix[i+1,j+1] == 0 :

                for i1 in range(i-5, i+5):            
                    for j1 in range(j-5,j+5):
                        if ((i1-i)**2 + (j1-j)**2) <= 25:
                            if matrix[i1,j1]==0:
                                matrix[i1,j1]=2

#_________________________________________________________________________________________________________________________________________________________
#END OF OBSTACLE SPACE

#Defining initial and final nodes
invalid_start = True
while invalid_start:
    print("_____START NODE ______")
    start_node_input_x = int(input("Start Node 'X' : "))
    start_node_input_y = int(input("Start Node 'Y' : "))
    if start_node_input_x>=0 and start_node_input_x<1200 and start_node_input_y>=0 and start_node_input_x<500 and matrix[start_node_input_x, start_node_input_y] == 0:
            invalid_start = False
            node1_state = [start_node_input_x, start_node_input_y]
    else:
        print("Invalid Start Node, Input again")

invalid_goal = True
while invalid_goal:
    print("_____GOAL NODE ______")
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
# node1_state = [5,5] #state of start point5
# goal_state = [50,450] #state of Goal point

node1 = node_class(0,1,0,node1_state) # creating a node with start point

# closed_list = []
closed_list_states=[]

open_list = []
open_list_explored=[]

heapq.heappush(open_list,(node1.Cost_to_Come, node1.Node_State, node1))
open_list_explored.append(node1.Node_State)
# print(l(open_list[0]))

loop = True
while loop:
    if len(open_list)!=0: 
        current_node_cost, current_node_state, current_node = heapq.heappop(open_list)
    else:
        print("No Solution Found")
        break
    
    # closed_list.append(current_node)
    closed_list_states.append(current_node_state)
    # print(current_node.Node_Index)
    if current_node_state == goal_state:
        print("Goal Reached")
        print(current_node)
        points_list = current_node.backtrack()
        break
    
    children_set=[]
    children_set = current_node.Actions() # performing actions to get children

    for cost_child,child in children_set:
        # if not window.get_at((child[0],child[1]))[1] == 100 :
        if matrix[child[0],child[1]] == 0 : # checking if child is in the obstacle space
            if child not in closed_list_states: # checking if the state is in the closed states list

                in_open_list = False
                if len(open_list)!= 0:  #if open list is not empty
                    open_list_states = list(np.array(open_list, dtype= object)[:,1]) #conveting column of states into a list, changes every iteration

                    if child in open_list_states:
                            in_open_list = True
                            index = open_list_states.index(child)   # #finding index of child node, from open list

                            if cost_child < open_list[index][0]:    
                                open_list[index][0] = cost_child
                                open_list[index][2].Cost_to_come = cost_child
                                open_list[index][2].Parent_Index = current_node.Node_Index
                                # heapq.heapify(open_list)
                                break
                            else:
                                break                

                if in_open_list == False:
                        new_node = node_class(cost_child, no_of_nodes+1, current_node.Node_Index, child)
                        heapq.heappush(open_list,(new_node.Cost_to_Come, new_node.Node_State, new_node))
                        open_list_explored.append(new_node.Node_State)
                        matrix[child[0],child[1]]=4
                        # window.set_at((child[0],child[1]),color1)
                    

# for i in node_class.all_states:
#     print(i)
print("Process finished --- %s seconds ---" % (time.time() - start_time)) # DIsplays run time


pygame.init()
#initializing window
window = pygame.display.set_mode((1200,500))
window.fill((200,200,200))
#initializing color
white=(220,220,220)
black = (0,0,0)
red = (225,50,50)
blue = (105,135,235)

for i in range(1200):
    for j in range(500):
        # if matrix[i,j]==0:
        #     window.set_at((i,j),white)
        if matrix[i,j]==1:
            window.set_at((i,j),black)
        elif matrix[i,j]==2:
            window.set_at((i,j),red)
        # elif matrix[i,j]==3:
        #     window.set_at((i,j),black)
        # elif matrix[i,j]==4:
        #     window.set_at((i,j),blue)

pygame.display.flip()

for i,state in enumerate(open_list_explored):
        window.set_at((state[0],state[1]),blue)
        if i%100==0:
            pygame.display.flip()

for i, point in enumerate(points_list):
        time.sleep(0.01)
        window.set_at((point[0],point[1]),white)
        # if i%10==0:
        pygame.display.flip()





run = True
while run:
    for event in pygame.event.get():
     if event.type ==pygame.QUIT:
        run = False
    pygame.display.update()


pygame.quit()

