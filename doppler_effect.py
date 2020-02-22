import math
import pygame

"""
Just a dot moving left or right
depending on given settings
"""
class Entity:
    """
    x, y
    direction -->  -1 is left  and  1 is right
    velocity
    """
    def __init__(self, x, y, direction, velocity):
        self.x = x
        self.y = y
        self.direction = direction
        self.velocity = velocity

    def draw(self, screen):
        pygame.draw.circle(screen, (0, 255, 0), [self.x, self.y], 10)

    def update(self, dTime):
        if self.direction == 1:
            self.x += self.velocity*dTime
        elif self.direction == -1:
            self.x -= self.velocity*dTime
    def getPosition(self):
        return [self.x, self.y]

"""
This is object representing sound wave
 which spreads around 'emitter'
"""
class Wave:
    radius = 2
    velocity = 3 # Speed of wave
    def __init__(self, x, y, ID):
        self.x = x
        self.y = y
        self.id = ID # object identificator
    def draw(self, screen):
        pygame.draw.circle(screen, (0, 0, 255), [self.x, self.y], self.radius, 1)
    def update(self, dTime):
        self.radius += self.velocity*dTime

    def doesCollideWithCircle(self, position, radius):
        """Return wave id if its colliding, if not return False
        --> Checks if circle passed in arguments is colliding with this wave
        """
        distBetween = math.sqrt( (self.x-position[0])**2 + (self.y-position[1])**2 )
        if distBetween <= self.radius + radius and distBetween >= abs(self.radius - radius):
            return self.id
        else:
            return False

class FrequencyTimeline:
    pointer = [10, 550]
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    SPEED = 2
    height = 100
    width = 1000
    lastCollidedWaveId = False

    blocksPositions = [] # List containing x positions of timeline blocks
    
    def __init__(self):
        size = (1000, 150)
        self.aplha_surface = pygame.Surface(size, pygame.SRCALPHA)
        self.aplha_surface.fill((76, 80, 82, 150))
        
    def draw(self, screen):
        screen.blit(self.aplha_surface, (0, 550))
        pygame.draw.rect(self.aplha_surface, self.BLUE, (0, 500, self.width, self.height), 10) 
        for blockPos in self.blocksPositions:
            pygame.draw.rect(screen, self.RED, (blockPos, 550, 5, self.height), 0)

        pygame.draw.circle(screen, self.RED, self.pointer, 7) # a little circle on the top of the pointer - for attention
        pygame.draw.line(screen, self.RED, self.pointer, self.bottomPointer(), 2)
    def update(self, collision):
        self.pointer[0] += self.SPEED # move pointer to the right~!

        # If pointer is beyond screen
        if self.pointer[0] > self.width:
            self.pointer[0] = 5 # go back to the start!

        """If there is block in front of pointer
         in range of 250px then  d e l e t e  i t!
        """
        blcksNum = len(self.blocksPositions)
        if blcksNum > 0:
            isInRange = True
            i = 0
            while isInRange:
                print(i)
                if self.pointer[0] < self.blocksPositions[i] and self.pointer[0] + 250 > self.blocksPositions[i]:
                    del self.blocksPositions[i]
                else:
                    isInRange = False
                if i+1 < blcksNum:
                    i += 1

        """Check if collision with some new
        wave occured. If indeed, then add new block
        """
        if collision != False:
            if self.lastCollidedWaveId != collision:
                self.lastCollidedWaveId = collision
                self.blocksPositions.append( self.pointer[0] )
    def reset(self):
        self.blocksPositions = []
        
    def bottomPointer(self):
        return [ self.pointer[0], self.pointer[1]+self.height ]

class DopplerEffect:
    WHITE = (255, 255, 255)
    cycle = 1000 # how often emmit waves (in seconds/10)
    waves = []
    lastWaveTime = pygame.time.get_ticks()
    emitterDirect = -1
    observDirect = 1
    
    emitterSpeed = 1
    observSpeed = 1

    
    def __init__(self):
        self.frequencyMeter = FrequencyTimeline()
        self.reset()
    def render(self, screen):
        # Set the screen background
        for wave in self.waves:
            wave.draw(screen)

        self.emitter.draw(screen)
        self.observer.draw(screen)
        self.frequencyMeter.draw(screen)
    def update(self, dTime):
        roundDeltaTime = math.ceil( dTime )
        colission = False

        # Create new wave around emitter
        now = pygame.time.get_ticks()
        if now - self.lastWaveTime >= self.cycle:
            newWave = Wave(self.emitter.x, self.emitter.y, len(self.waves)+1)
            self.waves.append(newWave)
            self.lastWaveTime = now

        colission = False
        for wave in self.waves:
            wave.update(roundDeltaTime)
    
            if colission == False: # search till collision with wave found
                colission = wave.doesCollideWithCircle(self.observer.getPosition(), 5)

        self.emitter.update(roundDeltaTime)
        self.observer.update(roundDeltaTime)
        self.frequencyMeter.update(colission)

    # set frequency given in herz
    def setFrequency(self, frequency):
        self.cycle = 1/frequency * 1000
    
    def setDirection(self, emitt, obsrv):
        if emitt != None:
            self.emitterDirect = emitt
        if obsrv != None:
            self.observDirect = obsrv

    def setSpeed(self, emitt, obsrv):
        self.emitterSpeed = emitt
        self.observSpeed = obsrv
         
    def reset(self):
        # set starting coords by looking on choosen directions
        emittCoords = {'x': 500, 'y':300}
        obsvCoords = {'x': 100, 'y':300}
        

        """Depending on direction settings
         we change starting position of emitter and observer""" 
        if self.emitterDirect == 1 and self.observDirect == 1: # Both going right
            emittCoords['x'] = 270
        elif self.emitterDirect == -1 and self.observDirect == -1: # Both going left
            emittCoords['x'] = 900
            obsvCoords['x'] = 650
        elif self.emitterDirect == 1 and self.observDirect == -1: # Emitter right, observer left
            emittCoords['x'] = 270
            obsvCoords['x'] = 400
        elif self.emitterDirect == -1 and self.observDirect == 1: # Emitter right, observer left
            emittCoords['x'] = 500
            obsvCoords['x'] = 100

        # Object which is emitting sound
        self.emitter = Entity(emittCoords['x'], emittCoords['y'], self.emitterDirect, self.emitterSpeed)
        
        # Observer, which receives sound
        self.observer = Entity(obsvCoords['x'], obsvCoords['y'], self.observDirect, self.observSpeed)
        
        # Clear waves array and timeline with sound receiving
        self.waves = []
        self.frequencyMeter.reset()