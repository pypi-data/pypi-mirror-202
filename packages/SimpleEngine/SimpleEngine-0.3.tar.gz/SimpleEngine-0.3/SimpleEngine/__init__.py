import pygame
from PIL import Image

WHITE = (255, 255, 255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
CYAN = (0,255,255)
MAGENTA = (255,0,255)
GRAY = (128,128,128)

keyPressed = ""

def StartGame(update, start):
    start()
    setFPS()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keyPressed = pygame.key.get_pressed()
        update()
    
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
        self.hitbox = pygame.Rect(self.x-(self.width/2), self.y-(self.height/2), self.width, self.height)
    
    def move(self, x, y):
        self.x += x
        self.y += y
    
    def draw(self, clr=WHITE):
        self.hitbox = pygame.Rect(self.x-(self.width/2), self.y-(self.height/2), self.width, self.height)
        pygame.draw.rect(self.screen, clr, self.hitbox)
    
    def drawHitbox(self):
        pygame.draw.rect(self.screen, GREEN, self.hitbox,  2)

class Circle():
    def __init__(self, x, y, radius, screen):
        self.x = x
        self.y = y
        self.radius = radius
        self.screen = screen
        self.hitbox = pygame.Rect(self.x-self.radius, self.y-self.radius, self.radius*2, self.radius*2)
    
    def move(self, x, y):
        self.x += x
        self.y += y
    
    def draw(self, clr=WHITE):
        self.hitbox = pygame.Rect(self.x-self.radius, self.y-self.radius, self.radius*2, self.radius*2)
        pygame.draw.circle(self.screen, clr, (self.x, self.y), self.radius)
        
    
    def drawHitbox(self):
        pygame.draw.rect(self.screen, GREEN, self.hitbox,  2)

class Triangle():
    def __init__(self, x, y, width, height, screen):
        self.width = width
        self.height = height
        self.screen = screen
        self.hitbox = pygame.Rect(self.x1, self.y1, self.width, self.height)
        self.x1 = 0
        self.x2 = 0
        self.y1 = 0
        self.y2 = 0
        self.x3 = 0
        self.y3 = 0
        self.move(x, y)
    
    def move(self, x, y):
        self.x1 += x
        self.y1 += y-(self.height/2)
        self.x2 += x-(self.width/2)
        self.y2 += y+(self.height/2)
        self.x3 += x+(self.width/2)
        self.y3 += y+(self.height/2)


    def draw(self, clr=WHITE):
        self.hitbox = pygame.Rect(self.x1-(self.width/2), self.y1, self.width, self.height)
        pygame.draw.polygon( self.screen, clr, ((self.x1, self.y1), (self.x2, self.y2), (self.x3, self.y3)) )
    
    def drawHitbox(self):
        pygame.draw.rect(self.screen, GREEN, self.hitbox,  2)

class Sprite(pygame.sprite.Sprite):
    def __init__(self, x, y, screen,image):
        super().__init__()
        self.x = x
        self.y = y
        self.img = image
        self.image = pygame.image.load(image)
        self.hitbox = pygame.Rect(self.x-(Image.open(self.img).width/2), self.y-(Image.open(self.img).height/2), Image.open(self.img).width, Image.open(self.img).height)
        self.screen = screen

    def move(self, x, y):
        self.x += x
        self.y += y

    def draw(self):
        self.hitbox = pygame.Rect(self.x-(Image.open(self.img).width/2), self.y-(Image.open(self.img).height/2), Image.open(self.img).width, Image.open(self.img).height)
        self.screen.blit(self.image, (self.x-(Image.open(self.img).width/2), self.y-(Image.open(self.img).height/2)))
    
    def drawHitbox(self):
        pygame.draw.rect(self.screen, GREEN, self.hitbox,  2)

def createWindow(width, height, name):
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(name)
    return screen

def fillScreen(screen, color):
    screen.fill(color)

def updateScreen():
    pygame.display.update()

def collisionCheck(rect1, rect2):
    return pygame.Rect.colliderect(rect1, rect2)

def GetKeysPressed():
    return pygame.key.get_pressed()