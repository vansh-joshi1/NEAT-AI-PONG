# NEAT AI PONG
# Team: Vansh Joshi, Om Patel, Mathew Phan, Sarvvesh Vinodkumar
# Overview: This outputs a window pong game window with the "Pong" title at the top

import pygame

pygame.init()

WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

def main():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        WIN.fill((0, 0, 0))  # Fill the window with black color
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()