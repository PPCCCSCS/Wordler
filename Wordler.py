import re
import tkinter as tk
from tkinter import ttk, messagebox
import random

STATES = ["grey","orange","green"]

def btn_clicked(btn):
    bg_next = STATES[(STATES.index(btn.cget('bg'))+1)%len(STATES)]
    btn.config(bg=bg_next)
 
def main():
    root = tk.Tk()
    root.title("Wordler-Wordle-Guesser")

    f = open("Wordle.txt",'r')
    word_list = f.read().rsplit(",")
    print(len(word_list))

    winMain = tk.Frame(root)
    winMain.grid(row=0,column=0)

    ButtonArray = []

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
                command=lambda: btn_clicked(btn)
                )
            btn.grid(row=i+1,column=j,columnspan=5,sticky="W")
            row.append(btn)
        ButtonArray.append(row)

    btnGuess = tk.Button(winMain,
                         text="NEXT GUESS",
                         width=20,
                         height=1,
                         bg="grey",
                         fg="black",
                         )
    btnGuess.grid(row=0,column=0,columnspan=5,pady=2)

    '''#TEST'''
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
