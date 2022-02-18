import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from WordleSolver import readFile, readPresavedEntropy, narrowDown, narrowDownList, check, allResultsRec, calcEntropy
from random import randint
import time

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
            text = fnt.render(str(self.value), True, (255, 255, 255))
            win.blit(text, (x+(self.width/3),y+(self.height/3)))
            
    def set(self, val):
        self.value = val

class Grid:
    
    def __init__(self, width, height, wordBankName, solver, rows = 6, cols = 5):
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube("", i, j, width/cols, height/rows) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.selected = (0,0)
        self.cubes[0][0].selected = True
        self.wordBank = readFile(wordBankName)
        self.narrowedWB = self.wordBank
        self.solver = solver
        if solver:
            self.ans = ""
        else:
            self.ans = self.wordBank[randint(0,len(self.wordBank)-1)]
        self.resultsList = allResultsRec(cols)
        self.narrowedEntropy = readPresavedEntropy("narrowedEntropy-"+wordBankName)
        self.message = []
        
    def draw(self, win):
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(win)
        self.drawList(win, 600, 25)
        self.drawMessage(win, 600, 350)
        
                
    def updateCurrent(self, letter):
        if self.solver:
            self.cubes[self.selected[0]][self.selected[1]].status = "b"
        if self.selected[1] != self.cols-1:
            self.cubes[self.selected[0]][self.selected[1]].value = letter
            self.cubes[self.selected[0]][self.selected[1]].selected = False
            self.selected = (self.selected[0],self.selected[1]+1)
            self.cubes[self.selected[0]][self.selected[1]].selected = True
        elif self.selected[1] == self.cols-1 and self.cubes[self.selected[0]][self.selected[1]].value == "":
            self.cubes[self.selected[0]][self.selected[1]].value = letter
            
    def enter(self):
        if not (self.selected[1] == self.cols-1 and self.cubes[self.selected[0]][self.selected[1]].value != ""):
            self.message = ["Not enough letters!"]
        elif not self.solver:
            word = ""
            for i in range(self.cols):
                word += self.cubes[self.selected[0]][i].value
            if(word in self.wordBank):
                result = check(self.ans, word)
                #print(result)
                #self.narrowedWB = narrowDownList(self.narrowedWB, word, result)
                for i in range(self.cols):
                    self.cubes[self.selected[0]][i].status = result[i]
                    self.narrowedWB = narrowDown(self.narrowedWB, word[i], result[i], i)
                if result == "ggggg":
                    self.message = ["You win!", "Press enter to play again!"]
                    return False
                print(len(self.narrowedWB))
                if self.selected[0] == self.rows-1:
                    self.message = ["Game over!", "Press enter to play again!"]
                    return False
                self.updateNarrowedEntropy()
                self.cubes[self.selected[0]][self.selected[1]].selected = False
                self.selected = (self.selected[0]+1, 0)
                self.cubes[self.selected[0]][self.selected[1]].selected = True
                self.message = []
            else:
                self.message = ["Word not in word bank"]
        elif self.solver:
            word = ""
            for i in range(self.cols):
                word += self.cubes[self.selected[0]][i].value
            result = ""
            for i in range(self.cols):
                result += self.cubes[self.selected[0]][i].status
                self.narrowedWB = narrowDown(self.narrowedWB, word[i], result[i], i)
            if self.selected[0] == self.rows-1:
                return False
            self.updateNarrowedEntropy()
            self.cubes[self.selected[0]][self.selected[1]].selected = False
            self.selected = (self.selected[0]+1, 0)
            self.cubes[self.selected[0]][self.selected[1]].selected = True
            self.message = ["Word not in word bank"]
        return True
    
    def backspace(self):
        #self.cubes[self.selected[0]][self.selected[1]].value = ""
        if self.selected[1] != 0:
            if not (self.selected[1] != self.cols and self.cubes[self.selected[0]][self.selected[1]].value != ""):
                self.cubes[self.selected[0]][self.selected[1]].selected = False
                self.selected = (self.selected[0],self.selected[1]-1)
                self.cubes[self.selected[0]][self.selected[1]].selected = True
            self.cubes[self.selected[0]][self.selected[1]].value = ""
            self.cubes[self.selected[0]][self.selected[1]].status = "n"
                        
    def up(self):
        if self.selected[1] != 0:
            x = self.selected[0]
            y = 0
            if self.selected[1] == self.cols-1 and self.cubes[self.selected[0]][self.selected[1]].value != "":
                y = self.selected[1]
            else:
                y = self.selected[1]-1
            if self.cubes[x][y].status == "n" or self.cubes[x][y].status == "b":
                self.cubes[x][y].status = "g"
            elif self.cubes[x][y].status == "g":
                self.cubes[x][y].status = "y"
            elif self.cubes[x][y].status == "y":
                self.cubes[x][y].status = "b"
                
    def down(self):
        if self.selected[1] != 0:
            x = self.selected[0]
            y = 0
            if self.selected[1] == self.cols-1 and self.cubes[self.selected[0]][self.selected[1]].value != "":
                y = self.selected[1]
            else:
                y = self.selected[1]-1
            if self.cubes[x][y].status == "n" or self.cubes[x][y].status == "b":
                self.cubes[x][y].status = "y"
            elif self.cubes[x][y].status == "y":
                self.cubes[x][y].status = "g"
            elif self.cubes[x][y].status == "g":
                self.cubes[x][y].status = "b"
                
    def updateNarrowedEntropy(self):
        start = time.time()
        self.narrowedEntropy = [[word, calcEntropy(word, self.resultsList,self.narrowedWB)] for word in self.narrowedWB]
