import pygame
from pygame.locals import *
import sys
import random

game_state = "menu"  # "menu", "playing", "game_over" eller "win"
wave = 1             # NY: hvilken wave vi er på
max_waves = 3        # NY: hvor mange waves det er totalt

pygame.init() # Starter opp pygame-biblioteket så vi kan bruke det

clock = pygame.time.Clock()
fps = 60

screen_width = 600
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Leos Spill")

# Definerer farger som RGB verdier
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)


# Laster inn bakgrunnsbildet fra img-mappen
bg = pygame.image.load("img/bg.png")

# Laster inn tittelbilde og endre hvor stor den er
title = pygame.image.load("img/Invaders in space.png")
title = pygame.transform.scale(title, (540, 270))

# Funksjon som tegner bakgrunnen på skjermen
def draw_bg():
    screen.blit(bg, (0, 0))
# Tegner tittelen øverst på skjermen (vises i menyen)
def draw_title():
    screen.blit(title, (35, 0))


# Farger brukt til knapper og bakgrunn i menyskjermen
BG_COLOR = (30, 30, 30)
BUTTON_COLOR = (70, 130, 180)
HOVER_COLOR = (100, 170, 220)
TEXT_COLOR = (255, 255, 255)



# Fonter som spillet bruker til å skrive tekst på skjermen (f.eks. wave 1, game over, osv.)
font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 72)



# Funksjon som skriver tekst midt på skjermen
def draw_text(text, font, color, y):
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect(center=(screen_width / 2, y))
    screen.blit(text_surf, text_rect)


# Klasse for knapper som vises i menyen
class Button:
    def __init__(self, text, x, y, w, h):
        self.text = text # Teksten som vises på knappen
        self.rect = pygame.Rect(x, y, w, h) # Knappens posisjon og størrelse

    def draw(self, surface):
        color = HOVER_COLOR if self.rect.collidepoint(pygame.mouse.get_pos()) else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect) # Tegner knappebakgrunnen
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2) # Tegner svart kantlinje

        # Tegner knappeteksten sentrert i knappen
        text_surf = font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )

# Lager de to knappene i menyen med posisjon og størrelse
buttons = [
    Button("Play", 200, 300, 200, 50),
    Button("Quit", 200, 370, 200, 50),
]


# Klasse for spillerens romskip
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y):  # Lager skipet på spillet
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/spaceship.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y] 
        self.last_shot = pygame.time.get_ticks()

    # Funksjon som oppdaterer romskipet hvert bilde (frame)
    def update(self):
        speed = 8  # Bevegelseshastighet i piksler per frame

        # Keys for spillet aka (Henter hvilke taster som trykkes ned akkurat nå)
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= speed
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += speed

    # NY: Egen funksjon for å skyte (kalles ved ETT trykk på space)
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)  # Lager en ny kule fra toppen av romskipet
        bullet_group.add(bullet)   # Legger kulen til bullet_group så den oppdateres og tegnes


# Klasse for kuler som romskipet skyter
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()
        # Sjekker om kulen treffer en fiende
        if pygame.sprite.spritecollide(self, alien_group, True):
            self.kill()


# ====== NY: Klasse for fiendene (aliens) ======
class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # Velger et tilfeldig alien-bilde (alien1 til alien5)
        nummer = random.randint(1, 5)
        self.image = pygame.image.load("img/alien" + str(nummer) + ".png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        # Fienden beveger seg nedover
        self.rect.y += 1


# lage sprite grupper
Spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()   # NY: gruppe for fiender

# lage spilleren
spaceship = Spaceship(screen_width / 2, screen_height - 100)
Spaceship_group.add(spaceship)


# ====== NY: Funksjon som lager fiendene på toppen ======
def lag_aliens(rader):
    alien_group.empty()  # Fjerner gamle fiender først
    for rad in range(rader):      # Antall rader bestemmes av wave
        for kolonne in range(6):  # 6 fiender i hver rad
            x = 60 + kolonne * 90
            y = 50 + rad * 70
            alien = Alien(x, y)
            alien_group.add(alien)

# NY: Gir antall rader for hver wave (wave 1=2, wave 2=4, wave 3=5)
def rader_for_wave(wave):
    if wave == 1:
        return 2
    elif wave == 2:
        return 4
    else:
        return 5


run = True
while run:
    clock.tick(fps)
    draw_bg()
    if game_state == "menu":
        draw_title()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # NY: Skyter når man TRYKKER space (kun ett skudd per trykk)
        if game_state == "playing":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                spaceship.shoot()

        # Knappe-trykk håndteres inne i event-løkka
        if game_state == "menu":
            for button in buttons:
                if button.clicked(event):
                    if button.text == "Play":
                        game_state = "playing"
                        wave = 1       # NY: starter alltid på wave 1
                        lag_aliens(rader_for_wave(wave))   # NY: lager fiendene for wave 1
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
        alien_group.update()   # NY: oppdaterer fiendene

        Spaceship_group.draw(screen)
        bullet_group.draw(screen)
        alien_group.draw(screen)   # NY: tegner fiendene

        # NY: Viser hvilken wave vi er på øverst på skjermen
        draw_text("Wave " + str(wave), font, white, 30)

        # NY: Sjekker om noen fiende har nådd bunnen -> game over
        for alien in alien_group:
            if alien.rect.bottom >= screen_height:
                game_state = "game_over"
                slutt_tid = pygame.time.get_ticks()   # NY: husker når det ble game over

        # NY: Sjekker om alle fiendene i denne wave er døde
        if len(alien_group) == 0:
            if wave < max_waves:
                wave += 1        # Går til neste wave
                lag_aliens(rader_for_wave(wave))     # Lager nye fiender for denne wave
            else:
                game_state = "win"   # Alle waves er klaret -> du vant!
                slutt_tid = pygame.time.get_ticks()   # NY: husker når du vant

    elif game_state == "game_over":
        # NY: Viser game over-skjerm
        draw_text("GAME OVER", big_font, red, screen_height / 2)
        # NY: Etter 2 sekunder -> tilbake til menyen
        if pygame.time.get_ticks() - slutt_tid > 2000:
            game_state = "menu"

    elif game_state == "win":
        # NY: Viser seier-skjerm
        draw_text("DU VANT!", big_font, green, screen_height / 2)
        # NY: Etter 2 sekunder -> tilbake til menyen
        if pygame.time.get_ticks() - slutt_tid > 2000:
            game_state = "menu"

    pygame.display.update()

pygame.quit()