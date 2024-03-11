import pygame
import numpy as np
# initializing pygame
pygame.init()

#initializing surface
surface = pygame.display.set_mode((1200,500))
surface.fill((200,200,200))
#initializing color
color = (220,10,0)
color1 = (255,0,0)
color2 = (0,0,0)


# drawing rectangle


def obstacle(x,y):
    # x=state[0]
    # y=state[1]
    check = 0
    # if x > 95 and x < 105 and y > 95 and (x-100)**2 + (y-100)**2 > 25 and (x-175)**2 + (y-100)**2 > 25:
    check +=1 if x > 95 and x < 180 and y > 95  else 0 # 1 st obstacle
    # if x > 270 and x < 355 and y < 405 and (x-275)**2 + (y-400)**2 > 25 and (x-350)**2 + (y-400)**2 > 25:
    check +=1 if x > 270 and x < 355 and y < 405  else 0 # 1 st obstacle
    check +=1 if x > 895 and x < 1105 and y > 45 and y < 130 else 0 # U shape obstacle top part
    check +=1 if x > 895 and x < 1105 and y >370 and y < 455 else 0 # U shape obstacle right part
    check +=1 if x >1015 and x < 1105 and y > 45 and y < 455 else 0 # U shape obstacle bottom part

    #((625, 100), (755, 175), (755, 325), (625, 400), (495, 325),(495, 175))
    if x<755 and x>495 and y>100 and y<400:
        if (y-100)-(75/130)*(x-625) > 0:
            if (y-325)+ (75/130)*(x-755) <0:
                if (y-400)-(15/26)*(x-625) <0:
                    if (y-175)+(15/26)*(x-495) >0:
                        check +=1

    check +=1 if x <5 or x > 1195 or y<5 or y > 495 else 0  # borders
    return check  


# pygame.draw.rect(surface, color, pygame.Rect(100,   0,  75, 400))
# pygame.draw.rect(surface, color, pygame.Rect(275, 100,  75, 400))
# pygame.draw.rect(surface, color, pygame.Rect(900,  50, 200,  75))
# pygame.draw.rect(surface, color, pygame.Rect(1020,125,  80, 250))
# pygame.draw.rect(surface, color, pygame.Rect(900, 375, 200,  75))
# pygame.draw.polygon(surface, color2, ((625, 100), (755, 175), (755, 325), (625, 400), (495, 325),(495, 175)))

# pygame.draw.rect(surface, color2, pygame.Rect(0,0,1200,500), 5)




 

pygame.display.flip()
matrix = np.zeros((1200,500))

# print(surface.get_at((500,1200)))

for i in range(1200):
        for j in range(500):
            if obstacle(i,j) != 0:
                matrix[i,j]=1


# pygame.display.flip()

count = 0

for i in range(5,1195):
        for j in range(5,495):
            if matrix[i,j]==1:
              if matrix[i-1,j-1] == 0 or matrix[i-1,j+1] == 0 or matrix[i+1,j-1] == 0 or matrix[i+1,j+1] == 0 :
                for i1 in range(i-5, i+5):            
                    for j1 in range(j-5,j+5):
                        if ((i1-i)**2 + (j1-j)**2) <= 25:
                            if matrix[i1,j1]==0:
                                matrix[i1,j1]=2


for i in range(1200):
    for j in range(500):
        if matrix[i,j]==1:
            surface.set_at((i,j), color2)
        elif matrix[i,j]==2:
            surface.set_at((i,j), color1)

pygame.display.flip()

print("count",count)


run = True
while run:
    for event in pygame.event.get():
     if event.type ==pygame.QUIT:
        run = False
    pygame.display.update()
pygame.quit()





# drawing rectangle
# pygame.draw.rect(window, coloro, pygame.Rect(100,   0,  75, 400))
# pygame.draw.rect(window, colorc, pygame.Rect(95 ,   0,  85, 405), 5)

# pygame.draw.rect(window, coloro, pygame.Rect(275, 100,  75, 400))
# pygame.draw.rect(window, colorc, pygame.Rect(270, 100,  85, 405), 5)

# # pygame.draw.polygon(window, colorc, ((895, 45), (1105,45), (1105,455), (895,455), (895,370),(1015,370),(1015,130),(895,130)),5)
# pygame.draw.polygon(window, coloro, ((900, 50), (1100,50), (1100,450), (900,450), (900,375),(1020,375),(1020,125),(900,125)))
# pygame.draw.polygon(window, colorc, ((900, 50), (1100,50), (1100,450), (900,450), (900,375),(1020,375),(1020,125),(900,125)),-5)

# pygame.draw.polygon(window, coloro, ((625, 100), (755, 175), (755, 325), (625, 400), (495, 325),(495, 175)))
# pygame.draw.rect(window, colorc, pygame.Rect(0,0,1200,500), 5)

# pygame.display.flip()