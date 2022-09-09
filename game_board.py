import pygame

import sys

import os

from pygame.locals import *


pygame.init()  # initialize pygame

clock = pygame.time.Clock()

screen = pygame.display.set_mode((600, 480))


# Load the background image here. Make sure the file exists!

bg = pygame.image.load(os.path.join("./", "background.png"))

pygame.mouse.set_visible(0)

pygame.display.set_caption('Space Age Game')


# fix indentation


while True:

    clock.tick(60)

    screen.blit(bg, (0, 0))

    x, y = pygame.mouse.get_pos()


    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            sys.exit()


    pygame.display.update()