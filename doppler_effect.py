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
    def __init__(self, x, y, kierunek, velocity):
        self.x = x
        self.y = y
        self.kierunek = kierunek
        self.velocity = velocity

    def draw(self, screen):
        pygame.draw.circle(screen, (0, 255, 0), [self.x, self.y], 10)

    def update(self, dTime):
        if self.kierunek == 1:
            self.x += self.velocity*dTime
        else:
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
    cycle = 300 # how often emmit waves (in seconds) 
    waves = []
    lastWaveTime = pygame.time.get_ticks()

    def __init__(self):
        self.zrodlo = Entity(500, 325, -1, 1)
        #self.wave = Wave(self.zrodlo.x, self.zrodlo.y, 2)
    def render(self, screen):
        # Set the screen background
        #screen.fill(self.WHITE)
        
        for wave in self.waves:
            wave.draw(screen)

        self.zrodlo.draw(screen)
    def update(self, dTime):
        roundDeltaTime = math.ceil( dTime )
        
        # Create new wave around emitter
        print("cycle: "+str(self.cycle))
        print("dTIme: "+str(self.lastWaveTime))
        now = pygame.time.get_ticks()
        if now - self.lastWaveTime >= self.cycle:
            newWave = Wave(self.zrodlo.x, self.zrodlo.y, 2)
            self.waves.append(newWave)
            self.lastWaveTime = now
        
        for wave in self.waves:
            wave.update(roundDeltaTime)
        
        self.zrodlo.update(roundDeltaTime)