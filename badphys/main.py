import pygame

pygame.init()

screen = pygame.display.set_mode((200, 200))
font = pygame.

clock = pygame.Clock()

running = True

while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    clock.tick(60)
