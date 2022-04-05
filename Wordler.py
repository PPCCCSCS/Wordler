import re
import tkinter as tk
import tkinter.font as font
from tkinter import ttk, messagebox
import random

STATES = ["grey","orange","green"]
c_row = 0 # Keep track of which row we're currently on

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

def check_guess_result(word,prev,result):
    rval = False
    for r in result:
        if r == "grey":
            pass
        elif r == "orange":
            pass
        elif r == "green":
            pass
        else:
            pass

def first_guess():
    pass
    return "farts"

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

def btn_guessed(BA,dWU,dW):
    global c_row

    # Pick the max(dctWeightedUnique,key=dctWeighted.get)
    if c_row == 0:
        guess = max(dWU,key=dW.get)
        for i,ch in enumerate(guess):
            BA[0][i].config(text=ch)
    # Read the color of the letters for previous guess, filter accordingly
    elif c_row < 6:
        BA[c_row][0].config(text="W")
        BA[c_row][1].config(text="O")
        BA[c_row][2].config(text="R")
        BA[c_row][3].config(text="D")
        BA[c_row][4].config(text="S")
    else:
        print("gameover")

    if c_row < 6:
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

    dctWeightedUnique = list(filter(check_unique, dctWeighted))

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
    for i in range(6):
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

    '''#TEST
    ButtonArray[0][0].config(text="S",bg="green")
    ButtonArray[0][1].config(text="T",bg="orange")
    ButtonArray[0][2].config(text="A",bg="grey")
    ButtonArray[0][3].config(text="I",bg="grey")
    ButtonArray[0][4].config(text="R",bg="grey")

    ButtonArray[1][0].config(text="C",bg="grey")
    ButtonArray[1][1].config(text="L",bg="grey")
    ButtonArray[1][2].config(text="O",bg="green")
    ButtonArray[1][3].config(text="N",bg="orange")
    ButtonArray[1][4].config(text="E",bg="grey")

    ButtonArray[2][0].config(text="S",bg="green")
    ButtonArray[2][1].config(text="N",bg="green")
    ButtonArray[2][2].config(text="O",bg="green")
    ButtonArray[2][3].config(text="T",bg="orange")
    ButtonArray[2][4].config(text="S",bg="grey")

    ButtonArray[3][0].config(text="S",bg="green")
    ButtonArray[3][1].config(text="N",bg="green")
    ButtonArray[3][2].config(text="O",bg="green")
    ButtonArray[3][3].config(text="U",bg="green")
    ButtonArray[3][4].config(text="T",bg="green")
    '''#TEST'''
    
    #window = Wordler(root)
    root.mainloop()

if __name__=="__main__":
    main()
