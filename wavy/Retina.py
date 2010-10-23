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
This module contain classes needed to build a sensosry substitution system.
Retina - genral container and control object
ReceptiveField - sampling unit
'''
from __future__ import division

from threading import Thread

import pygame
import numpy as np


class Retina(Thread):
    '''
    Retina class is the core of the sensory substitution system.
    It carry out sampling on an INPUT_FIELD (numpy array), compute new value for each receptive-fields
    and call ReceptiveFields' output method.

    Constructor :
    -------------
    file_name     : file name of the retina file which contain sampling parameters
    rf_model      : ReceptiveField class to use in sensory substitution
    input_array   : numeric array to be sampled (numpy array)
    '''
    
    def __init__(self, file_name, rf_model, input_array):
        "Constructor"
        Thread.__init__(self)
        self.X_SIZE = None
        self.Y_SIZE = None
        self.RF_LIST = []
        self.RF_MODEL = rf_model
        self.INPUT_FIELD = input_array
        self.initRetina(file_name)
        self.NBR_RF = len(self.RF_LIST)
        
    def initRetina(self, file_name):
        "Read the retina file and setup all Receptive Fields according to retina file data's"
        try:
            fRetina = open(str(file_name), 'r')
            
        except IOError:
            print('E: No such retina file : %s' % file_name)
            exit(1)

        retina_data = fRetina.readlines()            
        fRetina.close()

        # Read data X and Y
        data = retina_data.pop(0).split(';')
        self.X_SIZE = int(data[0])
        self.Y_SIZE = int(data[1])
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
                
            rf = self.RF_MODEL(X, Y, cap_list, self)
            self.RF_LIST.append(rf)
            c1 += 2                    

    def getNum_RF(self):
        "Return the number of Receptive Fields set into the retina"
        return self.NBR_RF
                          
    def update(self):
        "Update each Receptive Field and output them"
        for rf in self.RF_LIST:
            rf.update()
            rf.output()


class ReceptiveField(Thread):
    '''
    A Receptive Field object is a part of a Retina.
    It is defined by its position and a list of captor sampling the Retina's INPUT_FIELD
    *** The output method must be implemented ***

    Constructor :
    -------------
    x, y      : (x, y) position of the ReceptiveField
    cap_list  : captors list
    retina    : instancied Retina reference
    treshold  : treshold parameter [0 ; 255]
    '''
    
    def __init__(self, x, y, cap_list, retina, threshold = 0):
        "Constructor"
        Thread.__init__(self)
        self.X = x
        self.Y = y
        self.CAP_LIST = cap_list
        self.NBR_CAP = len(cap_list)
        self.THRESHOLD = threshold
        self.RETINA = retina
        self.INPUT_FIELD = retina.INPUT_FIELD
        self.ACTIVITY = 0.
        
    def t_func(self, initial_activity):
        "Transfert function"
        if initial_activity > self.THRESHOLD:
            return initial_activity
        else:
            return 0

    def update(self):
        "Update samples input accordingly to the numeric input <array>"
        activity = 0.
        
        for cap in self.CAP_LIST:
            v = self.INPUT_FIELD[cap[0], cap[1]]
            activity += v

        self.ACTIVITY = self.t_func(activity / (255 * self.NBR_CAP))
        self.output()

    def output(self):
        "Generic output method"
        raise NotImplementedError
        
        
class SoundRF(ReceptiveField):
    '''
    SoundRF is a class implementing a Sound output ReceptiveField class.
    As a ReceptiveField derivative it take place as part of a Retina.
    It is define by its position and a list of captor sampling the Retina's INPUT_FIELD.

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

    def __init__(self, x, y, cap_list, retina, threshold = 0):
        "Constructor"
        super(SoundRF, self).__init__(x, y, cap_list, retina, threshold)
        self.NB_CHANS = 2
        self.FREQ_SPAN = None
        self.MAX_TIME = None
        self.AMP = None
        self.FS = None
        self.TONE = None
        self.PAN = None
        self.SINE = None
        self.SOUND = None
        self.CHNL = None
        
    def setAudioParams(self, freq_min, freq_max, max_time, amp = 10000, fs = 44100):
        "Setup audio paramters for the Receptive Field instance. This is an example, should be overloaded."
        self.FREQ_SPAN = freq_max - freq_min
        self.MAX_TIME = max_time
        self.AMP = amp
        self.FS = fs
        self.TONE = freq_max - (self.Y / self.RETINA.Y_SIZE * self.FREQ_SPAN)
        self.PAN = [.5 + (.5 - float(self.X)/self.RETINA.X_SIZE), .5 + (float(self.X)/self.RETINA.X_SIZE - .5)]
        self.SINE = self.mkSineWave(self.TONE)
        self.SOUND = pygame.sndarray.make_sound(self.SINE.T)
        self.CHNL = pygame.mixer.find_channel()
        self.CHNL.play(self.SOUND, loops = -1)
        self.CHNL.set_volume(0, 0)
        print('RF object inited - x: %d, y: %d, on %s' % (self.X, self.Y, self.CHNL))

    def mkSineWave(self, tone):
        "Create a sinewave to be output"
        sinewave = np.array(self.AMP * np.sin(tone * np.pi * np.arange(0, self.MAX_TIME, 1/self.FS)), dtype = np.int16)
        if self.NB_CHANS == 2:
            sinewave = np.array([sinewave]*2, dtype = np.int16)
        return sinewave
        
    def output(self):
        "Sound output method"
        left = self.PAN[0] * self.ACTIVITY
        right = self.PAN[1] * self.ACTIVITY 
        self.CHNL.set_volume(left, right)
