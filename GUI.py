import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from WordleSolver import readFile, narrowDown, check
from random import randint

pygame.init()

class Cube:
    def __init__(self, value, row, col, width, height):
        self.value = value
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False
        #0 = not yet submitted
        #1 = green/correct letter and placement
        #2 = yellow/correct letter wrong placement
        #3 = black/incorrect letter
        self.status = "n";

    def draw(self, win):
        fnt = pygame.font.SysFont("comicsans", 80)
        
        x = (self.col) * (self.width+5)+20
        y = (self.row) * (self.height+5)+20
        if self.status == "n":
            pygame.draw.rect(win, (100,100,100), (x, y, self.width, self.height), 2, border_radius=1)
        elif self.status == "g":
            pygame.draw.rect(win, (100,255,100), (x, y, self.width, self.height))
        elif self.status == "y":
            pygame.draw.rect(win, (255,255,100), (x, y, self.width, self.height))
        if self.value != "":
            text = fnt.render(str(self.value), 1, (255, 255, 255))
            win.blit(text, (x+(self.width/3),y+(self.height/3)))
    def set(self, val):
        self.value = val

class Grid:
    
    def __init__(self, width, height, wordBank, rows = 6, cols = 5):
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube("", i, j, width/cols, height/rows) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.selected = (0,0)
        self.cubes[0][0].selected = True
        self.wordBank = wordBank
        self.narrowedWB = wordBank
        self.ans = wordBank[randint(0,len(wordBank)-1)]
        
    def draw(self, win):
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(win)
                
    def updateCurrent(self, letter):
        if self.selected[1] != self.cols-1:
            self.cubes[self.selected[0]][self.selected[1]].value = letter
            self.cubes[self.selected[0]][self.selected[1]].selected = False
            self.selected = (self.selected[0],self.selected[1]+1)
            self.cubes[self.selected[0]][self.selected[1]].selected = True
        elif self.selected[1] == self.cols-1 and self.cubes[self.selected[0]][self.selected[1]].value == "":
            self.cubes[self.selected[0]][self.selected[1]].value = letter
            
    def enter(self):
        if self.selected[1] == self.cols-1 and self.cubes[self.selected[0]][self.selected[1]].value != "":
            word = ""
            for i in range(self.cols):
                word += self.cubes[self.selected[0]][i].value
            if(word in self.wordBank):
                result = check(self.ans, word)
                for i in range(self.cols):
                    self.cubes[self.selected[0]][i].status = result[i]
                    self.narrowedWB = narrowDown(self.narrowedWB, word[i], result[i], i)
                print(self.narrowedWB)
                if self.selected[0] == self.rows-1:
                    print("Game over!")
                    return False
                self.cubes[self.selected[0]][self.selected[1]].selected = False
                self.selected = (self.selected[0]+1, 0)
                self.cubes[self.selected[0]][self.selected[1]].selected = True
            else:
                print("Word not in word bank")
        else:
            print("Not enough letters!")
        return True


def drawWindow(WIN, grid):
    WIN.fill((75,75,75 ))
    grid.draw(WIN)
    pygame.display.update()

def main():
    WIDTH, HEIGHT = 740, 650
    WIN = pygame.display.set_mode((WIDTH,HEIGHT))
    FPS = 60
    clock = pygame.time.Clock()
    pygame.display.set_caption("Wordle Solver")
    wordBank = readFile('sgb-words.txt')
    grid = Grid(500,540, wordBank)
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if pygame.key.name(event.key).isalpha() and len(pygame.key.name(event.key)) == 1:
                    grid.updateCurrent(pygame.key.name(event.key))
                elif event.key == pygame.K_RETURN:
                    run = grid.enter()
                #elif event.key == pygame.K_BACKSPACE:
                    
        drawWindow(WIN, grid)
    pygame.quit()
    
if __name__ == "__main__":
    main()