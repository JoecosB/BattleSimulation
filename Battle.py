import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((1440, 800))
screen.fill('white')
pygame.display.flip()
start = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == 13:
                start = 1
        
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()