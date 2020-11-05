# Space Invaders in python using pygame

# ------------------------------------------------------------------------------------------------------------------------- #

import pygame
import random
import time
import os
# import sys

# ------------------------------------------------------------------------------------------------------------------------- #

pygame.font.init()

WIDTH, HEIGHT = 400, 700
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Space Invaders')

PLAYER_SHIP = pygame.image.load(
    os.path.join('assets', 'pixel_ship_yellow.png'))
ENEMY_SHIP = pygame.transform.flip(pygame.image.load(
    os.path.join('assets', 'pixel_ship_red_small.png')), True, True)
BG = pygame.transform.scale2x(pygame.image.load(
    os.path.join('assets', 'background-black.png')))
LASER = pygame.image.load(os.path.join('assets', 'pixel_laser_yellow.png'))

shipx = 150
shipy = 600
player_vel = 5
enemy_vel = 3
space_vel = 2
total_enemies = 5
frame_rate = 30

GAME_FONT = pygame.font.SysFont("comicsans", 50)

# ------------------------------------------------------------------------------------------------------------------------- #


class Space:
    height = BG.get_height()
    img = BG

    def __init__(self):
        self.y1 = 0
        self.y2 = -self.height

    def move(self):
        self.y1 += space_vel
        self.y2 += space_vel

        if self.y1 == self.height:
            self.y1 = self.y2 - self.height

        if self.y2 == self.height:
            self.y2 = self.y1 - self.height

    def draw(self, win):
        win.blit(self.img, (0, self.y1))
        win.blit(self.img, (0, self.y2))

# ------------------------------------------------------------------------------------------------------------------------- #


class Enemy(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.mask = pygame.mask.from_surface(ENEMY_SHIP)

    def move(self):
        self.y += enemy_vel

    def draw(self, win):
        win.blit(ENEMY_SHIP, (self.x, self.y))

# ------------------------------------------------------------------------------------------------------------------------- #


class Ship(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.mask = pygame.mask.from_surface(PLAYER_SHIP)

    def move_left(self):
        self.x -= player_vel

    def move_right(self):
        self.x += player_vel

    def draw(self, win):
        win.blit(PLAYER_SHIP, (self.x, self.y))

# ------------------------------------------------------------------------------------------------------------------------- #


class Laser(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.mask = pygame.mask.from_surface(LASER)

    def move(self):
        self.y -= 5

    def draw(self, win):
        win.blit(LASER, (self.x, self.y - 45))

# ------------------------------------------------------------------------------------------------------------------------- #


def collide(o1, o2):
    xoff = o2.x - o1.x
    yoff = o2.y - o1.y
    return o1.mask.overlap(o2.mask, (xoff, yoff)) != None

# ------------------------------------------------------------------------------------------------------------------------- #


def main():
    run = True
    global shipx, shipy, total_enemies
    ship = Ship(shipx, shipy)
    space = Space()
    score = 0
    enemies = []
    lasers = []
    lives = 5
    counter = 0
    clock = pygame.time.Clock()

    while run:
        clock.tick(frame_rate)
        space.move()
        space.draw(display)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                # pygame.quit()

            if keys[pygame.K_SPACE]:
                lasers.append(Laser(ship.x, ship.y))

        # ----------------------------------------------------------------------- #
        # checks for the total enemies and increments score and makes a new wave
        if len(enemies) == 0:
            # score += 1
            total_enemies += 1
            for _ in range(total_enemies):
                enemies.append(Enemy(random.randrange(
                    10, WIDTH - ENEMY_SHIP.get_width() - 10), random.randrange(-1500, -100)))

        # ----------------------------------------------------------------------- #
        # controls:
        if (keys[pygame.K_LEFT] and ship.x > 0):
            ship.move_left()

        elif (keys[pygame.K_RIGHT] and ship.x + PLAYER_SHIP.get_width() < WIDTH):
            ship.move_right()

        if lives == 0:
            lost_text = GAME_FONT.render('You Lost!', 3, (255, 255, 255))
            display.blit(lost_text, ((WIDTH // 2) -
                                     (lost_text.get_width() // 2), 50))
            counter += 1

        if counter == 30:
            time.sleep(2)
            run = False

        # ----------------------------------------------------------------------- #
        # collision logic:

        for enemy in enemies:
            for laser in lasers:
                if collide(laser, enemy):
                    score += 1
                    enemies.remove(enemy)
                    lasers.remove(laser)
                    break

        # for enemy in enemies:
        #     if collide(enemy, ship):
        #         lives -= 1
        #         continue

        for laser in lasers:
            laser.move()
            laser.draw(display)
            if laser.y + LASER.get_height() < 0:
                lasers.remove(laser)
                continue

        for enemy in enemies:
            enemy.move()
            enemy.draw(display)
            if enemy.y > HEIGHT:
                enemies.remove(enemy)
                lives -= 1
                continue

        # ----------------------------------------------------------------------- #

        lives_text = GAME_FONT.render(
            "Lives: " + str(lives), 1, (255, 255, 255))
        score_text = GAME_FONT.render(
            "Score: " + str(score), 1, (255, 255, 255))
        display.blit(lives_text, (10, 10))
        display.blit(score_text, (WIDTH - 10 - score_text.get_width(), 10))
        ship.draw(display)
        pygame.display.flip()

    # for debugging purposes
    print(len(lasers))
    print(len(enemies))
    print(lives)

# ------------------------------------------------------------------------------------------------------------------------- #

# calling the function to run the game loop


if __name__ == '__main__':
    main()

# ------------------------------------------------------------------------------------------------------------------------- #


