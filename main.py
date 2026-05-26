import pygame
from pygame.locals import *

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



# Funksjon som tegner bakgrunnen på skjermen
def draw_bg():
    screen.blit(bg, (0, 0))




# Klasse for spillerens romskip
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, health, lives): # LAger skipet på spillet 
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

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # update spaceship
    spaceship.update()

    # update bullets
    bullet_group.update()

    # tegne sprite grupper
    Spaceship_group.draw(screen)
    bullet_group.draw(screen)

    pygame.display.update()

pygame.quit()