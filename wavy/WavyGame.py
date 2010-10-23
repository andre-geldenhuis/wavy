#! -*- coding: utf-8 -*-

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
This module contain template classes to make sensury substitution system building easier.
WavyGame - a general class
WavySoundGame - an easy to use visual-to-sound classe
'''

from __future__ import division

from threading import Thread
import ConfigParser

import pygame
from pygame.surfarray import pixels2d

from Retina import Retina, SoundRF


class WavyGame(Thread):
    '''
    WavyGame is a class to help you create easily a sensory substitution system for gaming.
    Many of methods of this class must be implemented in order to be used.

    Constructor :
    -------------
    config_file : configuration file to be load (optionnal, default: None)
    title       : Title to be displayed onto the window's caption
    '''


    def __init__(self, config_file = None, title = 'Wavy Game Engine'):
        '''
        Constructor
        '''
        Thread.__init__(self)
        self.HEIGHT = None
        self.WIDTH = None
        self.SCREEN = None           # pyGame display reference
        self.INPUT_FIELD = None      # array reference to SCREEN
        self.RETINA = None
        self.CONFIG = ConfigParser.RawConfigParser()
        self.CONFIG_FILE = config_file
        self.TITLE = title

    def writeConfig(self):
        "Write the config file"
        try:
            f = open(str(self.CONFIG_FILE), 'w')

        except IOError:
            print('Unable to write config file : %s' % self.CONFIG_FILE)
            
        self.CONFIG.write(f)
        f.close()

    def config_INI(self):
        "Read the config file and fetch values"
        if self.CONFIG_FILE is not None:
            self.CONFIG.read(self.CONFIG_FILE)
            try:
                self.fetchConfig()

            except NotImplementedError:
                print('fetchConfig is called without a correct implementation')

            except IOError:
                print('Unable to fetch config file : %s' % self.CONFIG_FILE)
                exit(1)
    
    def display_INIT(self):
        "Setup the display system"
        pygame.display.init()
        self.SCREEN = pygame.display.set_mode((self.WIDTH, self.HEIGHT), 0, 8)
        pygame.display.set_caption(self.TITLE)
        self.INPUT_FIELD = pixels2d(self.SCREEN)
        
    def refresh(self):
        "Refresh screen and Retina"
        pygame.display.update()
        self.RETINA.update()

    def init(self):
        "Generic init method"
        raise NotImplementedError
    
    def fetchConfig(self):
        "Generic method to fetch config file"
        raise NotImplementedError
                                  
    def retina_INIT(self):
        "Generic method to setup Retina"
        raise NotImplementedError
               
    def main(self):
        raise NotImplementedError
    

class WavySoundGame(WavyGame):
    '''
    WavySoundGame is a class to help you to make an Vision-to-Sound sensory substitution for games.
    
    Constructor :
    -------------
    config_file : configuration file to be load (optionnal, default: None)
    title       : Title to be displayed onto the window's caption
    '''

    def __init__(self, config_file, title = 'Wavy Game Engine'):
        "Constructor"
        super(WavyGame, self).__init__(config_file, title)
        self.RETINA_FILE = None
        self.FS = None        # Audio parameters pre-init : required 
        self.FREQ_MIN = None  # a properly implemented fetchConfig method is needed
        self.FREQ_MAX = None
        self.AMP = None
       
    def init(self):
        "General init: fetch config, setup retina, display and sound system"
        self.config_INI()
        self.display_INIT()
        self.RETINA = Retina(self.RETINA_FILE, SoundRF, self.INPUT_FIELD)
        pygame.mixer.pre_init(self.FS, -16, 2, 1024*4)
        pygame.mixer.init()
        pygame.mixer.set_num_channels(self.RETINA.getNum_RF() * 2)
        rfs = self.RETINA.RF_LIST
        for rf in rfs:
            rf.setAudioParams(self.FREQ_MIN, self.FREQ_MAX, self.MAX_TIME, \
                              self.AMP, self.FS)
