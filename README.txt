#################################################################
 Wavy sensory substitution system
#################################################################

v1.x
Nicolas Louveton

Wavy is an agile sensory substitution system designed to make
easier prototyping, experimenting and playing with sensory
substitution.

Wavy is a free software released under the GPLv3 license.
For more details, see LICENSE file in this directory or visit :
http://www.gnu.org/licenses/gpl.txt

Please check wavy's webpage : 
http://nblouveton.wordpress.com/wavy/

[ BEFORE INSTALLATION ]

To properly install wavy you need a standard python execution
environment (Python >=2.5).

Check Python project's website : http://www.python.org/download/

Minimal requierements :
- numpy
- pygame


[ HOW TO INSTALL ]

You can simply unpack the source package and use it.

Or to install Wavy on you system:
- If you want to install Wavy in your environment, you can run :
  $ python setup.py install


[ HOW TO USE WITH GAMES/EXPERIMENTS ? ]

Optionnal package needed: python-openGL to enable 3D display substitution.

You can run demos located in the root directory in the same way
as you run usual python scripts.

You can inspire yourself with these examples to create new
games/experiments from base classes.


[ HOW TO USE WITH DIGITAL VIDEO INPUT ? ]

Required package: python-opeCV

If you want to use Wavy with a digital camera (webcam for exampele) :
- plug your device
- run theWave.py script


[ RETINA FILES ]

Retina Files can be created with wavy.Utils module. See module's documentation
for more details.


[ EOF ]
