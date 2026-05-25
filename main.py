import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 600
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Leos Spill")

bg = pygame.image.load("img/bg.png")

def draw_bg():
    screen.blit(bg, (0, 0))


# lage spaceship class
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/spaceship.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.health = health
        self.cooldown = 500  # milliseconds
        self.game_over = 0
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        # set movement speed
        speed = 8

        # get key press
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= speed
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += speed


# lage sprite grupper
Spaceship_group = pygame.sprite.Group()

# lage spilleren
spaceship = Spaceship(screen_width / 2, screen_height - 100, 100)
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

    # tegne sprite grupper
    Spaceship_group.draw(screen)

    pygame.display.update()

pygame.quit()