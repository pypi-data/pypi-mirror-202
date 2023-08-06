import pygame

WHITE = (255, 255, 255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
CYAN = (0,255,255)
MAGENTA = (255,0,255)
GRAY = (128,128,128)


def StartGame(update, start):
    start()
    setFPS()
    running = True
    while running:
        update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
def setFPS(fps=30):
    clock = pygame.time.Clock()
    clock.tick(fps)
    
    

class Rect():
    def __init__(self, x, y, width, height, screen):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen = screen
    
    def draw(self, x, y, clr=WHITE):
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(self.screen, clr, rect)

class Circle():
    def __init__(self, x, y, radius, screen):
        self.x = x
        self.y = y
        self.radius = radius
        self.screen = screen
    
    def draw(self, x, y, clr=WHITE):
        pygame.draw.circle(self.screen, clr, (self.x, self.y), self.radius)

class Triangle():
    def __init__(self, x, y, width, height, screen):
        self.width = width
        self.height = height
        self.screen = screen
        self.updatePosition(x, y)
    
    def updatePosition(self, x, y):
        self.x1 = x
        self.y1 = y-(self.height/2)
        self.x2 = x-(self.width/2)
        self.y2 = y+(self.height/2)
        self.x3 = x+(self.width/2)
        self.y3 = y+(self.height/2)

    def draw(self, x, y, clr=WHITE):
        self.updatePosition(x, y)
        pygame.draw.polygon( self.screen, clr, ((self.x1, self.y1), (self.x2, self.y2), (self.x3, self.y3)) )

class Sprite(pygame.sprite.Sprite):
    def __init__(self, x, y, screen,image):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.image.load(image)
        self.screen = screen
    
    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))

def createWindow(width, height, name):
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(name)
    return screen

def fillScreen(screen, color):
    screen.fill(color)
