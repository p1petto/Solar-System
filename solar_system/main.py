import pygame
import math
import sys
import enum
 
class Colors(enum.Enum):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    YELLOW = (255, 255, 0)
    COLOR_MERCURY = (175, 83, 34)
    COLOR_VENUS = (160, 18, 9)
    COLOR_EARTH = (100, 149, 237)
    COLOR_MARS = (223, 146, 115)
    COLOR_JUPITER = (170, 130, 160)
    COLOR_SATURN = (220, 170, 60)
    COLOR_URANUS = (170, 200, 250)
    COLOR_NEPTUNE = (120, 170, 250)
    
class Window:
    def __init__(self, width=1200, height=800, scale=1):
        self.W = width
        self.H = height
        self._scale = scale
        self._WIN = pygame.display.set_mode((self.W, self.H))
        self._drawSurface = pygame.Surface((self.W, self.H))
        self._scaleSurface = pygame.Surface(self.get_resolution())
        pygame.display.set_caption('Planet Simulation')

        self.bg = pygame.image.load("images\space.jpg")
        
 
    def get_resolution(self):
        return self.W * self._scale, self.H * self._scale
 
    def updateScale(self):
        self._WIN.fill(Colors.BLACK.value)
        self._scaleSurface = pygame.Surface(self.get_resolution())
        pygame.transform.smoothscale(self._drawSurface, self.get_resolution(), self._scaleSurface)
        self._WIN.blit(self._scaleSurface, ((-((self.W * self._scale) - self.W) / 2), (-((self.H * self._scale) - self.H)) / 2))
 
    def fill(self, color=Colors.BLACK):
        self._drawSurface.fill(color.value)
        
    def blit_bg(self):
        self._drawSurface.blit(self.bg, (0,0))

    def getSurface(self):
        return self._drawSurface
 
    def getScale(self):
        return self._scale
 
    def setScale(self, scale):
        try:
            if scale <= 0:
                raise ValueError('scale can`t be below zero')
            self._scale = scale
        except ValueError as err:
            raise
        

class Planet:
	def __init__(self, name, radius, color, coef, distance):
		self.angle = 6
		self.radius = radius
		self.color = color
		self.distance_to_sun = 0
		self.coef = coef
		self.distance = distance
		self.name = name
		self.x = 0
		self.y = 0
		
	def draw(self, win):
		self.x = int(math.cos(self.angle) * self.distance) + win.W / 2
		self.y = int(math.sin(self.angle) * self.distance) + win.H / 2

		self.circ = pygame.draw.circle(win.getSurface(), self.color, (self.x, self.y), self.radius)

		self.angle += self.coef
		
	def draw_info(self, win, num):
		
		self.info_circ = pygame.draw.circle(win.getSurface(), self.color, (50 + num * 50, 50), 20)

r_earth = 9

mercury = 	Planet('Mercury',   r_earth * 0.38, 	Colors.COLOR_MERCURY.value, 	10 / 87.97, 	10)
venus = 	Planet('Venus',     r_earth * 0.95, 	Colors.COLOR_VENUS.value, 	    10 / 224.7, 	22)
earth = 	Planet('Earth',     r_earth * 1, 	    Colors.COLOR_EARTH.value, 	    10 / 365.3, 	38)
mars = 		Planet('Mars',      r_earth * 0.53, 	Colors.COLOR_MARS.value, 	    10 / 867, 		55)
jupiter = 	Planet('Jupiter',   r_earth * 11.2, 	Colors.COLOR_JUPITER.value, 	10 / 4332.3, 	165)
saturn = 	Planet('Saturn',    r_earth * 9.5, 	    Colors.COLOR_SATURN.value, 	    10 / 10761.7, 	360)
uranus = 	Planet('Uranus',    r_earth * 3.9, 	    Colors.COLOR_URANUS.value, 	    10 / 30592.9, 	485)
neptune = 	Planet('Neptune',   r_earth * 4.0, 	    Colors.COLOR_NEPTUNE.value, 	10 / 60201.2, 	560)
 
planets = [mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]
 

clock = pygame.time.Clock()
# MainLoop
def main():

    wind = Window()
    currScale = 1
    run = True
    pause = False
    while run:
        if not pause:
            clock.tick(100)
            wind.fill(Colors.BLACK)
            wind.blit_bg()
            sun = pygame.draw.circle(wind.getSurface(), Colors.YELLOW.value, (wind.W / 2, wind.H / 2), 4)

            for i, planet in enumerate(planets):
                planet.draw(wind)
                planet.draw_info(wind, i)

            wind.updateScale()
 
        # EventHandle
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # Buttons
            if event.type == pygame.KEYDOWN:
                if not pause:
                    if event.key == pygame.K_z:
                        if wind.getScale() < 3:
                            currScale += 0.1
                            wind.setScale(currScale)
                    if event.key == pygame.K_x:
                        if wind.getScale() > 1:
                            currScale -= 0.1
                            wind.setScale(currScale)
                if event.key == pygame.K_p:
                    pause = not pause 

            if wind.getScale() == 1:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for planet in planets:
                        if planet.circ.collidepoint(pygame.mouse.get_pos()):
                            print(planet.name) 
                        if planet.info_circ.collidepoint(pygame.mouse.get_pos()):
                            print(planet.name)                           
        pygame.display.update()
 
    pygame.quit()
 
 
main()