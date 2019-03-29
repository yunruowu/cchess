import pygame
from pygame.locals import *
from sys import exit
background_image = 'image/xia.jpg'
screen = pygame.display.set_mode((640,480),0,32)
background = pygame.image.load(background_image).convert()

Fullscreen = False

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            if event.key == K_f:
                Fullscreen = not Fullscreen
                if Fullscreen:
                    screen = pygame.display.set_mode((640,480),FULLSCREEN,32)
                else:
                    screen = pygame.display.set_mode((640,480),0,32)
    screen.blit(background,(0,0))
    pygame.display.update()