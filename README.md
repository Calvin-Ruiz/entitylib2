# entitylib2
Library with optimized gestion of entities with pygame

Notes :  
all textures must be in "textures", and all sound in "sounds"  
rename "background.png" your background image  
if one image couldn't be loaded, "default.bmp" was loaded instead  
Descriptions wasn't in french now.  
"test.py" is an example of program using my library.  
textures/letter and textures/letters is used for write text on pygame display.

Usage :  
Use "from entitylib2 import * " to import this library, pygame (initialized) and randint.  
Initialize entitylib2 and your entities with init()

Warning : multiprocessing doesn't work with python 3.7.1 !  
multiprocessing work with python 3.5.2, and maybe with other version.
