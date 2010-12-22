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
psychopyIntegration is a module providing PsychopyWrapper class enabling
sensory substitution with Wavy library coupled with a psychopy experiment.
'''

from __future__ import division

from psychopy import *
from pygame.surfarray import array2d, pixels2d
 
from WavyGame import WavySoundGame


class ExternalWrapper(WavySoundGame):
    
    def __init__(self, field_handle, title = 'a test', config_file = './wavy.conf', gl = True):
        super(WavySoundGame, self).__init__(config_file, title, gl)
        self._field_handle = field_handle
        self.init()
    
    def _display_init(self):
        pass

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
        
    def refresh(self):
        self._retina.update(gl_get = True)
