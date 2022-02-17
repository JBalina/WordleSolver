from random import randint
import math

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

def allResults():
    letters = ["b","g","y"]
    resultList = []
    for letter1 in letters:
        for letter2 in letters:
            for letter3 in letters:
                for letter4 in letters:
                    for letter5 in letters:
                        resultList.append(letter1+letter2+letter3+letter4+letter5)
    return resultList
    
def allResultsHelper(letters, resultList, string, digits):
    if digits == 0:
        return
    else:
        for letter in letters:
            nextDigit = digits-1
            nextWord = string+letter
            if len(nextWord)==5:
                resultList.append(nextWord)
            allResultsHelper(letters, resultList, nextWord, nextDigit)
        
def allResultsRec(digits):
    resultList = []
    allResultsHelper(["b","g","y"], resultList, "", digits)
    return resultList
    
def calcEntropy(word, resultsList, wordBank):
    entropy = 0
    for result in resultsList:
        narrowedWB = wordBank
        for i in range(len(word)): 
            narrowedWB = narrowDown(narrowedWB, word[i], result[i], i)
            i += 1
        #narrowedWB = narrowDown(narrowedWB, word[i], result[i], i) for i in range(len(word))
        p = len(narrowedWB)/len(wordBank)
        if p != 0:
            entropy += p*math.log2(1/p)
    return entropy

def narrowedEntropy(narrowedWB):
    resultsList = allResultsRec(5)
    narrowedEntropy = [[word, calcEntropy(word, resultsList, narrowedWB)] for word in narrowedWB]
#     for word in narrowedWB:
#         print(word)
#         narrowedEntropy.append([word, calcEntropy(word, resultsList, narrowedWB)])
    narrowedEntropy.sort(reverse = True,key = lambda i: i[1])
    return narrowedEntropy
        

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
words = readFile('sgb-words.txt')
#wordleSolver(words)
#allResultsRec(5)
#print(calcEntropy("calms", allResultsRec(5), words))

#testIt()


# narrowedEntropy = narrowedEntropy(words)
# f = open("narrowedEntropy-sgb-words.txt", "w")
# for word in narrowedEntropy:
#     f.write(word)
# f.close()

    



