#! /usr/bin/env python

from __future__ import division

from random import randint
from math import sqrt

import pygame
from pygame.locals import *
from pygame.surfarray import array2d, pixels2d
from psychopy import *

from wavy.WavyGame import WavySoundGame


class psychopyWrapper(WavySoundGame):
    
    def __init__(self, winHandle, title = 'a test', config_file = './wavy.conf'):
        super(WavySoundGame, self).__init__(config_file, title)
        self._winHandle = winHandle
        self.init()
    
    def display_INIT(self):
        self.SCREEN = pixels2d(self._winHandle)

    def refresh(self):
        self.RETINA.update()

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


def main():
    #create a window to draw in
    myWin = visual.Window((600,600), allowGUI=False, winType = 'pygame')
    ppw = psychopyWrapper(myWin.winHandle)

    #INITIALISE SOME STIMULI
    grating1 = visual.PatchStim(myWin,mask="gauss",
    rgb=[1.0,1.0,1.0],opacity=1.0,
    size=(1.0,1.0), sf=(4,0), ori = 45)
    grating2 = visual.PatchStim(myWin,mask="gauss",
    rgb=[1.0,1.0,1.0],opacity=0.5,
    size=(1.0,1.0), sf=(4,0), ori = 135)

    trialClock = core.Clock()
    t = 0
    while t<20:#quits after 20 secs

        t=trialClock.getTime()
        
        grating1.setPhase(1*t)  #drift at 1Hz
        grating1.draw()  #redraw it
        
        grating2.setPhase(2*t)    #drift at 2Hz
        grating2.draw()  #redraw it
    
        myWin.flip()          #update the screen
        ppw.refresh()

        #handle key presses each frame
        for keys in event.getKeys():
            if keys in ['escape','q']:
                core.quit()


if __name__ == '__main__':
    main()
