from random import randint
import math

def readFile(txtFile):
    with open(txtFile,'r') as f:
        return f.read().splitlines()

#I presaved the initial entropy of just the first guess, because otherwise it would take 
#about 8-10 minutes to just start up the program.
#This function just reads the file and returns it as a list of lists of the word and its information gain.
def readPresavedEntropy(txtFile):
    with open(txtFile,'r') as f:
        return [[lineSplit[i] 
                 if i == 0 
                 else float(lineSplit[1][:-1]) 
                 for i 
                 in range(2) 
                 if (lineSplit := line.split(","))] 
                    for line in f.readlines()]
"""
    for line in lines:
        item = [lineSplit[i] if i == 0 else float(lineSplit[1][:-1]) for i in range(2) if (lineSplit := line.split(","))]
        #print(lineSplit)
#         item.append(lineSplit[0])
#         item.append(float(lineSplit[1][:-1]))
        items.append(item)
"""
    
#Returns list of words that may still be an answer
#It takes a list of possible answers, a letter from the alphabet, a status (indicator if it is
#in the word and right location, in the word and wrong location, or not in the word), and an 
#index of where in the word the letter is, and it returns a further narrowed down list of
#potential answers.
def narrowDown(wordBank, letter, status, index=0):
    return [word 
            for word 
            in wordBank 
            if (status == "b" and letter not in word) 
            or (status == "y" and letter in word and letter != word[int(index)]) 
            or (status == "g" and letter == word[int(index)])]
"""
    status = int(status)
    index = int(index)
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
"""

#Takes a list of possible answers, the guessed word, and the result statuses from the letters of the
#guessed word, and it uses them to return a further narrowed down list of the remaining 
#possible answers.
def narrowDownList(wordBank, guess, result):
    return [word 
            for 
            word 
            in wordBank 
            if ((result[0] == "b" and guess[0] not in word) or 
            (result[0] == "y" and guess[0] in word and guess[0] != word[0]) or 
            (result[0] == "g" and guess[0] == word[0])) and
                                          ((result[1] == "b" and guess[1] not in word) or 
            (result[1] == "y" and guess[1] in word and guess[1] != word[1]) or 
            (result[1] == "g" and guess[1] == word[1])) and
                                          ((result[2] == "b" and guess[2] not in word) or 
            (result[2] == "y" and guess[2] in word and guess[2] != word[2]) or 
            (result[2] == "g" and guess[2] == word[2])) and
                                          ((result[3] == "b" and guess[3] not in word) or 
            (result[3] == "y" and guess[3] in word and guess[3] != word[3]) or 
            (result[3] == "g" and guess[3] == word[3])) and
                                          ((result[4] == "b" and guess[4] not in word) or 
            (result[4] == "y" and guess[4] in word and guess[4] != word[4]) or 
            (result[4] == "g" and guess[4] == word[4]))]
"""
    start = time.time()
    narrowedWB = wordBank
    for i in range(len(word)): 
        narrowedWB = narrowDown(narrowedWB, word[i], result[i], i)
    end = time.time()
    print("narrowDownList: " + str(end-start))
    return narrowedWB
"""

#Goes through the letters of the answer and the guess and checks which letters match.
#It returns an answer key where: g == correct letter and correct spot, y = correct 
#letter but wrong spot, and b == wrong letter
def check(ans, guess):
    return "".join("g" if ans[i] == guess[i] 
                   else "y" if guess[i] in ans 
                   else "b" for i in range(0,5))
"""
    result = ""
    for i in range(0,5):
        if ans[i] == guess[i]:
            result += "g"
        elif guess[i] in ans:
            result += "y"
        else:
            result += "b"
    return result
"""

#Returns a list of every possible combination of the letters "b", "g", and "y"
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
    
#Helper function for the allResultsRec function.
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
        
#Recursive version of the allResults function
def allResultsRec(digits):
    resultList = []
    allResultsHelper(["b","g","y"], resultList, "", digits)
    return resultList
    
#Calculates the entropy/information gain of the word.
#Takes a word, a list of all possible results, and a list of possible answers,
#and it runs it through the entropy formula.
def calcEntropy(word, resultsList, wordBank):
    return sum((p)*math.log2(1/(p)) 
               if (p) != 0 
               else 0 
               for result 
               in resultsList 
               if (p := len(narrowDownList(wordBank, word, result))/len(wordBank)))
"""
    #entropyList = [(len(narrowDownList(wordBank, word, result))/len(wordBank))*math.log2(1/(len(narrowDownList(wordBank, word, result))/len(wordBank))) if (len(narrowDownList(wordBank, word, result))/len(wordBank)) != 0 else 0 for result in resultsList]
    entropy = 0
    for result in resultsList:
        narrowedWB = narrowDownList(wordBank, word, result)
#         for i in range(len(word)): 
#             narrowedWB = narrowDown(narrowedWB, word[i], result[i], i)
            #i += 190[
             
        #narrowedWB = [narrowDown(narrowedWB, word[i], result[i], i) for i in range(len(word))]
        p = len(narrowedWB)/len(wordBank)
        if p != 0:
            entropy += p*math.log2(1/p)
    start = time.time() 
   x = sum((len(narrowDownList(wordBank, word, result))/len(wordBank))*math.log2(1/(len(narrowDownList(wordBank, word, result))/len(wordBank))) if (len(narrowDownList(wordBank, word, result))/len(wordBank)) != 0 else 0 for result in resultsList)
 
    end = time.time()
    print("calcEntropy: " + str(end-start))
    return x
"""

#Takes a list of words and calculates the entropy/information gain of each one of the words.
#It creates a new list of lists, containing each word and its entropy. It then sorts and returns the list.
def narrowedEntropy(narrowedWB):
    resultsList = allResults()
    narrowedEntropy = [[word, calcEntropy(word, resultsList, narrowedWB)] for word in narrowedWB]
    narrowedEntropy.sort(reverse = True,key = lambda i: i[1])
    return narrowedEntropy

#Plays wordle with a CLI. Takes in a list of words to use as a dictionary
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

#Wordle solver with CLI
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



    



