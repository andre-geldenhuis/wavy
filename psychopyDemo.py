#! /usr/bin/env python

from psychopy import *

from wavy.psychopyIntegration import PsychopyWrapper


class myPsychopyExperiment(PsychopyWrapper):

    def __init__(self):
        super(PsychopyWrapper, self).__init__('wavy.conf', 'Psychopywrapper')

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

    def main(self):
        
        #INITIALISE SOME STIMULI
        grating1 = visual.PatchStim(self.SCREEN,mask="gauss",
                                    rgb=[1.0,1.0,1.0],opacity=1.0,
                                    size=(1.0,1.0), sf=(4,0), ori = 45)
        grating2 = visual.PatchStim(self.SCREEN,mask="gauss",
                                    rgb=[1.0,1.0,1.0],opacity=0.5,
                                    size=(1.0,1.0), sf=(4,0), ori = 135)
        
        trialClock = core.Clock()
        t = 0

        while t<20:#quits after 20 secs
            
            t=trialClock.getTime()
            
            grating1.setPhase(1*t)  #drift at 1Hz
            grating1.draw()  #redraw it
            
            grating2.setPhase(2*t)    #drift at 2Hz
            grating2.draw()  #redraw it
            
            myWin.flip()          #update the screen
            
            #handle key presses each frame
            for keys in event.getKeys():
                if keys in ['escape','q']:
                    core.quit()
                    

if __name__ == '__main__':
    exp = myPsychopyExperiment()
    exp.main()
