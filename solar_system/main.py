import pygame
import math
import enum
 
#создается класс перечислений, наследуемый от enum.Enum
class Colors(enum.Enum):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    YELLOW = (255, 255, 0)

class Window:
    def __init__(self, width=1200, height=800, scale=1):
        self.W = width
        self.H = height
        self._scale = scale
        self._WIN = pygame.display.set_mode((self.W, self.H))
        self._draw_Surface = pygame.Surface((self.W, self.H))
        self._scale_Surface = pygame.Surface(self.get_resolution())
        pygame.display.set_caption('Planet Simulation')
        self.bg = pygame.image.load("images\space.jpg")
        pygame.font.init()
        self.my_font = pygame.font.SysFont('Comic Sans MS', 100)
        self._text_surface = self.my_font.render('Some Text', False, Colors.WHITE.value)
        self.textRect = self._text_surface.get_rect()
        
 
    def get_resolution(self):
        return self.W * self._scale, self.H * self._scale
 
    def update_Scale(self):
        self._WIN.fill(Colors.BLACK.value)
        self._scale_Surface = pygame.Surface(self.get_resolution())
        pygame.transform.smoothscale(self._draw_Surface, self.get_resolution(), self._scale_Surface)
        self._WIN.blit(self._scale_Surface, ((-((self.W * self._scale) - self.W) / 2), (-((self.H * self._scale) - self.H)) / 2))
 
    def fill(self, color=Colors.BLACK):
        self._draw_Surface.fill(color.value)
        
    def blit_bg(self):
        self._draw_Surface.blit(self.bg, (0,0))
    
    def blit_t(self):
        self._text_surface.blit(self._text_surface, (100,100))

    def get_draw_Surface(self):
        return self._draw_Surface
 
    def get_Scale(self):
        return self._scale
 
    def set_Scale(self, scale):
        try:
            if scale <= 0:
                raise ValueError('scale can`t be below zero')
            self._scale = scale
        except ValueError as err:
            raise
        

class Planet:
	def __init__(self, name, radius, color, coef, distance):
		self.rad = 0
		self.radius = radius
		self.color = color
		self.distance_to_sun = 0
		self.coef = coef
		self.distance = distance
		self.name = name
		self.x = 0
		self.y = 0
		self.angle = 0
        		
	def get_angle(self):
		self.angle = self.rad * 180 / math.pi % 360
		return self.angle

	def draw(self, win):
		self.x = int(math.cos(self.rad) * self.distance) + win.W / 2
		self.y = int(math.sin(self.rad) * self.distance) + win.H / 2

		self.circ = pygame.draw.circle(win.get_draw_Surface(), self.color, (self.x, self.y), self.radius)

		self.rad += self.coef
		
	def draw_info(self, win, num):
		self.info_circ = pygame.draw.circle(win.get_draw_Surface(), self.color, (50 + num * 50, 50), 20)

	

r_earth = 9

fin = open ("planets.txt", 'r')

#Объявление планет в списке
planets = []
for line in fin:
    plan = line.split()
    planets.append(Planet(str(plan[0]), float(plan[1]) * r_earth, (int(plan[2]), int(plan[3]), int(plan[4])), 10 / float(plan[5]), int(plan[6]) ))

fin.close()

inf = open ("info.txt", "r", encoding="UTF-8")
l_info = inf.readlines()
 
clock = pygame.time.Clock()
# MainLoop
def main():

    wind = Window()
    currScale = 1
    run = True
    pause = False
    while run:
        if not pause:
            clock.tick(60)
            wind.fill(Colors.BLACK)
            wind.blit_bg()
            wind.blit_t()
            sun = pygame.draw.circle(wind.get_draw_Surface(), Colors.YELLOW.value, (wind.W / 2, wind.H / 2), 4)

            for i, planet in enumerate(planets):
                planet.draw(wind)
                planet.draw_info(wind, i)

            wind.update_Scale()
 
        # EventHandle
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # Buttons
            if event.type == pygame.KEYDOWN:
                if not pause:
                    if event.key == pygame.K_z:
                        if wind.get_Scale() < 3:
                            currScale += 0.1
                            wind.set_Scale(currScale)
                    if event.key == pygame.K_x:
                        if wind.get_Scale() > 1:
                            currScale -= 0.1
                            wind.set_Scale(currScale)
                if event.key == pygame.K_p:
                    pause = not pause 

            if wind.get_Scale() == 1:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i, planet in enumerate(planets):
                        if (planet.circ.collidepoint(pygame.mouse.get_pos()) or planet.info_circ.collidepoint(pygame.mouse.get_pos())):
                            print(planet.name) 
                            print("Угол", planet.get_angle())
                            print(l_info[i]) 
                                             
        pygame.display.update()
 
    pygame.quit()
 
 
main()
inf.close()