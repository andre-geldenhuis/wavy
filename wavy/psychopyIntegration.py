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


class PsychopyWrapper(WavySoundGame):
    
    def __init__(self, winHandle, title = 'a test', config_file = './wavy.conf'):
        super(WavySoundGame, self).__init__(config_file, title)
        self.WIN_HANDLE = winHandle
        self.init()
    
    def display_INIT(self):
        self.INPUT_FIELD = pixels2d(self.WIN_HANDLE)

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
