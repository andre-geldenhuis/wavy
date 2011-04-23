#! /usr/bin/env python

from __future__ import division

from random import randint
from math import sqrt

import pygame
from pygame.locals import *

from wavy.WavyGame import WavySoundGame


class getItGame(WavySoundGame):
    
    def __init__(self, title = 'a test', config_file = './wavy.conf', gl = False, update_method = 'update'):
        super(WavySoundGame, self).__init__(config_file, title, gl, update_method)
        self.init()

    def main(self):
        X_SIZE = self._width
        Y_SIZE = self._height
        POK_SIZE = (100, 25)
        POK_YPOS = Y_SIZE - 20
        BALL_SIZE = (30, 30)
        BALL_SPEED = 1

        LEVEL = 1
        SCORE = 0
        GOTIT = 10
        LOSEIT = -5

        screen = self._screen

        # player
        xp, yp = 0, POK_YPOS
        
        # ball info
        xb, yb = 0, 0
        b_falling = False

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()

                if event.type == KEYDOWN:
                    if (event.key == K_ESCAPE):
                        exit()

                    if (event.key == K_f):
                        pygame.display.toggle_fullscreen()

                if (event.type == MOUSEMOTION):
                    xp = pygame.mouse.get_pos()[0]
            
            if (b_falling):
                yb += BALL_SPEED * LEVEL
                if (yb > yp - POK_SIZE[1] / 2):
                    b_falling = False
                    if (xb > xp - POK_SIZE[0] / 2) and (xb < xp + POK_SIZE[0] / 2):
                        SCORE += GOTIT
                    else:
                        SCORE -= LOSEIT
            elif (not b_falling):
                xb, yb = randint(0, X_SIZE), 0
                b_falling = True

            # filling background
            screen.fill((0, 0, 0))

            # drawing player
            POK_RECT = pygame.Rect(xp - POK_SIZE[0] / 2, yp - POK_SIZE[1] / 2, POK_SIZE[0], POK_SIZE[1])
            pygame.draw.rect(screen, (255, 255, 255), POK_RECT)
            
            BALL_RECT = pygame.Rect(xb - BALL_SIZE[0] / 2, yb - BALL_SIZE[1] / 2, BALL_SIZE[0], BALL_SIZE[1])
            pygame.draw.rect(screen, (255, 255, 255), BALL_RECT)

            # terminating loop and refreshing
            self.refresh()


if __name__=='__main__':
    getit = getItGame()
    getit.main()
