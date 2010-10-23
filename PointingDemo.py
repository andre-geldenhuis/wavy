#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
PointingGame is an example of sensory substitution game (or experiment) made possible
by wavy.

The game make appearing a white circle on the screen. The user can move over the screen
a similar white circle and have to put it above the later one. Whene he/she think it's
he have to push escape button to record its performance and the same task appear again.

This application can be used to assess learning curve and favorise learning progression 
of a senosry substitution system.  
'''

from __future__ import division

from random import randint
from math import sqrt

import pygame
from pygame.locals import *

from wavy.WavyGame import WavySoundGame


class PointingGame(WavySoundGame):
    
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
        RADIUS = 50
        OUT_FILE = 'pointingOut.dat'
        screen =self.SCREEN
        
        outfile = open(OUT_FILE, 'w') # output file for recording performance
        outfile.write("DX\tDY\tDISTANCE\n")
        xs, ys = randint(0, X_SIZE), randint(0, Y_SIZE)
    
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()

                if event.type == KEYDOWN:
                    if (event.key == K_ESCAPE):
                        exit()

                    if (event.key == K_f):
                        pygame.display.toggle_fullscreen()

                    if (event.key == K_SPACE):
                        xy_out = pygame.mouse.get_pos()
                        x_out = xs - xy_out[0]
                        y_out = ys - xy_out[1]
                        d_out = sqrt(x_out**2 + y_out**2)
                        outfile.write("%d\t%d\t%d\n" % (x_out, y_out, d_out))
                        xs, ys = randint(0, X_SIZE), randint(0, Y_SIZE)

            screen.fill((0, 0, 0))
    
            pygame.draw.circle(screen, (255, 255, 255), (xs, ys), RADIUS, 0)
    
            x, y = pygame.mouse.get_pos()
            pygame.draw.circle(screen, (255, 255, 255), (x, y), RADIUS, 0)
    
            self.refresh()

        # end of the game
        outfile.close()


if __name__=='__main__':
    pg = PointingGame()
    pg.main()
