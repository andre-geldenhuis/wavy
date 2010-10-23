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

    def __init__(self, config_file = 'wavy.conf'):
        super(WavySoundGame, self).__init__(config_file, 'Psychopywrapper')
        self.init()
        
    def display_INIT(self):
        "Setup the display system"
        self.SCREEN =  visual.Window((self.HEIGHT, self.WIDTH), winType='pygame', allowGUI=False)
        self.INPUT_FIELD = pixels2d(self.SCREEN)

    def fetchConfig(self):
        'Virtual method for fetching configuration file'
        raise NotImplementedError

    def main(self):
        'Virtual main method'
        raise NotImplementedError
