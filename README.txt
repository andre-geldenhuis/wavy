#################################################################
 Wavy sensory substitution system
#################################################################

v1.0
Nicolas Louveton - <nblouveton@gmail.com>

Wavy is an agile sensory substitution system designed to make
easier prototyping, experimenting and playing with sensory
substitution.

Wavy provides base components to create a variety
of sensory substitution machines adapted to a variety of context
of use. It is coded in python to improve ease of use, extension
and prototyping.

Wavy is a free software remeased under the GPLv3 license.
For more details, see COPYING file in this directory or visit :
http://www.gnu.org/licenses/gpl.txt


[ BEFORE INSTALLATION ]

To properly install wavy you need a standard python execution
environment (Python >=2.5).

Check Python project's website : http://www.python.org/download/

Minimal requierements :
- numpy
- pygame

Recommanded packages :
- python-opencv to work with digital video input.
- pyOpenGL to work with openGL input.
- matplotlib to make plots with retina files.
- psyco : a just-in-time compiler to improve run-time performances.

Additionaly :
Wavy can be used with psychopy experiments in order to sonify psychopy's
displays.

Wavy should be able to run on every system were these requierements
are satisfied.


[ HOW TO INSTALL ]

There is two way to install Wavy :
- You can simply unpack the source package and use it.
- If you want to install Wavy in your environment, you can run :
  $ python setup.py install


[ HOW TO USE WITH GAMES/EXPERIMENTS ? ]

You can run demos located in the root directory in the same way
as you run usual python scripts.

You can inspire yourself with these examples to create new
games/experiments from base classes.

!!! glDemo must be launched using python's executable in command line
even if you are under unix :
$ python glDemo.py

[ HOW TO USE WITH DIGITAL VIDEO INPUT ? ]

If you want to use Wavy with a digital camera (webcam for exampele) :
- plug your device
- run theWave.py script


[ RETINA FILES ]

Retina Files can be created with wavy.Utils module. See module's documentation
for more details.


[ EOF ]