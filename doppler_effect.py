#import time
import math
import pygame
#SCREEN = pygame.display.set_mode((1000, 650))

class Entity:
    """
    x, y
    kierunek <== -1 w lewo i 1 w prawo
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
    
class Wave:
    radius = 2
    def __init__(self, x, y, velocity):
        self.x = x
        self.y = y
        self.velocity = velocity
    def draw(self, screen):
        pygame.draw.circle(screen, (0, 0, 255), [self.x, self.y], self.radius, 1)
    def update(self, dTime):
        self.radius += self.velocity*dTime
        

class DopplerEffect:
    WHITE = (255, 255, 255)
    cycle = 1000 # how often emmit waves (in seconds/10) 
    waves = []
    lastWaveTime = pygame.time.get_ticks()
    emitterDirect = -1
    observDirect = 1
    
    
    def __init__(self):
        self.reset()
        #self.wave = Wave(self.emitter.x, self.emitter.y, 2)
    def render(self, screen):
        # Set the screen background
        #screen.fill(self.WHITE)
        
        for wave in self.waves:
            wave.draw(screen)

        self.emitter.draw(screen)
        self.observer.draw(screen)
    def update(self, dTime):
        roundDeltaTime = math.ceil( dTime )
        
        # Create new wave around emitter
        now = pygame.time.get_ticks()
        if now - self.lastWaveTime >= self.cycle:
            newWave = Wave(self.emitter.x, self.emitter.y, 2)
            self.waves.append(newWave)
            self.lastWaveTime = now
        
        for wave in self.waves:
            wave.update(roundDeltaTime)
        
        self.emitter.update(roundDeltaTime)
        self.observer.update(roundDeltaTime)
        
    # set frequency given in herz
    def setFrequency(self, frequency):
        #print("frequency: "+str(frequency))
        self.cycle = 1/frequency * 1000
    
    def setDirection(self, emitt, obsrv):
        if emitt != None:
            self.emitterDirect = emitt
        if obsrv != None:
            self.observDirect = obsrv
         
    def reset(self):
        # set starting coords by looking on choosen directions
        emittCoords = {'x': 500, 'y':300}
        obsvCoords = {'x': 100, 'y':300}
        
        if self.emitterDirect == 1 and self.observDirect == 1: # Both going right
            emittCoords['x'] = 270
        elif self.emitterDirect == -1 and self.observDirect == -1: # Both going left
            emittCoords['x'] = 900
            obsvCoords['x'] = 650
        elif self.emitterDirect == 1 and self.observDirect == -1: # Emitt right, observer left
            emittCoords['x'] = 270
            obsvCoords['x'] = 400
        elif self.emitterDirect == -1 and self.observDirect == 1: # Emitt right, observer left
            emittCoords['x'] = 500
            obsvCoords['x'] = 100

        self.emitter = Entity(emittCoords['x'], emittCoords['y'], self.emitterDirect, 1)
        self.observer = Entity(obsvCoords['x'], obsvCoords['y'], self.observDirect, 1)
        self.waves = []