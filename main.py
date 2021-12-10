import pygame as pg
import random
import math
# initialize pygame and access all the methods in it
pg.init()
# create screen where we state the with and height respectively
screen = pg.display.set_mode((800, 600))

# Title and icon
pg.display.set_caption("Space Fire")
# load icon image into game
icon = pg.image.load("icon.png")
pg.display.set_icon(icon)

# load player image into game
playerImg = pg.image.load("player.png")
playerX = 370
playerY = 480
playerX_change = 0


# To draw our player image on to the display screen
def player(x, y):
    screen.blit(playerImg, (x, y))


# load our enemy image into game
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

number_of_enemies = 6
# using a for loop to create a given number of enemies
for i in range(number_of_enemies):

    enemyImg.append(pg.image.load("enemy.png"))
    enemyX.append(random.randint(0, 740))
    enemyY.append(random.randint(0, 150))
    enemyX_change.append(2)
    enemyY_change.append(30)


# To draw our enemy image onto the display screen
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


# load bullet image into game
bulletImg = pg.image.load("bullet.png")
bulletX = 370
bulletY = 480
bulletX_change = 0
bulletY_change = 2
# the bullet_state variable is used to determine when and when not the bullet is visible on the screen
bullet_state = "ready"


def fire_bullet(x, y):
    # we declare the bullet_state variable as global to access it with in our function
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x+16, y+10))


# To find the distance  between the bullet and the enemy
def collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX-bulletX, 2) + math.pow(enemyY-bulletY, 2))
    if distance < 27:
        return True


# variable to record points scored
score = 0

# to display the scores on the game screen

font = pg.font.Font('freesansbold.ttf', 25)
textX = 10
textY = 10


# function to display our text on the display screen
def show_score(x, y):
    score_value = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_value, (x, y))


# game over text
game_over_font = pg.font.Font('freesansbold.ttf', 64)


def game_over():
    over = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over, (200, 250))


# game loop
game_on = True

while game_on:
    screen.fill((0, 0, 0))
    # loop through all events of the game
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_on = False
        # checking if the pressed keyboard key is the right or left key
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RIGHT:
                playerX_change = 0.2
            if event.key == pg.K_LEFT:
                playerX_change = -0.2
            if event.key == pg.K_SPACE:
                # To only fire another bullet when the previous bullet is out
                if bullet_state == "ready":
                    # To capture the current X positioning of the player to be used for the bulletX position
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pg.KEYUP:
            # To ensure movement stops once the keyboard key is released
            if event.key == pg.K_RIGHT or event.key == pg.K_LEFT:
                playerX_change = 0

    # adjusting our positioning depending on the keyboard stroke
    playerX += playerX_change
    # to limit the player not to go over our boundaries
    if playerX <= -11:
        playerX = -11
    elif playerX >= 750:
        playerX = 750

    # To deal with each enemy movement individually
    for i in range(number_of_enemies):
        # To determine game over
        if enemyY[i] > 420:
            # move all enemies off the screen
            for j in range(number_of_enemies):
                enemyY[j] = 2000
            game_over()
            break
        # execution to have the the enemy image moving
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= -11:
            # starts moving the enemy to the right when left boundary is reached
            enemyX_change[i] = 0.3
            # moves enemy down when the left boundary is reached
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 750:
            # starts moving enemy to left when right boundary is reached
            enemyX_change[i] = -0.3
            # moves enemy down when the right boundary is reached
            enemyY[i] += enemyY_change[i]

        # calling the collision function to determine distance
        collided = collision(enemyX[i], enemyY[i], bulletX, bulletY)
        # determining what needs to be done once the collision happens
        if collided:
            bulletY = 480
            bullet_state = "ready"
            score += 1

            # to draw a new enemy at a random position after collision
            enemyX[i] = random.randint(0, 740)
            enemyY[i] = random.randint(0, 150)

        enemy(enemyX[i], enemyY[i], i)

    player(playerX, playerY)
    show_score(textX, textY)

    # resetting bullet back to default to be able to fire another
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    # bullet movement when fired
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # This helps to always have the display window of the game updated
    pg.display.update()
