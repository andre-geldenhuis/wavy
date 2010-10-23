# -*- coding: utf-8 -*-

#    Copyright 2010, Nicolas Louveton <nblouveton@gmail.com>
#
#    This file is part of Wavy.
#
#    Wavy is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Wavy is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Wavy.  If not, see <http://www.gnu.org/licenses/>.

'''
theWave is a sensory substitution system to be used with a digital camera like an usb webcam.
The visual-to-sound substitution is performed onto the picture captured by the digital camera.
The input pictures are also displayed on the screen in real time.
'''

from __future__ import division

import sys
from threading import Thread
import ConfigParser

import pygame
from pygame.locals import *
from pygame.surfarray import array2d

import opencv
from opencv import highgui
 
from Retina import Retina, SoundRF
from WavyGame import WavySoundGame


class TheWaveMachine(WavySoundGame):
    '''
    TheWaveMachine < is a WavySoundGame sub-class.
    It is a visual-to-sound sensory substitution system for digital camera devices.
    It take no argument to be inited.
    It rely on the < wavy.conf > config file which must be in the same directory.
    There is one < main > method to be called in order to start system.
    '''

    def __init__(self):
        'Constructor'
        super(WavySoundGame, self).__init__('wavy.conf', 'theWave')
        self.CAMERA = highgui.cvCreateCameraCapture(0)
        self.FPS = 22
        self.init()

    def display_INIT(self):
        'Initialize display'
        pygame.display.init()
        self.SCREEN = pygame.display.set_mode((self.WIDTH, self.HEIGHT), 0, 8)
        pygame.display.set_caption(self.TITLE)
        self.INPUT_FIELD = array2d(self.SCREEN) # surface locking prevent the use of array reference here
                                                # using a copy method instead (performance loss)
    
    def fetchConfig(self):
        "fetchingConfig file according to WavySoundGame class audio paramters"
        self.RETINA_FILE = self.CONFIG.get('GAME', 'RETINA_FILE')
        self.WIDTH = self.CONFIG.getint('GAME', 'WIDTH')
        self.HEIGHT = self.CONFIG.getint('GAME', 'HEIGHT')
        self.FS = self.CONFIG.getint('SONIFICATION', 'FS')
        self.AMP = self.CONFIG.getfloat('SONIFICATION', 'AMP')
        self.FREQ_MIN = self.CONFIG.getfloat('SONIFICATION', 'FREQ_MIN')
        self.FREQ_MAX = self.CONFIG.getfloat('SONIFICATION', 'FREQ_MAX')
        self.MAX_TIME = self.CONFIG.getfloat('SONIFICATION', 'MAX_TIME')

    def refresh(self):
        'Refreshing display and retina state'
        self.RETINA.INPUT_FIELD = array2d(self.SCREEN)  # copy by value (see above)
        for rf in self.RETINA.RF_LIST:
            rf.INPUT_FIELD = self.RETINA.INPUT_FIELD    # updating rf copy by reference
        self.RETINA.update()
        pygame.display.update()
                
    def get_image(self):
        'Dump a picture nfrom video capture'
        im = highgui.cvQueryFrame(self.CAMERA)
        return opencv.adaptors.Ipl2PIL(im)
    
    def t_func(self, data):
        'Generic transfert method, implement an identity function here'
        return data

    def main(self):
        'Main method'
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == QUIT:
                    sys.exit(0)
                    
            im = self.t_func(self.get_image())
            pg_img = pygame.image.frombuffer(im.tostring(), im.size, im.mode)
            self.SCREEN.blit(pg_img, (0,0))
            self.refresh()
            pygame.time.delay(int(1000 * 1.0/self.FPS))  
