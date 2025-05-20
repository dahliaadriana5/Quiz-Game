import tkinter as tk
from tkinter import ttk
from quiz import QuizGame

def main():
    root = ttk.Window(themename="litera")  # Folosește ttk.Window pentru consistență
    app = QuizGame(root)
    root.mainloop()  # Înlocuiește while True cu mainloop

if __name__ == "__main__":
    main()
