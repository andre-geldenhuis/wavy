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
        self._camera = highgui.cvCreateCameraCapture(0)
        self._fps = 22
        self.init()

    def _display_init(self):
        'Initialize display'
        pygame.display.init()
        self._screen = pygame.display.set_mode((self._width, self._height), 0, 8)
        pygame.display.set_caption(self._title)
        self._input_field = array2d(self._screen) # surface locking prevent the use of array reference here
                                                # using a copy method instead (performance loss)

    def _t_func(self, data):
        'Generic transfert method, implement an identity function here'
        return data
      
    def _get_image(self):
        'Dump a picture nfrom video capture'
        im = highgui.cvQueryFrame(self._camera)
        return opencv.adaptors.Ipl2PIL(im)
          
    def refresh(self):
        'Refreshing display and retina state'
        self._retina._input_field = array2d(self._screen)  # copy by value (see above)
        for rf in self._retina._rf_list:
            rf._input_field = self._retina._input_field    # updating rf copy by reference
        self._retina.update()
        pygame.display.update()

    def main(self):
        'Main method'
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == QUIT:
                    sys.exit(0)
                    
            im = self._t_func(self._get_image())
            pg_img = pygame.image.frombuffer(im.tostring(), im.size, im.mode)
            self._screen.blit(pg_img, (0,0))
            self.refresh()
            pygame.time.delay(int(1000 * 1.0/self._fps))  
