#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
theWave.py script use wavy as a digitial video input
to auditory stream sensory substitution system.
It provide a similar system to theVibe.
'''

from wavy.thewavelib import TheWaveMachine

# Launching theWave
if __name__=='__main__':
    theWave = TheWaveMachine()
    theWave.main()
