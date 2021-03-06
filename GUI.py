import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from WordleSolver import readFile, readPresavedEntropy, narrowDown, narrowDownList, check, allResultsRec, calcEntropy
from random import randint
import time

pygame.init()

#A single cube object to be drawn. Each cube will be able to hold a letter and a status.
class Cube:
    def __init__(self, value, row, col, width, height):
        self.value = value
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False
        #"" = not yet submitted
        #g = green/correct letter and placement
        #y = yellow/correct letter wrong placement
        #b = black/incorrect letter
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

#Grid to hold the cubes into a 6x5 grid. Also displays the list of items and their entropy.
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
        
    #updates the letter of a cube after the user has typed a letter in
    #Also updates where the cursor is (which cube is currently selected)
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
            
    #Goes over the cases when the user hits the enter button.
    #It will first check if the user inputed a full word. If it is in solver mode, pressing
    #enter will update the entropy list with the input given. If not in solver mode, it will
    #check first if the word is in the word bank. Then it will compare the guess with the answer
    #and form a result as well as update the colors of the cubes to match the result. It will 
    #use the result to update the entropy list. If the user wins or loses, it will prompt the
    #user to press enter to play again.
    def enter(self):
        if not (self.selected[1] == self.cols-1 and self.cubes[self.selected[0]][self.selected[1]].value != ""):
            self.message = ["Not enough letters!"]
        elif not self.solver:
            word = ""
            for i in range(self.cols):
                word += self.cubes[self.selected[0]][i].value
            if(word in self.wordBank):
                result = check(self.ans, word)
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
            #self.message = ["Word not in word bank"]
        return True
    
    #This function erases the letter in the current block and moves the cursor back,
    #unless the cursor is already in the first cube.
    def backspace(self):
        if self.selected[1] != 0:
            if not (self.selected[1] != self.cols and self.cubes[self.selected[0]][self.selected[1]].value != ""):
                self.cubes[self.selected[0]][self.selected[1]].selected = False
                self.selected = (self.selected[0],self.selected[1]-1)
                self.cubes[self.selected[0]][self.selected[1]].selected = True
            self.cubes[self.selected[0]][self.selected[1]].value = ""
            self.cubes[self.selected[0]][self.selected[1]].status = "n"
                        
    #Only usable in solve mode. Change the state of the current cube.
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
                
    #Only usable in solve mode. Change the state of the current cube.
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
    
    #Updates the entropy list. Narrows down the answers and sorts the list by its entropy.
    def updateNarrowedEntropy(self):
        start = time.time()
        self.narrowedEntropy = [[word, calcEntropy(word, self.resultsList,self.narrowedWB)] for word in self.narrowedWB]
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
    wordBankName = "sgb-words.txt"
    solver = True
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
                    elif event.key == pygame.K_UP and grid.solver:
                        grid.up()
                    elif event.key == pygame.K_DOWN and grid.solver:
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