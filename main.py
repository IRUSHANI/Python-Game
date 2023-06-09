import pygame
from pygame import mixer
import random
import math

#initialize pygame
pygame.init()

#create the screen
screen=pygame.display.set_mode((800,600))

#Background
background=pygame.image.load("5.png")

#Background music


#Title and Icon
pygame.display.set_caption("Space Invaders")
icon=pygame.image.load("1.png")
pygame.display.set_icon(icon)


#player
playerImge=pygame.image.load("2.png")
playerX=370
playerY=480
playerX_change=0

#Enemy
enemyImge=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
num_of_enemy=6

for i in range(num_of_enemy):
    enemyImge.append(pygame.image.load("3.png"))
    enemyX.append(random.randint(0,800))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(4)
    enemyY_change.append(40)

#Bullet
bulletImge=pygame.image.load("6.png")
bulletX=0
bulletY=480
bulletX_change=0
bulletY_change=10
bullet_state="ready"  #can't see bullet

#Score

score_value=0
font=pygame.font.Font('freesansbold.ttf',30)

textX=10
textY=10

#Game over text
over_font=pygame.font.Font('freesansbold.ttf',64)

def show_score(x,y):
    score=font.render("Score  :"+str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))

def game_over_text():
    over_text=font.render('GAME OVER',True,(255,255,255))
    screen.blit(over_text, (300, 250))

def player(x,y):
    screen.blit(playerImge,(x,y))

def enemy(x,y,i):
    screen.blit(enemyImge[i],(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state="fire"
    screen.blit(bulletImge,(x+16,y+10))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance=math.sqrt(math.pow(enemyX-bulletX,2)+(math.pow(enemyY-bulletY,2)))
    if distance<27:
        return True
    else:
        return False

#game loop
running=True
while running:

    #background color
    screen.fill((0, 0, 0))
    #background image
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

        #if keystrock is pressed check whether its right or left
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                playerX_change=-5
            if event.key==pygame.K_RIGHT:
                playerX_change =5
            if event.key==pygame.K_SPACE:
                if bullet_state=="ready":
                   #get the current cordinate of the spaceship
                  bulletX=playerX
                  fire_bullet(bulletX,bulletY)

        if event.type==pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key==pygame.K_RIGHT:
                playerX_change = 0  #place use to stop

    #Player Movement
    playerX+=playerX_change

    if playerX <=0:
            playerX=0
    elif playerX>=736:
            playerX=736 #How stop at the boundry


    #Enemy Movement
    for i in range(num_of_enemy):

        #Game over
        if enemyY[i]>420:
            for j in range(num_of_enemy):
                enemyY[j]=2000

            game_over_text()
            break


        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
           enemyX_change[i] = 4
           enemyY[i]+=enemyY_change[i]
        elif enemyX[i] >= 736:
           enemyX_change[i] = -4  # How stop at the boundry
           enemyY[i]+=enemyY_change[i]

     # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            print(score_value)
            enemyX[i] = random.randint(0, 800)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i],enemyY[i],i)



    #bullet movement
    if bulletY<=0:
        bulletY=480
        bullet_state="ready"

    if bullet_state == "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change



    player(playerX,playerY)
    show_score(textX,textY)
    pygame.display.update()