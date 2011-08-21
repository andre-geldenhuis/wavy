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
This module contain classes needed to build a minimal sensosry substitution system.
Retina         - Genral container, control input sampling and output
ReceptiveField - Unitary area of input to be sampled 
SoundRF        - Sonification oriented ReceptiveField
'''

from __future__ import division

from threading import Thread

import pygame
import numpy as np

try:
    from OpenGL.GL import glReadPixels, GL_LUMINANCE, GL_FLOAT
except ImportError:
    HAS_GL = False
else:
    HAS_GL = True


class Retina(Thread):
    '''
    Retina class is the core of the sensory substitution system.
    It carry out sampling from an INPUT_FIELD (numpy array), compute new activity for each receptive fields
    and call ReceptiveFields' output method.
    '''
    
    def __init__(self, file_name, rf_model, input_array):
        '''
        Constructor :
        -------------
        file_name     : file name of the retina file which contain sampling parameters
        rf_model      : ReceptiveField class to be used in sensory substitution process
        input_array   : numeric array to be sampled (numpy array)
        '''
        Thread.__init__(self)
        self._x_size = None
        self._y_size = None
        self._rf_list = []
        self._rf_model = rf_model
        self._input_field = input_array
        self._init_retina(file_name)
        self._nbr_rf = len(self._rf_list)
        
    def _init_retina(self, file_name):
        "Read the retina file and setup all Receptive Fields according to retina file's data"
        try:
            fRetina = open(str(file_name), 'r')
            
        except IOError:
            print('E: No such retina file : %s' % file_name)
            exit(1)

        retina_data = fRetina.readlines()            
        fRetina.close()

        # Read data X and Y
        data = retina_data.pop(0).split(';')
        self._x_size = int(data[0])
        self._y_size = int(data[1])
        nb_lines = len(retina_data)
        
         # Reading file: first line (Recpetive Field position), second line (Captors list position)
        c1 = 0
        while c1 < nb_lines - 1:
            data_rf = retina_data.pop(0).split(';')
            data_caps = retina_data.pop(0).split(';')
            X = int(data_rf[0])
            Y = int(data_rf[1])
            cap_list = []
            nb_cap = len(data_caps)
            
            # Read capors' position (x, y)
            c2 = 0
            while c2 < nb_cap - 1:
                x = int(data_caps.pop(0))
                y = int(data_caps.pop(0))
                cap_list.append((x, y))
                c2 += 2
                
            rf = self._rf_model(X, Y, cap_list, self)
            self._rf_list.append(rf)
            c1 += 2                    
                          
    def update(self, gl_get = False):
        '''
        Update each Receptive Field and output them
        gl_get is a boolean flag to specify if the video buffer have to be read from openGL buffer.
        '''
        for rf in self._rf_list:
            rf.update(gl_get)
            rf.output()


class ReceptiveField(Thread):
    '''
    A Receptive Field object is a part of a Retina.
    It is defined by its position and a list of captor sampling the Retina's INPUT_FIELD
    *** The output method must be implemented ***
    '''
    
    def __init__(self, x, y, cap_list, retina, threshold = 0):
        '''
        Constructor :
        -------------
        x, y      : (x, y) position of the ReceptiveField
        cap_list  : captors list
        retina    : reference of a retina instance
        treshold  : treshold parameter [0; 255]
        '''
        Thread.__init__(self)
        self._x = x
        self._y = y
        self._cap_list = cap_list
        self._nbr_cap = len(cap_list)
        self._threshold = threshold
        self._retina = retina
        self._input_field = retina._input_field
        self._activity = 0.
        self._gl = False
        
    def _t_func(self, initial_activity):
        "Threshold transfert function"
        if initial_activity > self._threshold:
            return initial_activity
        else:
            return 0

    def update(self, gl_get = False):
        '''
        Update samples input accordingly to the retina's input field <numpy array>
        gl_get is a boolean flag to specify if the video buffer have to be read from openGL buffer.
        '''

        activity = 0.
        
        for cap in self._cap_list:
            if gl_get:
                v = glReadPixels(cap[0], cap[1], 1, 1, GL_LUMINANCE, GL_FLOAT)
                v = round(v * 255)
            else:
                v = self._input_field[cap[0], cap[1]]
            activity += v

        self._activity = self._t_func(activity / (255 * self._nbr_cap))
        self.output()

    def output(self):
        "Abstract output method"
        raise NotImplementedError
        
        
class SoundRF(ReceptiveField):
    '''
    SoundRF is a class implementing an audio output ReceptiveField class.
    It is defined by same parameters than base class and by audio parameters.
    '''

    def __init__(self, x, y, cap_list, retina, threshold = 0):
        '''
        Constructor :
        -------------
        same as ReceptiveField class
        
        Audio parameters :
        ------------------
        freq_min, freq_max : frequency span
        max_time           : playing time in seconds
        amp                : amplitude factor
        fs                 : sampling frequence
        '''
        super(SoundRF, self).__init__(x, y, cap_list, retina, threshold)
        self._nb_chans = 2
        self._freq_span = None
        self._max_time = None
        self._amp = None
        self._fs = None
        self._tone = None
        self._pan = None
        self._sine = None
        self._sound = None
        self._chnl = None
        
    def _make_sinwave(self, tone):
        "Create the sinewave to be output"
        sinewave = np.array(self._amp * np.sin(tone * np.pi * np.arange(0, self._max_time, 1/self._fs)), dtype = np.int16)
        if self._nb_chans == 2:
            sinewave = np.array([sinewave]*2, dtype = np.int16)
        return sinewave
        
    def set_audio_params(self, freq_min, freq_max, max_time, amp = 10000, fs = 44100, flip_y = False):
        "Setup audio paramters according to the receptive field specifications"
        self._freq_span = freq_max - freq_min
        self._max_time = max_time
        self._amp = amp
        self._fs = fs
        if not flip_y:
            self._tone = freq_max - (self._y / self._retina._y_size * self._freq_span)
        else:
            self._tone = freq_min + (self._y / self._retina._y_size * self._freq_span)

        self._pan = [.5 + (.5 - float(self._x)/self._retina._x_size), .5 + (float(self._x)/self._retina._x_size - .5)]   
        self._sine = self._make_sinwave(self._tone)
        self._sound = pygame.sndarray.make_sound(self._sine.T)
        self._chnl = pygame.mixer.find_channel()
        self._chnl.play(self._sound, loops = -1)
        self._chnl.set_volume(0, 0)
        # print('RF object inited - x: %d, y: %d, on %s' % (self._x, self._y, self._chnl))
        
    def output(self):
        "Sonification method"
        left = self._pan[0] * self._activity
        right = self._pan[1] * self._activity 
        self._chnl.set_volume(left, right)
