"""
Models module for Alien Invaders

This module contains the model classes for the Alien Invaders game. Anything that you
interact with on the screen is model: the ship, the laser bolts, and the aliens.

Just because something is a model does not mean there has to be a special class for
it.  Unless you need something special for your extra gameplay features, Ship and Aliens
could just be an instance of GImage that you move across the screen. You only need a new 
class when you add extra features to an object. So technically Bolt, which has a velocity, 
is really the only model that needs to have its own class.

With that said, we have included the subclasses for Ship and Aliens.  That is because
there are a lot of constants in consts.py for initializing the objects, and you might
want to add a custom initializer.  With that said, feel free to keep the pass underneath 
the class definitions if you do not want to do that.

You are free to add even more models to this module.  You may wish to do this when you 
add new features to your game, such as power-ups.  If you are unsure about whether to 
make a new class or not, please ask on Piazza.

# Author: Komukill Loganathan (kl866)
# Date: November 30, 2017
"""
from consts import *
from game2d import *

# PRIMARY RULE: Models are not allowed to access anything in any module other than 
# consts.py.  If you need extra information from Gameplay, then it should be
# a parameter in your method, and Wave should pass it as a argument when it
# calls the method.


class Ship(GImage):
    """
    A class to represent the game ship.
    
    At the very least, you want a __init__ method to initialize the ships dimensions.
    These dimensions are all specified in consts.py.
    
    You should probably add a method for moving the ship.  While moving a ship just means
    changing the x attribute (which you can do directly), you want to prevent the player
    from moving the ship offscreen.  This is an ideal thing to do in a method.
    
    You also MIGHT want to add code to detect a collision with a bolt. We do not require
    this.  You could put this method in Wave if you wanted to.  But the advantage of 
    putting it here is that Ships and Aliens collide with different bolts.  Ships 
    collide with Alien bolts, not Ship bolts.  And Aliens collide with Ship bolts, not 
    Alien bolts. An easy way to keep this straight is for this class to have its own 
    collision method.
    
    However, there is no need for any more attributes other than those inherited by
    GImage. You would only add attributes if you needed them for extra gameplay
    features (like animation). If you add attributes, list them below.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    pass
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getShipX(self):
        """
        Returns the x coordinate of Ship object
        """
        return self.x
        
    
    def getShipY(self):
        """
        Returns the y coordinate of Ship object
        """
        return self.y
    
    
    # INITIALIZER TO CREATE A NEW SHIP
    def __init__(self):
        """
        Initializer: creates a ship using default measurements
        """
        super().__init__(x=GAME_WIDTH/2, y=SHIP_BOTTOM, width=SHIP_WIDTH,
                         height=SHIP_HEIGHT, source='ship.png')
    
    # METHODS TO MOVE THE SHIP AND CHECK FOR COLLISIONS
    def moveShip(self, input):
        """
        Moves ship to left or right based on keystroke detected.
        
        This method reads the player's key presses.The ship moves only when the
        player presses a left or right arrow keys.
        
        This method is written with guidance from codes in arrows.py update()
        method from class
        """
        #print('initial x: ' + str(self.x)) #watch
        da = 0
        if input.is_key_down('left'):
            da += SHIP_MOVEMENT
        if input.is_key_down('right'):
            da -= SHIP_MOVEMENT
        
        #change position
        x = self.x - da
        x = max(SHIP_WIDTH/2, x)
        x = min(x, GAME_WIDTH-(SHIP_WIDTH/2))
        self.x = x
        
    
    def collides(self,bolt):
        """
        Returns: True if the bolt was fired by the alien and collides with this ship
        
        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        collision = False
        half_width = BOLT_WIDTH/2
        half_height = BOLT_HEIGHT/2
        
        bottomleft = self.contains((bolt.getBoltX()-half_width, bolt.getBoltY()-half_height))
        bottomright = self.contains((bolt.getBoltX()+half_width, bolt.getBoltY()-half_height))
        bottom = bottomleft or bottomright
        
        topleft = self.contains((bolt.getBoltX()-half_width, bolt.getBoltY()+half_height))
        topright = self.contains((bolt.getBoltX()+half_width, bolt.getBoltY()+half_height))
        top = topleft or topright
        
        collision = bottom or top
        
        return collision and (not bolt.isPlayerBolt())
    
    
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Alien(GImage):
    """
    A class to represent a single alien.
    
    At the very least, you want a __init__ method to initialize the alien dimensions.
    These dimensions are all specified in consts.py.
    
    You also MIGHT want to add code to detect a collision with a bolt. We do not require
    this.  You could put this method in Wave if you wanted to.  But the advantage of 
    putting it here is that Ships and Aliens collide with different bolts.  Ships 
    collide with Alien bolts, not Ship bolts.  And Aliens collide with Ship bolts, not 
    Alien bolts. An easy way to keep this straight is for this class to have its own 
    collision method.
    
    However, there is no need for any more attributes other than those inherited by
    GImage. You would only add attributes if you needed them for extra gameplay
    features (like giving each alien a score value). If you add attributes, list
    them below.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getAlienX(self):
        """
        Returns the x coordinate of the alien object
        """
        return self.x
    
    
    def setAlienX(self, val):
        """
        Sets x coordinate of Alien object
        
        Parameter val: value to be set as x coordinate
        Precondition: val is a number, int or float, x>0 and x<GAME_WIDTH
        """
        self.x = val
    
    
    def getAlienY(self):
        """
        Returns the y coordinate of the alien object
        """
        return self.y
    
    
    def setAlienY(self, val):
        """
        Sets y coordinate of Alien object
        
        Parameter val: value to be set as y coordinate
        Precondition: val is a number, int or float, y>0 and y<GAME_HEIGHT
        """
        self.y = val
        
    
    # INITIALIZER TO CREATE AN ALIEN
    def __init__(self, x_coor, y_coor, image):
        """
        Initializer: Creates an Alien object.
        
        Parameter x-coor: The x position of image
        Precondition: x-coor is an int or float and x-coor >= 0
        
        Parameter y-coor: The y position of image
        Precondition: y-coor is an int or float and y-coor >= 0
        
        Parameter image: The image name
        Precondition: image is a str and a valid name of image from Images folder
        """
        super().__init__(x=x_coor, y=y_coor, width=ALIEN_WIDTH, height=ALIEN_HEIGHT, source=image)
    
    # METHOD TO CHECK FOR COLLISION (IF DESIRED)
    def collides(self, bolt):
        """
        Returns: True if the bolt was fired by the player and collides with this alien
        
        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        collision = False
        half_width = BOLT_WIDTH/2
        half_height = BOLT_HEIGHT/2
        
        bottomleft = self.contains((bolt.getBoltX()-half_width, bolt.getBoltY()-half_height))
        bottomright = self.contains((bolt.getBoltX()+half_width, bolt.getBoltY()-half_height))
        bottom = bottomleft or bottomright
        
        topleft = self.contains((bolt.getBoltX()-half_width, bolt.getBoltY()+half_height))
        topright = self.contains((bolt.getBoltX()+half_width, bolt.getBoltY()+half_height))
        top = topleft or topright
        
        collision = bottom or top
        
        return bolt.isPlayerBolt() and collision
    
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Bolt(GRectangle):
    """
    A class representing a laser bolt.
    
    Laser bolts are often just thin, white rectangles.  The size of the bolt is 
    determined by constants in consts.py. We MUST subclass GRectangle, because we
    need to add an extra attribute for the velocity of the bolt.
    
    The class Wave will need to look at these attributes, so you will need getters for 
    them.  However, it is possible to write this assignment with no setters for the 
    velocities.  That is because the velocity is fixed and cannot change once the bolt
    is fired.
    
    In addition to the getters, you need to write the __init__ method to set the starting
    velocity. This __init__ method will need to call the __init__ from GRectangle as a 
    helper.
    
    You also MIGHT want to create a method to move the bolt.  You move the bolt by adding
    the velocity to the y-position.  However, the getter allows Wave to do this on its
    own, so this method is not required.
    
    INSTANCE ATTRIBUTES:
        _velocity: The velocity in y direction [int or float]
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    pass
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def isPlayerBolt(self):
        """
        Returns True if Bolt object is fired by Player, False otherwise
        """
        return (self._velocity >= 0)
    
    def getBoltY(self):
        """
        Returns the y value of the bottom of the Bolt object
        """
        return self.y
    
    
    def setBoltY(self, yval):
        """
        Sets the y coordinate of Bolt object
        
        Parameter yval: y coordinate to be set as
        Precondition: y is an int or float
        """
        self.y = yval
    
    
    def getBoltX(self):
        """
        Returns the x value of the center of the Bolt object
        """
        return self.x
    
    def getVelocity(self):
        """
        Returns velocity of Bolt object
        """
        return self._velocity
    
    
    # INITIALIZER TO SET THE VELOCITY
    def __init__(self, xval, yval, w, h, fill, direction):
        """
        Initializes Bolt object
        
        This methods overrides the initializer of the super class GRectangle to
        initializes the velocity of the bolt according to the direction it travels.
        
        Parameter xval: x coordinate of Bolt object
        Precondition: x is an int or float, same as the x coordinate of Ship
        
        Parameter yval: y coordinate of Bolt object
        Precondition: y is an int or float, position right above the Ship's nose
        
        Parameter w: width of the Bolt object
        Precondition: w is an int or float
        
        Parameter h: height of the Bolt object
        Precondition: h is an int or float
        
        Parameter fill: fillcolor of the Bolt object
        Precondition: fill is a str, a valid RGB color
        
        Parameter direction: direction travelled by Bolt object
        Precondition direction is a str, either 'up' or 'down'
        """
        super().__init__(x=xval, y=yval, width=w, height=h, fillcolor=fill)
        if direction == 'up':
            self._velocity = BOLT_SPEED
        elif direction == 'down':
            self._velocity = -1*BOLT_SPEED
            
    
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
        

# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE