#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
PointingGame is an example of sensory substitution
game (or experiment) made possible by wavy.

A white circle appears randomly on the screen. Player
have to move with mouse an equivalent circle just above
the former one.

When s/he thinks it's ok, s/he can press 'space' key to
record its performance (x and y error) (pointingOut.dat file)
and start a new trial. 
'''

from __future__ import division

from random import randint
from math import sqrt

import pygame
from pygame.locals import *

from wavy.WavyWrappers import WavySoundGame


class PointingGame(WavySoundGame):
    
    def __init__(self, title = 'a test', config_file = './wavy.conf', log_file = None):
        WavySoundGame.__init__(self, config_file, title, log_file = log_file)
        self.init()

    def main(self):
        X_SIZE = self._width
        Y_SIZE = self._height
        RADIUS = 50
        OUT_FILE = 'pointingOut.dat'
        screen =self._screen
        
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
    pg = PointingGame(log_file = 'wavy.log') #log_file = None, if you don't want to log retina's loop
    pg.main()
