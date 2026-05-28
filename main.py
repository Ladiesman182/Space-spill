import pygame
from pygame.locals import *
import sys

game_state = "menu"  # "menu" eller "playing" 

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 600
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Leos Spill")

# Definerer farger som RGB-verdier
red = (255, 0, 0)
green = (0, 255, 0)



# Laster inn bakgrunnsbildet fra img-mappen
bg = pygame.image.load("img/bg.png") 

title = pygame.image.load("img/Invaders in space.png")

title = pygame.transform.scale(title,(540,270))

# Funksjon som tegner bakgrunnen på skjermen
def draw_bg():
    screen.blit(bg, (0, 0))

def draw_title():
    screen.blit(title, (35, 0))    


# Colors
BG_COLOR = (30, 30, 30)
BUTTON_COLOR = (70, 130, 180)
HOVER_COLOR = (100, 170, 220)
TEXT_COLOR = (255, 255, 255)

# Font
font = pygame.font.SysFont(None, 36)

# Button class
class Button:
    def __init__(self, text, x, y, w, h):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self, surface):
        color = HOVER_COLOR if self.rect.collidepoint(pygame.mouse.get_pos()) else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)

        text_surf = font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )

# Create buttons
buttons = [
    Button("Play", 200, 300, 200, 50),
    Button("Quit", 200, 370, 200, 50),
    
]









# Klasse for spillerens romskip
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, health, lives): # Lager skipet på spillet 
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/spaceship.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.health_start = health
        self.health_remaining = health
        self.last_shot = pygame.time.get_ticks()
        self.lives = lives



  # Funksjon som oppdaterer romskipet hvert bilde (frame)
    def update(self):
        speed = 8  # Bevegelseshastighet i piksler per frame
        cooldown = 500    # Tid i millisekunder mellom hvert skudd




        # Keys for spillet aka (Henter hvilke taster som trykkes ned akkurat nå)
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= speed
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += speed


        # Henter nåværende tid i millisekunder
        time_now = pygame.time.get_ticks()



        # Skyter en kule hvis mellomrom trykkes og nok tid har gått siden siste skudd
        if key[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
            bullet = Bullet(self.rect.centerx, self.rect.top)  # Lager en ny kule fra toppen av romskipet 
            bullet_group.add(bullet)   # Legger kulen til bullet_group så den oppdateres og tegnes
            self.last_shot = time_now   # Oppdaterer tidspunktet for siste skudd



        # health bar
        pygame.draw.rect(screen, red, (self.rect.x, (self.rect.y + self.rect.height + 10), self.rect.width, 15))
        if self.health_remaining > 0:
            pygame.draw.rect(screen, green, (self.rect.x, (self.rect.y + self.rect.height + 10), int(self.rect.width * (self.health_remaining / self.health_start)), 15))






# Klasse for kuler som romskipet skyter
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    # fikset: update er nå utenfor __init__, og duplikaten er fjernet
    def update(self):
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()


# lage sprite grupper
Spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()

# lage spilleren
spaceship = Spaceship(screen_width / 2, screen_height - 100, 100, 3)
Spaceship_group.add(spaceship)

run = True
while run:
    clock.tick(fps)
    draw_bg()
    draw_title()
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # Knappe-trykk håndteres inne i event-løkka
        if game_state == "menu":
            for button in buttons:
                if button.clicked(event):
                    if button.text == "Play":
                        game_state = "playing"
                    if button.text == "Quit":
                        pygame.quit()
                        sys.exit()

    if game_state == "menu":
        Spaceship_group.draw(screen)
        for button in buttons:
            button.draw(screen)

    elif game_state == "playing":
        spaceship.update()
        bullet_group.update()
        Spaceship_group.draw(screen)
        bullet_group.draw(screen)

    pygame.display.update()

pygame.quit()