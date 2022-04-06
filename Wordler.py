import re
import tkinter as tk
import tkinter.font as font
from tkinter import ttk, messagebox
import random

MAX_ROW = 15
STATES = ["grey","orange","green"]
GO_STS = ["black","orange","green"]
c_row = 0 # Keep track of which row we're currently on
guesses = list()
bad_letters = "."


def check_char_in_pos(word,char,pos):
    if word[pos] == char:
        return True
    else:
        return False

def check_char_in_word(word,char):
    if char in word:
        return True
    else:
        return False

def check_char_not_pos(word,char,pos):
    if check_char_in_word(word,char) and not check_char_in_pos(word,char,pos):
        return True
    else:
        return False

def check_unique(word):
    test = set()
    for char in word:
        test.add(char)
    if len(test) == len(word):
        return True
    else:
        return False        

def btn_clicked(i,j,ButtonArray):
    if i < 6:
        bg_next = STATES[(STATES.index(ButtonArray[i][j].cget('bg'))+1)%len(STATES)]
    else:
        bg_next = GO_STS[(GO_STS.index(ButtonArray[i][j].cget('bg'))+1)%len(GO_STS)]
    ButtonArray[i][j].config(bg=bg_next)

def wfr(BA,row):

    return BA[row][0]['text']+\
           BA[row][1]['text']+\
           BA[row][2]['text']+\
           BA[row][3]['text']+\
           BA[row][4]['text']

# For filtering a SINGLE word in dictionary
# Use with FILTER to build matching dictionary
def check_guess_result(word,prev,result):

    global guesses
    global bad_letters

    if word in guesses:
        #print("Duplicate")
        return False

    '''
    for letter in bad_letters:
        if letter in bad_letters:
            return False
    '''

    #print(bad_letters)
    
    for i,r in enumerate(result):
        if r == "grey":
            if prev[i] not in bad_letters:
                bad_letters += prev[i]
                print("bad letter:",prev[i])

            for j,letter in enumerate(word):
                if result[j] != 'green':
                    if word[j] in bad_letters:
                    #print(c_row,"grey:",prev[i],"from",prev,"in",word)
                        return False
        elif r == "orange":
            if prev[i] not in word:
                #print(c_row,"orange:",prev[i],"from",prev,"not in",word)
                return False
            elif prev[i] == word[i]:
                #print(c_row,"orange:",prev[i],"in",prev,"@ pos",i,"in",word)
                return False
        elif r == "green":
            if prev[i] != word[i]:
                #print(c_row,"green",prev[i],"from",prev,"not @ pos",i,"in",word)
                return False

    return True

def btn_guessed(BA,lWU,dW):
    global c_row
    global guesses
    global bad_letters
    dctFiltered = dict()

    print("lWU:",len(lWU),"dW",len(dW),"greys:",bad_letters)
    
    # Pick the max(dctWeightedUnique,key=dctWeighted.get)
    if c_row == 0:
        guess = max(lWU,key=dW.get)
        for i,ch in enumerate(guess):
            BA[0][i].config(text=ch)
    # Read the color of the letters for previous guess, filter accordingly
    elif c_row < MAX_ROW:

        result = [BA[c_row-1][0]['bg'],
                  BA[c_row-1][1]['bg'],
                  BA[c_row-1][2]['bg'],
                  BA[c_row-1][3]['bg'],
                  BA[c_row-1][4]['bg']]

        print(result)

        prev = wfr(BA,c_row - 1)
        print("prev was:", prev)
        for word in dW:

            #print("previous word was:", prev)
            if check_guess_result(word,prev,result):
                dctFiltered[word] = dW[word]
                #print(word)

        print(len(dctFiltered))
        guess = max(dctFiltered,key=dW.get)
        guesses.append(guess)
        for i,ch in enumerate(guess):
            BA[c_row][i].config(text=ch)
            if BA[c_row-1][i]['bg'] == "green":
                BA[c_row][i].config(bg="green")
        
    else:
        print("gameover")

    if c_row < MAX_ROW:
        print("Guess",c_row,"=",
              BA[c_row][0]['text']+\
              BA[c_row][1]['text']+\
              BA[c_row][2]['text']+\
              BA[c_row][3]['text']+\
              BA[c_row][4]['text'])
        c_row+=1
 
def main():
    root = tk.Tk()
    root.title("Wordler-Wordle-Guesser")
    tkFont = font.Font(size=24)

    f = open("Wordle.txt",'r')
    word_list = f.read().upper().strip().rsplit(",")

    dctFrequency = dict()
    lstFrequency = ""
    dctWeighted = dict()
    
    
    # Count the occurrences of each letter in the Wordle Word List
    for word in word_list:
        for char in word:
            if char in dctFrequency:
                dctFrequency[char] += 1
            else:
                dctFrequency[char] = 1

    # Create a list of letters sorted most common to least
    for ltr in sorted(dctFrequency,key=dctFrequency.get,reverse=True):
        lstFrequency += ltr

    #print(lstFrequency)

    # Create a dictionary with a weighted rarity score for each word
    for word in word_list:
        dctWeighted[word] = 0
        for char in word:
            dctWeighted[word] += dctFrequency[char]

    lstWeightedUnique = list(filter(check_unique, dctWeighted))

    dctWeightedUnique = dict()

    for item in lstWeightedUnique:
        dctWeightedUnique[item] = dctWeighted[item]

    '''#TEST'' '
    print(dctWeightedUnique)
    print(max(dctWeightedUnique,key=dctWeighted.get))
    print(min(dctWeightedUnique,key=dctWeighted.get))
    '''#TEST'''

    # Build the game window
    winMain = tk.Frame(root)
    winMain.grid(row=0,column=0)

    # Each button will correspond to a single letter
    ButtonArray = []

    # Build the Letter Button Array, Clickable for Context
    for i in range(MAX_ROW):
        row = []
        for j in range(5):
            btn = tk.Button(
                winMain,
                text=" ",
                width=3,
                height=1,
                bg="grey",
                fg="white",
                font=tkFont,
                command=lambda i=i,j=j,ButtonArray=ButtonArray: \
                btn_clicked(i,j,ButtonArray)
                )
            if i > 5:
                btn['bg'] = "black"
            btn.grid(row=i+1,column=j,columnspan=5,sticky="W")
            row.append(btn)
        ButtonArray.append(row)

    # create the guess button here
    btnGuess = tk.Button(winMain,
                         text="GUESS WORD",
                         width=15,
                         height=1,
                         bg="grey",
                         fg="white",
                         font=tkFont,
                         command=lambda c_row=c_row,
                         ButtonArray=ButtonArray,
                         dctWeightedUnique=dctWeightedUnique,
                         dctWeighted=dctWeighted: btn_guessed(ButtonArray,
                                                              dctWeightedUnique,
                                                              dctWeighted)
                         )
    # place the guess button at the top of the game window
    btnGuess.grid(row=0,column=0,columnspan=5,pady=2)
  
    #window = Wordler(root)
    root.mainloop()

if __name__=="__main__":
    main()
