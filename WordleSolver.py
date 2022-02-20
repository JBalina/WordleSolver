from random import randint
import math

def readFile(txtFile):
    with open(txtFile,'r') as f:
        return f.read().splitlines()

def readPresavedEntropy(txtFile):
    with open(txtFile,'r') as f:
        return [[lineSplit[i] if i == 0 else float(lineSplit[1][:-1]) for i in range(2) if (lineSplit := line.split(","))] for line in f.readlines()]
#     for line in lines:
#         item = [lineSplit[i] if i == 0 else float(lineSplit[1][:-1]) for i in range(2) if (lineSplit := line.split(","))]
#         #print(lineSplit)
# #         item.append(lineSplit[0])
# #         item.append(float(lineSplit[1][:-1]))
#         items.append(item)
    
def narrowDown(wordBank, letter, status, index=0):
    return [word for word in wordBank if (status == "b" and letter not in word) or (status == "y" and letter in word and letter != word[int(index)]) or (status == "g" and letter == word[int(index)])]
#     status = int(status)
#     index = int(index)
#     for word in wordBank:
#         #if not in word
#         if status == "b":
#             if letter not in word:
#                     newWordBank.append(word)
#         else:
#             #if in word but wrong placement
#             if status == "y":
#                 if letter in word and letter != word[int(index)]:
#                     newWordBank.append(word)
#             #check if matches placement
#             elif letter == word[int(index)]:
#                 newWordBank.append(word)
#     return newWordBank

def narrowDownList(wordBank, guess, result):
    return [word for word in wordBank if ((result[0] == "b" and guess[0] not in word) or 
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
#     start = time.time()
#     narrowedWB = wordBank
#     for i in range(len(word)): 
#         narrowedWB = narrowDown(narrowedWB, word[i], result[i], i)
#     end = time.time()
#     print("narrowDownList: " + str(end-start))
#     return narrowedWB

def check(ans, guess):
#     result = ""
#     for i in range(0,5):
#         if ans[i] == guess[i]:
#             result += "g"
#         elif guess[i] in ans:
#             result += "y"
#         else:
#             result += "b"
#     return result
    return "".join("g" if ans[i] == guess[i] else "y" if guess[i] in ans else "b" for i in range(0,5))

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
    #entropyList = [(len(narrowDownList(wordBank, word, result))/len(wordBank))*math.log2(1/(len(narrowDownList(wordBank, word, result))/len(wordBank))) if (len(narrowDownList(wordBank, word, result))/len(wordBank)) != 0 else 0 for result in resultsList]
#     entropy = 0
#     for result in resultsList:
#         narrowedWB = narrowDownList(wordBank, word, result)
# #         for i in range(len(word)): 
# #             narrowedWB = narrowDown(narrowedWB, word[i], result[i], i)
#             #i += 190[
#             
#         #narrowedWB = [narrowDown(narrowedWB, word[i], result[i], i) for i in range(len(word))]
#         p = len(narrowedWB)/len(wordBank)
#         if p != 0:
#             entropy += p*math.log2(1/p)
#     start = time.time() 
#    x = sum((len(narrowDownList(wordBank, word, result))/len(wordBank))*math.log2(1/(len(narrowDownList(wordBank, word, result))/len(wordBank))) if (len(narrowDownList(wordBank, word, result))/len(wordBank)) != 0 else 0 for result in resultsList)
    return sum((p)*math.log2(1/(p)) if (p) != 0 else 0 for result in resultsList if (p := len(narrowDownList(wordBank, word, result))/len(wordBank)))
# 
#     end = time.time()
#     print("calcEntropy: " + str(end-start))
#     return x

def narrowedEntropy(narrowedWB):
    resultsList = allResultsRec(5)
    narrowedEntropy = [[word, calcEntropy(word, resultsList, narrowedWB)] for word in narrowedWB]
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



    



