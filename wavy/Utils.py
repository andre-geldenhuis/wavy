# -*- coding: utf-8

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
This module contain utilitary functions related to Retina object.
'''

from random import randint, normalvariate

import numpy as np
try:
	import matplotlib.pyplot as plt
except ImportError:
	print('unable to find matplotlib library !')
	HAS_MATPLOTLIB = False
else:
	HAS_MATPLOTLIB = True

from Retina import Retina, ReceptiveField


def viewRetina(file_name):
	"Function plotting the content of a retina file"
	assert HAS_MATPLOTLIB, 'matplotlib not installed !, chack your installation.'
	retinaReader = Retina(file_name, ReceptiveField, None)
	rf_list = retinaReader.RF_LIST
	fig = plt.figure()
	for rf in rf_list:
		plt.plot(rf.X, rf.Y, '^k')
		caps = rf.CAP_LIST
		for cap in caps:
			plt.plot(cap[0], cap[1], 'xr')
			plt.plot([rf.X, cap[0]], [rf.Y, cap[1]], '--b')
	plt.show()
	return fig
	
	
def writeRetina(x_size, y_size, rf_list, cap_list, name = 'retina.ret'):
	"""Generic function which format retina properties to a text output
	x_size, y_size     : retina's size
	rf_list            : list of receptive fields coordinates
	cap_list           : list of captors list
	name               : file name to be used
	"""

        fRetina = open('retina.ret', 'w')
        fRetina.write('%d;%d\n' % (x_size, y_size))
	c_rf = 0
	for rf in rf_list:
		fRetina.write('%d;%d\n' % (rf[0], rf[1]))	
		caps = cap_list[c_rf]
		c_cap = 0
		for cap in caps:
			if (c_cap < len(caps) - 1):
				fRetina.write('%d;%d;' % (cap[0], cap[1]))
			else:
				fRetina.write('%d;%d\n' % (cap[0], cap[1]))
			c_cap += 1

		c_rf += 1
			 
	fRetina.close()


def LinearGridRetina(x_size, y_size, x_res, y_res, nbr_cap, sd_cap):
	"""Builder a linear sampling retina with lineary positionned receptivefields
	x_size, y_size  : retina's size
	x_res, y_res    : xy resolution
	nbr_cap         : number of captors
	sd_cap          : captors' standard deviation around receptive field
	"""

	rf_list = []
	cap_list = []
	x_grid = np.linspace(0, x_size - 1, round(x_size / x_res))
	y_grid = np.linspace(0, y_size - 1, round(y_size / y_res))

	for X in x_grid:
		for Y in y_grid:
			rf_list.append((X, Y))
			caps = []
		       	for cap_num in range(nbr_cap):
	       			x = int(round(normalvariate(X, sd_cap)))
       				y = int(round(normalvariate(Y, sd_cap)))					
				if x < 0:
					x = 0
				elif x >= x_size:
					x = x_size - 1
					
				if y < 0:
					y = 0   
				elif y >= y_size:
					y = y_size - 1
					
				caps.append((x, y))
			cap_list.append(caps)	

	writeRetina(x_size, y_size, rf_list, cap_list)


def LinearRandomRetina(x_size, y_size, nbr_rf, nbr_cap, sd_cap):
	"""Builder a linear sampling retina with randomly positionned receptivefields
	x_size, y_size   : retina's size
	nbr_rf           : number of receptive fields
	nbr_cap          : number of captors
	sd_cap           : captors' standard deviation around receptive fields
	"""

	rf_list = []
	cap_list = []

        for rf_num in range(nbr_rf):
            X = randint(0, x_size - 1)
            Y = randint(0, y_size - 1)
            rf_list.append((X, Y))
	    
	    caps = []
            for cap_num in range(nbr_cap):
                x = int(round(normalvariate(X, sd_cap)))
                y = int(round(normalvariate(Y, sd_cap)))
         
                if x < 0:
                    x = 0
                elif x >= x_size:
                    x = x_size - 1
                
                if y < 0:
                    y = 0   
                elif y >= y_size:
                    y = y_size - 1

		caps.append((x, y))
	    cap_list.append(caps)
	
	writeRetina(x_size, y_size, rf_list, cap_list)
