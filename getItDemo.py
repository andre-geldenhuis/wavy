#! /usr/bin/env python

from __future__ import division

from random import randint
from math import sqrt

import pygame
from pygame.locals import *

from wavy.WavyGame import WavySoundGame


class getItGame(WavySoundGame):
    
    def __init__(self, title = 'a test', config_file = './wavy.conf'):
        super(WavySoundGame, self).__init__(config_file, title)
        self.init()
    
    def fetchConfig(self):
        "Simple implementation of fetch config method, should be overloaded"
        self.RETINA_FILE = self.CONFIG.get('GAME', 'RETINA_FILE')
        self.WIDTH = self.CONFIG.getint('GAME', 'WIDTH')
        self.HEIGHT = self.CONFIG.getint('GAME', 'HEIGHT')
        self.FS = self.CONFIG.getint('SONIFICATION', 'FS')
        self.AMP = self.CONFIG.getfloat('SONIFICATION', 'AMP')
        self.FREQ_MIN = self.CONFIG.getfloat('SONIFICATION', 'FREQ_MIN')
        self.FREQ_MAX = self.CONFIG.getfloat('SONIFICATION', 'FREQ_MAX')
        self.MAX_TIME = self.CONFIG.getfloat('SONIFICATION', 'MAX_TIME')

    def main(self):
        X_SIZE = self.WIDTH
        Y_SIZE = self.HEIGHT
        POK_SIZE = (100, 25)
        POK_YPOS = Y_SIZE - 20
        BALL_SIZE = (30, 30)
        BALL_SPEED = 1

        LEVEL = 1
        SCORE = 0
        GOTIT = 10
        LOSEIT = -5

        screen =self.SCREEN

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
