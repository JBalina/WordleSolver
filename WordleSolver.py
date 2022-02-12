from random import randint

def readFile(txtFile):
    items = []
    with open(txtFile,'r') as f:
        items = f.read().splitlines()
    return items

def narrowDown(wordBank, letter):
    newWordBank = []
    for word in wordBank:
        if int(letter[1]) == 6:
            if letter[0] not in word:
                    newWordBank.append(word)
        else:
            if int(letter[1]) == 5:
                if letter[0] in word and letter[0] != word[int(letter[2])]:
                    newWordBank.append(word)
            elif letter[0] == word[int(letter[1])]:
                newWordBank.append(word)
    return newWordBank

def wordle(words):
    ans = words[randint(0,len(words)-1)]
    tries = 0
    uInput = ""
    result = ""
    while uInput != ans and tries != 5:
        uInput = input()
        if len(uInput) != 5:
            print("Guess must be 5 letters long.")
        elif uInput not in words:
            print("Guess does not exist in dictionary.")
        else:
            for i in range(0,5):
                if ans[i] == uInput[i]:
                    result += "g"
                elif uInput[i] in ans:
                    result += "y"
                else:
                    result += "b"
            print(result)
            
            tries += 1
        if result == "ggggg":
            print("Your win!")
        elif tries == 5:
            print("Game over! The answer was " + ans)
        
        result = ""

def wordleSolver(words):
    items = words
    uInput = ""
    while uInput != "Quit":
        uInput = input()
        if uInput != "Quit":
            items = narrowDown(items, uInput.split(" "))
            print(items)



#words = readFile('wordle-answers-alphabetical.txt')
words = readFile('sgb-words.txt')
wordle(words)




