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
This module contain template classes to make sensury substitution
system building easier. 
WavyGame - a general class
WavySoundGame - an easy to use visual-to-sound classe
ExternalWrapper - a class to handle arbitrary external input
'''

from __future__ import division

from threading import Thread
import ConfigParser

import pygame
from pygame.surfarray import pixels2d

from Retina import Retina, SoundRF


class WavyWrapper(Thread):
    '''External wrapper use an external surface for sonification instead of a specific display. 
    Referenbce to a numpy array is requiered if opengl mode is false
    Constructor :
    -------------
    field_handle  : reference to an input array <numpy array>
    config_file   : configuration file to be load (optionnal, default: None)
    gl            : is display surface set with OPENGL mode 
    update_method : method to be used for dipsplay update ('update' or 'flip')    
    '''
    
    def __init__(self, input_handle, config_file = None, gl = False, update_method = 'update', log_file = None):
        '''
        Constructor
        '''
        Thread.__init__(self)
        self._height = None
        self._width = None
        self._input_field = input_handle
        self._retina = None
        self._config = ConfigParser.RawConfigParser()
        self._config_file = config_file
        self._gl = gl

        try:
            self._log_file = open(log_file)

        except IOError:
            print('ERROR !\nNo such log file found %s' % log_file)
            self._log_file = None

        if self._gl:
            assert HAS_GL, 'No OpenGL package found !'
            self._update_method = 'flip'
        else:
            self._update_method = update_method

    def _config_init(self):
        "Read the config file and fetch values"
        if self._config_file is not None:
            self._config.read(self._config_file)
            try:
                self._fetch_config()

            except ConfigParser.NoSectionError, section:
                print('ERROR !\nPlease check :  %s in config file %s' % (section, self._config_file))
                exit(1)

            except NotImplementedError:
                print('ERROR !\nfetchConfig is called without a correct implementation')
                exit(1)

            except IOError:
                print('ERROR !\nUnable to fetch config file : %s' % self._config_file)
                exit(1)
    
    def _fetch_config(self):
        "Generic method to fetch config file"
        raise NotImplementedError
                                  
    def _retina_init(self):
        "Generic method to setup Retina"
        raise NotImplementedError
                       
    def refresh(self):
        "Refresh screen and Retina"
        self._retina.update(self._gl, self._log_file)

    def init(self):
        "Generic init method"
        raise NotImplementedError
    
    def main(self):
        raise NotImplementedError


class WavyGame(WavyWrapper):
    '''
    WavyGame is a class to help you create easily a sensory substitution system for gaming.
    Many of methods of this class must be implemented in order to be used.

    Constructor :
    -------------
    config_file   : configuration file to be load (optionnal, default: None)
    title         : Title to be displayed onto the window's caption
    gl            : is display surface set with OPENGL mode 
    update_method : method to be used for dipsplay update ('update' or 'flip')
    '''

    def __init__(self, config_file = 'wavy.conf', title = 'Wavy Game Engine', gl = False, update_method = 'update'):
        '''
        Constructor
        '''
        WavyWrapper.__init__(self, None, config_file, gl, update_method)
        self._screen = None           # pyGame display reference
        self._title = title

    def _display_init(self):
        "Setup the display system"
        pygame.display.init()
        try:
            if not self._gl:
                self._screen = pygame.display.set_mode((self._width, self._height), 0, 8)
        
            else:
                self._screen = pygame.display.set_mode((self._width, self._height), pygame.OPENGL, 8)

        except TypeError:
            print('ERROR !\nInteger value expected :')
            print('%s is given for width' % type(self._width))
            print('%s is given for height' % type(self._height))
            exit(1)
            
        pygame.display.set_caption(self._title)
        self._input_field = pixels2d(self._screen)

    def _fetch_config(self):
        "Generic method to fetch config file"
        raise NotImplementedError
                                  
    def _retina_init(self):
        "Generic method to setup Retina"
        raise NotImplementedError
                       
    def refresh(self):
        "Refresh screen and Retina"

        if self._update_method == 'update':
            pygame.display.update()
        else:
            pygame.display.flip()

        if self._gl:
            self._retina.update(gl_get = True)
        else:
            self._retina.update()

    def init(self):
        "Generic init method"
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

    def __init__(self, config_file, title = 'Wavy Game Engine', gl = False, update_method = 'update'):
        "Constructor"
        WavyGame.__init__(self, config_file, title, gl, update_method)
        self._retina_file = None
        self._fs = None        # Audio parameters pre-init : required 
        self._freq_min = None  # a properly implemented _fetch_config method is needed
        self._freq_max = None
        self._amp = None
       
    def init(self):
        "General init: fetch config, setup retina, display and sound system"
        self._config_init()
        self._display_init()
        self._retina = Retina(self._retina_file, SoundRF, self._input_field)
        pygame.mixer.pre_init(self._fs, -16, 2, 1024*4)
        pygame.mixer.init()
        pygame.mixer.set_num_channels(self._retina._nbr_rf * 2)
        rfs = self._retina._rf_list
        for rf in rfs:
            rf.set_audio_params(self._freq_min, self._freq_max, self._max_time, \
                              self._amp, self._fs, flip_y = self._flip_y)

    def _fetch_config(self):
        "Simple implementation of fetch_config method, should be overloaded"
        self._retina_file = self._config.get('GAME', 'RETINA_FILE')
        self._width = self._config.getint('GAME', 'WIDTH')
        self._height = self._config.getint('GAME', 'HEIGHT')
        self._fs = self._config.getint('SONIFICATION', 'FS')
        self._amp = self._config.getfloat('SONIFICATION', 'AMP')
        self._freq_min = self._config.getfloat('SONIFICATION', 'FREQ_MIN')
        self._freq_max = self._config.getfloat('SONIFICATION', 'FREQ_MAX')
        self._max_time = self._config.getfloat('SONIFICATION', 'MAX_TIME')
        self._flip_y = self._config.getboolean('SONIFICATION', 'FLIP_Y')
