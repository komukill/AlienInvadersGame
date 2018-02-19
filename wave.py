"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in the Alien
Invaders game.  Instances of Wave represent a single wave.  Whenever you move to a
new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on screen.  
These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a complicated
issue.  If you do not know, ask on Piazza and we will answer.

# Author: Komukill Loganathan (kl866)
# Date: November 30, 2017
"""

from game2d import *
from consts import *
from models import *
import random

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not permitted 
# to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.
    
    This subcontroller has a reference to the ship, aliens, and any laser bolts on screen. 
    It animates the laser bolts, removing any aliens as necessary. It also marches the
    aliens back and forth across the screen until they are all destroyed or they reach
    the defense line (at which point the player loses). When the wave is complete, you 
    should create a NEW instance of Wave (in Invaders) if you want to make a new wave of 
    aliens.
    
    If you want to pause the game, tell this controller to draw, but do not update.  See 
    subcontrollers.py from Lecture 24 for an example.  This class will be similar to
    than one in how it interacts with the main class Invaders.
    
    #UPDATE ME LATER
    INSTANCE ATTRIBUTES:
        _ship:   the player ship to control [Ship]
        _aliens: the 2d list of aliens in the wave [rectangular 2d list of Alien or None] 
        _bolts:  the laser bolts currently on screen [list of Bolt, possibly empty]
        _dline:  the defensive line being protected [GPath]
        _lives:  the number of lives left  [int >= 0]
        _time:   The amount of time since the last Alien "step" [number >= 0]
    
    As you can see, all of these attributes are hidden.  You may find that you want to
    access an attribute in class Invaders. It is okay if you do, but you MAY NOT ACCESS 
    THE ATTRIBUTES DIRECTLY. You must use a getter and/or setter for any attribute that 
    you need to access in Invaders.  Only add the getters and setters that you need for 
    Invaders. You can keep everything else hidden.
    
    You may change any of the attributes above as you see fit. For example, may want to 
    keep track of the score.  You also might want some label objects to display the score
    and number of lives. If you make changes, please list the changes with the invariants.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
        _direction: the direction the aliens march towards [string, either 'right' or 'left']
        _previouskeys: the number of keys pressed in the previous frame [int>=0]
        _firespeed: randomly generated, number of steps by aliens to fire [int>=1, int<=BOLT_RATE]
        _step: steps taken by aliens, cumulative but gets reset to 0 after firing bolt[int>=0]
        _gameover: is the game over, True for yes, False for no [bool]
        _won: did the player win, True for yes, False for no [bool]
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getWon(self):
        """
        Returns whether the player has won
        """
        return self._won
        
        
    def getLives(self):
        """
        Returns the number of lives remaining
        """
        return self._lives
    
    
    def getShip(self):
        """
        Returns player ship
        """
        return self._ship
    
    
    def getGameOver(self):
        """
        Returns a bool value that indicates whether the game is over
        """
        return self._gameover
    
    
    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self):
        """
        Initializer: creates ship, defense line, and wave of aliens
        """
        self._lives = SHIP_LIVES
        self._aliens = self._createAlienWave(); 
        self._ship = Ship()
        self._dline = GPath(points=[0,DEFENSE_LINE,GAME_WIDTH,DEFENSE_LINE],
                            linewidth=1.5, linecolor='black')
        self._time = 0
        self._direction = 'right'
        self._bolts = []
        self._previouskeys = 0
        self._firespeed = random.randint(1, BOLT_RATE)
        self._step = 0
        self._gameover = False
        self._won = False
    
    
    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self, input, dt):
        """
        Animates the movement of the ship, aliens and laser bolts
        
        This method is called in the update() method of Invaders to help in
        moving the ship, aliens and laser bolts.
        
        Parameter input: the user input, used to control the game
        Precondition: Instance of GInput and attribute of Invaders
        
        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        if self._isGameOver():
            self._gameover = True
        else:
            self._moveAliens(dt)
            if not(self._ship is None):
                self._ship.moveShip(input)
                self._createPlayerBolts(input)
            if self._ship == None:
                self._ship = Ship()
                self._bolts = []
            if not (not self._bolts):
                self._moveBolts()
                self._detectCollision()

    
    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self, view):
        """
        Draws the shapes in the view provided
        
        Parameter view: the game view, used in drawing
        Precondition: instance of GView and Invaders
        """
        if not (self._ship is None):
            self._ship.draw(view)
        self._dline.draw(view)
        
        for row in range(len(self._aliens)):
            for col in range(len(self._aliens[row])):
                if not(self._aliens[row][col] is None):
                    self._aliens[row][col].draw(view)
        
        for x in range(len(self._bolts)):
            self._bolts[x].draw(view)
        
    
    def _createAlienWave(self):
        """
        Returns: Created alien wave when the game begins
        
        This is a helper method that creates a wave of aliens. It does this by
        filling the _aliens 2d list with alien objects. It draws ALIEN_ROWS rows
        of aliens with ALIENS_IN_ROW many aliens in each row.
        
        Each row is an element of _aliens list and each row will be a list of
        Alien object. 
        """
        x_pos = ALIEN_H_SEP + (ALIEN_WIDTH//2)
        y_pos = GAME_HEIGHT - (ALIEN_CEILING + (ALIEN_ROWS*ALIEN_HEIGHT) + ((ALIEN_ROWS-1)*ALIEN_V_SEP))
        init_x = x_pos
        list = []
        
        for row in range(ALIEN_ROWS):
            list.append([])
            
            if row % 6 == 0 or row % 6 == 1:
                picture = 0
            elif row % 6 == 2 or row % 6 == 3:
                picture = 1
            else:
                picture = 2
                
            for col in range(ALIENS_IN_ROW):
                alien = Alien(x_pos, y_pos, ALIEN_IMAGES[picture])
                list[row].append(alien)
                x_pos = x_pos + ALIEN_H_SEP + ALIEN_WIDTH
            y_pos = y_pos + ALIEN_V_SEP + ALIEN_HEIGHT
            x_pos = init_x
        
        return list
    
    
    def _moveAliens(self, dt):
        """
        Moves aliens back and forth the screen.
        
        This is a helper method called int he update() function to move the
        aliens back and forth when the game is active.
        
        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        self._time += dt
        
        if self._time > ALIEN_SPEED:
            if self._direction == 'right':
                self._moveAlienToRight()
            elif self._direction == 'left':
                self._moveAlienToLeft()
            if self._step == self._firespeed:
                self._fireAlienBolt()
            self._time = 0
            
            
    def _moveAlienToRight(self):     # USE GETTERS/SETTERS FOR ALIEN X AND Y
        """
        Moves the aliens to the right
        """
        rightalien = self._rightmostAlien()
        if GAME_WIDTH - rightalien.getAlienX() <= (ALIEN_H_SEP + ALIEN_WIDTH/2):
            self._moveAlienDown()
            self._direction = 'left'
        else:
            for row in range(len(self._aliens)):
                for alien in range(len(self._aliens[row])):
                    if not(self._aliens[row][alien] is None):
                        x = self._aliens[row][alien].getAlienX()
                        x = x + ALIEN_H_WALK
                        self._aliens[row][alien].setAlienX(x)
        self._step +=1
        
        
    def _moveAlienToLeft(self):     
        """
        Moves the aliens to the left
        """
        leftalien = self._leftmostAlien()
        if leftalien.getAlienX() <= (ALIEN_H_WALK + ALIEN_WIDTH/2):  
            self._moveAlienDown()
            self._direction = 'right'
        else:
            for row in range(len(self._aliens)):
                for alien in range(len(self._aliens[row])):
                    if not(self._aliens[row][alien] is None):
                        x = self._aliens[row][alien].getAlienX()
                        x = x - ALIEN_H_WALK
                        self._aliens[row][alien].setAlienX(x)
        self._step += 1
            
    
    def _rightmostAlien(self):
        """
        Returns the right most alien in the wave
        """
        x = 0
        for row in range(len(self._aliens)):
            for col in range(len(self._aliens[row])):
                if not(self._aliens[row][col] is None) and self._aliens[row][col].getAlienX() > x:
                    alien = self._aliens[row][col]
                    x = alien.getAlienX()
        return alien
    
     
    def _leftmostAlien(self):
        """
        Returns the left most alien in the wave
        """
        x = GAME_WIDTH
        for row in range(len(self._aliens)):
            for col in range(len(self._aliens[row])):
                if not(self._aliens[row][col] is None) and self._aliens[row][col].getAlienX() < x:
                    alien = self._aliens[row][col]
                    x = alien.getAlienX()
        return alien
     
     
    def _moveAlienDown(self):    
        """
        Moves aliens down
        """
        for row in range(len(self._aliens)):
            for alien in range(len(self._aliens[row])):
                if not(self._aliens[row][alien] is None):
                    y = self._aliens[row][alien].getAlienY()
                    y = y - ALIEN_V_WALK
                    self._aliens[row][alien].setAlienY(y)
        
    
    def _createPlayerBolts(self, input):
        """
        Creates a laser bolt when the player presses a fire key (spacebar)
        
        This methods create a Bolt object when a fire command is detected. The
        Bolt object has the same x position as the ship and it will be placed
        right in front of the ship's nose. These Bolt objects are stored in the
        _bolts attribute.
        
        Parameter input: the user input, used to control the game
        Precondition: Instance of GInput and attribute of Invaders
        """
        if input.is_key_down('spacebar') and self._previouskeys == 0 and self._allowPlayerFire():
            obj = Bolt(self._ship.getShipX(), (self._ship.getShipY()+SHIP_HEIGHT/2),
                       BOLT_WIDTH, BOLT_HEIGHT, 'black', 'up')
            self._bolts.append(obj)
        self._previouskeys = input.key_count
        
        
    def _createAlienBolts(self, alien):
        """
        Creates a laser bolt to be fired by aliens
        
        This method creates a Bolt object to be fired by an alien and add it to
        the _bolts list.
        
        Parameter alien: alien that will fire the bolt
        Precondition: alien is an Alien object from the 2D list _aliens.
        """
        obj = Bolt(alien.getAlienX(), (alien.getAlienY()-ALIEN_HEIGHT/2), BOLT_WIDTH,
                   BOLT_HEIGHT, 'green', 'down')
        self._bolts.append(obj)
        
        
    def _allowPlayerFire(self):
        """
        Returns True if player can fire, False otherwise
        """
        fire = True
        
        for x in range(len(self._bolts)):
            if self._bolts[x].isPlayerBolt():
                fire = False
                
        return fire
        
    
    def _fireAlienBolt(self):
        """
        Picks aliens from wave to fire and fires bolt randomly
        """
        random_col = self._randomNonEmptyColumn()
        
        #bottommost element in random col
        alien = self._bottomMostAlien(random_col)
        if not(alien is None):
            self._createAlienBolts(alien)
        self._step = 0
        self._firespeed = random.randint(1, BOLT_RATE)
    
    
    def _randomNonEmptyColumn(self):
        """
        Returns a random nonempty column in aliens wave
        """
        #determine non-empty columns
        row = 0
        col = 0
        nonEmptyCols = []
        emptyCol = True
        while col < len(self._aliens[row]):
            if not (self._aliens[row][col] is None):
                emptyCol = False
            row = row + 1
            if row == len(self._aliens):
                row = 0
                nonEmptyCols.append(col)
                col = col + 1
                
        return nonEmptyCols[random.randint(0,len(nonEmptyCols)-1)] #pick a random nonempty col
    
    
    def _bottomMostAlien(self, col):
        """
        Returns the bottom most alien object in the column
        
        Parameter col: column in which the bottommost alien needs to be found
        Precondition: col is a valid col number within the aliens 2D list
        """
        alien = None
        min_y = GAME_HEIGHT
        for row in range(len(self._aliens)):
            if not(self._aliens[row][col] is None) and self._aliens[row][col].getAlienY() < min_y:
                min_y = self._aliens[row][col].getAlienY()
                alien = self._aliens[row][col]
        
        return alien
    
        
    def _moveBolts(self):
        """
        Move bolts across the screen and delete them when they go off screen
        """
        x = 0
        while x < len(self._bolts):
            y = self._bolts[x].getBoltY()
            y += self._bolts[x].getVelocity()
            self._bolts[x].setBoltY(y)
            
            #delete bolt when they go off screen, above or below
            if self._bolts[x].getBoltY() > GAME_HEIGHT or self._bolts[x].getBoltY() <= 0:
                del self._bolts[x]
            else:
                x = x+1
                
    
    # HELPER METHODS FOR COLLISION DETECTION
    def _detectCollision(self):
        x = 0
        condition = True
        while x < len(self._bolts) and condition == True and not(self._ship is None):
            if self._detectAlienCollision(self._bolts[x]) == True:
                del self._bolts[x]
            else:
                self._detectShipCollision(self._bolts[x])
            x = x+1
    
    
    def _detectAlienCollision(self, bolt):
        """
        Returns: True if detects collision between aliens in the wave and laser bolt by player
        
        This method detects collision between aliens and the laser bolt passed
        as argument. If there is collision, this method sets the alien that had
        collided to None, deletes the bolt and returns True. It returns False
        otherwise.
        
        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        collision = False
        for row in range(len(self._aliens)):
            for col in range(len(self._aliens[row])):
                if collision == False and not(self._aliens[row][col] is None) and self._aliens[row][col].collides(bolt):
                    self._aliens[row][col] = None
                    collision = True
        return collision
    
    
    def _detectShipCollision(self, bolt):
        """
        Returns: True if detects collision between ship and laser bolt by aliens
        
        This method detects collision between the ship and the laser bolt passed
        as argument. If there is collision, this method sets the ship that had
        collided to None, deletes the bolt and returns true. It returns False
        otherwise.
        
        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        collision = False
        if self._ship.collides(bolt):
            self._ship = None
            del bolt
            collision = True
            self._lives -= 1
        return collision
    
    
    def _isGameOver(self):
        """
        Returns bool after checking if the game is over
        
        This methods checks if (1) all the aliens are killed or (2) any alien
        dips below the defense line. If either of the cases happen, this method
        returns True. It returns False otherwise. 
        """
        emptywave = True
        dipped = False
        
        for row in range(len(self._aliens)):
            for col in range(len(self._aliens[row])):
                if not (self._aliens[row][col] is None):
                    emptywave = False
                    if self._aliens[row][col].getAlienY() <= DEFENSE_LINE:
                        dipped = True
        
        if emptywave:
            self._won = True

        return emptywave or dipped
        