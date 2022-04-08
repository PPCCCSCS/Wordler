import re
import tkinter as tk
import tkinter.font as font
from tkinter import ttk, messagebox
import random

MAX_ROW = 10
STATES = ["grey","orange","green"]
c_row = 0 # Keep track of which row we're currently on
guesses = list()
bad_letters = "."
not_here = ["","","","",""]

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
    bg_next = STATES[(STATES.index(ButtonArray[i][j].cget('bg'))+1)%len(STATES)]
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
    global not_here
    if word in guesses:
        return False
    for i,r in enumerate(result):
        if r == "grey":
            if word[i] in not_here[i]:
                return False
            for j,letter in enumerate(word):
                if result[j] != 'green':
                    if word[j] in bad_letters:
                        return False
        elif r == "orange":
            if prev[i] not in not_here[i]:
                not_here[i] += prev[i]
            # If the yellow letter is not in this word; fail the test
            if prev[i] not in word:
                return False
            # If the current letter here was ever yellow here; fail test
            elif word[i] in not_here[i]:
                return False
        elif r == "green":
            if prev[i] != word[i]:
                return False
    return True

def btn_guessed(BA,lWU,dW):
    global c_row
    global guesses
    global bad_letters
    dctFiltered = dict()
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
        prev = wfr(BA,c_row - 1)
        oranges = "."
        greys   = "."
        for btn in BA[c_row-1]:
            if btn['bg'] == "grey":
                greys += btn['text']
            elif btn['bg'] == "orange":
                oranges += btn['text']
            for i in greys:
                if i not in oranges:
                    if i not in bad_letters:
                        bad_letters += i
        for word in dW:
            if check_guess_result(word,prev,result):
                dctFiltered[word] = dW[word]
        if len(dctFiltered) > 0:
            guess = max(dctFiltered,key=dW.get)
            guesses.append(guess)
            for i,ch in enumerate(guess):
                BA[c_row][i].config(text=ch)
                if BA[c_row-1][i]['bg'] == "green":
                    BA[c_row][i].config(bg="green")
    else:
        print("gameover")
    if c_row < MAX_ROW:
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
    # Create a dictionary with a weighted rarity score for each word
    for word in word_list:
        dctWeighted[word] = 0
        for char in word:
            dctWeighted[word] += dctFrequency[char]
    lstWeightedUnique = list(filter(check_unique, dctWeighted))
    dctWeightedUnique = dict()
    for item in lstWeightedUnique:
        dctWeightedUnique[item] = dctWeighted[item]
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
