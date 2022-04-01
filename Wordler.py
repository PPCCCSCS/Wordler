import re
import tkinter as tk
from tkinter import ttk, messagebox
import random
 
def main():
    root = tk.Tk()
    root.title("Wordler-Wordle-Guesser")

    f = open("Wordle.csv",'r')
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
                fg="black"
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

    #TEST
    ButtonArray[0][0].config(text="F")
    
    #window = Wordler(root)
    root.mainloop()

if __name__=="__main__":
    main()