#         for word in self.narrowedWB:
#             print(word)
#             self.narrowedEntropy.append([word, calcEntropy(word, self.resultsList,self.narrowedWB)])
        self.narrowedEntropy.sort(reverse = True,key = lambda i: i[1])
        end = time.time()
        print("updateNarrowedEntropy: " + str(end-start))
            
    def drawList(self, win, x_pos, y_pos):
        fontSize = 30
        fnt = pygame.font.SysFont("comicsans", fontSize)
        x = x_pos
        y = y_pos
        i = 0
        while i < 20 and i < len(self.narrowedEntropy):
            if i == 10:
                x += 200
            text = fnt.render(str(i+1)+": "+self.narrowedEntropy[i][0] + "     " + str(round(self.narrowedEntropy[i][1],2)), True, (255, 255, 255))
            win.blit(text, (x, y+((i%10)*fontSize)))
            i += 1

    def drawMessage(self, win, x_pos, y_pos):
        fontSize = 30
        fnt = pygame.font.SysFont("comicsans", fontSize)
        for i in range(len(self.message)):
            text = fnt.render(self.message[i], True, (255, 255, 255))
            win.blit(text, (x_pos,y_pos+(i+1)*fontSize))
        
def drawWindow(WIN, grid):
    WIN.fill((75,75,75))
    grid.draw(WIN)
    pygame.display.update()

def main():
    WIDTH, HEIGHT = 1000, 620
    WIN = pygame.display.set_mode((WIDTH,HEIGHT))
    FPS = 60
    clock = pygame.time.Clock()
    pygame.display.set_caption("Wordle Solver")
#     wordBank = readFile('sgb-words.txt')
    #wordBank = readFile('wordle-answers-alphabetical.txt')
    wordBankName = "sgb-words.txt"
    solver = False
    grid = Grid(500,540, wordBankName, solver)
    run = True
    playing = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif playing:
                if event.type == pygame.KEYDOWN:
                    if pygame.key.name(event.key).isalpha() and len(pygame.key.name(event.key)) == 1:
                        grid.updateCurrent(pygame.key.name(event.key))
                    elif event.key == pygame.K_RETURN:
                        playing = grid.enter()
                    elif event.key == pygame.K_BACKSPACE:
                        grid.backspace()
                    elif event.key == pygame.K_ESCAPE:
                        run = False
                    elif event.key == pygame.K_UP:
                        grid.up()
                    elif event.key == pygame.K_DOWN:
                        grid.down()
            elif not playing:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        grid = Grid(500,540, wordBankName, False)
                        playing = True
                    elif event.key == pygame.K_ESCAPE:
                        run = False
        drawWindow(WIN, grid)
    pygame.quit()
    
if __name__ == "__main__":
    main()