#! /usr/bin/env python

from __future__ import division

from random import randint
from math import sqrt

import pygame
from pygame.locals import *
from pygame.surfarray import array2d, pixels2d

try:
    from psychopy import *
except ImportError:
    print("PsychoPy not available on this system !!!")
    exit(1)

from wavy.WavyGame import ExternalWrapper

def main():
    #create a window to draw in
    myWin = visual.Window((640,480), allowGUI=True, winType = 'pygame')
    ppw = ExternalWrapper(myWin.winHandle, gl = True)

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
