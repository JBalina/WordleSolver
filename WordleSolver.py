from random import randint

def readFile(txtFile):
    items = []
    with open(txtFile,'r') as f:
        items = f.read().splitlines()
    return items

def narrowDown(wordBank, letter, status, index=0):
    newWordBank = []
#     status = int(status)
#     index = int(index)
    for word in wordBank:
        #if not in word
        if status == "b":
            if letter not in word:
                    newWordBank.append(word)
        else:
            #if in word but wrong placement
            if status == "y":
                if letter in word and letter != word[int(index)]:
                    newWordBank.append(word)
            #check if matches placement
            elif letter == word[int(index)]:
                newWordBank.append(word)
    return newWordBank

def check(ans, guess):
    result = ""
    for i in range(0,5):
        if ans[i] == guess[i]:
            result += "g"
        elif guess[i] in ans:
            result += "y"
        else:
            result += "b"
    return result

def wordle(words):
    ans = words[randint(0,len(words)-1)]
    tries = 0
    uInput = ""
    result = ""
    while uInput != ans and tries != 6:
        uInput = input()
        if len(uInput) != 5:
            print("Guess must be 5 letters long.")
        elif uInput not in words:
            print("Guess does not exist in dictionary.")
        else:
            result = check(ans, uInput)
            print(result)
            tries += 1
        if result == "ggggg":
            print("Your win!")
        elif tries == 6:
            print("Game over! The answer was " + ans)
        
        result = ""

def wordleSolver(words):
    items = words
    uInput = ""
    while uInput != "Quit":
        uInput = input()
        if uInput != "Quit":
            inputList = uInput.split(" ")
            if len(inputList) == 3:
                items = narrowDown(items, inputList[0],inputList[1],inputList[2])
            else:
                items = narrowDown(items, inputList[0], inputList[1])
            print(items)
            print(len(items))



#words = readFile('wordle-answers-alphabetical.txt')
#words = readFile('sgb-words.txt')
#wordleSolver(words)




