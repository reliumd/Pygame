import time
import pygame
import math
import random
from pygame import mixer

# Initialize pygame
pygame.init()

# Create screen
screen = pygame.display.set_mode((800, 738))

# Background
background = pygame.image.load('Cosmic.png')


# Title and Icon
pygame.display.set_caption("Akikasai")
icon = pygame.image.load('fire.png')
pygame.display.set_icon(icon)

# Player
player_image = pygame.image.load('Eliane.jpg')
playerX = 370
playerY = 600
playerX_change = 0

# Enemy
enemy_image = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemy_image.append(pygame.image.load('Renfeld.jpg'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(40, 140))
    enemyX_change.append(0.1)
    enemyY_change.append(40)

# Bullet
bullet_image = pygame.image.load('fireball.png')
bulletX = 0
bulletY = 550
bulletX_change = 0
bulletY_change = 0.3
bullet_state = 'ready'

# Font
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)
textX = 10
textY = 10

# Background Sound 
mixer.music.load('EP_backgound.ogg')
mixer.music.play(0)
    

# Game Over text
over_font = pygame.font.Font('freesansbold.ttf',64)

def show_score(x,y):
    score = font.render("Score : " + str(score_value), True, (255,255,255))
    screen.blit(score, (x,y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255,0,0))
    screen.blit(over_text, (200,250))


def winning_text():
    over_text = over_font.render("YOU WIN", True, (255,0,0))
    screen.blit(over_text, (250,270))


def player(x, y):
    screen.blit(player_image, (x, y))

def enemy(x, y, i):
    screen.blit(enemy_image[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_image, (x + 1, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))
    if distance < 35:
        return True
    else:
        return False
    


running = True
while running:
    screen.fill((0, 255, 0))
    #Background image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # If key stroke is pressed, check whether it is left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('fireball_sound.mp3')
                    bullet_sound.play()                    
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

# Enemy movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 500:
            for j in range (num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        elif score_value == 1:
            winning_text()
            break

        enemyX[i] += enemyX_change[i]  
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.15
            enemyY[i] += enemyY_change[i]  
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.15
            enemyY[i] += enemyY_change[i]
        
        # Collision        
        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            explosion_Sound = mixer.Sound('NPC_die_male.wav')
            explosion_Sound.play()
            bulletY = 550
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(40, 140)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= 0:
        bulletY = 550
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
