import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
#from WordleSolver import wordle, wordleSolver
pygame.init()

WIDTH, HEIGHT = 740, 650
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Wordle Solver")

def main():
    run = True
    while run:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        WIN.fill((75,75,75))
        pygame.display.update()
    pygame.quit()
    
if __name__ == "__main__":
    main()