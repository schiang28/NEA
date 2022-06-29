from abc import ABC, abstractmethod
from calendar import c
from types import CellType
from Game import Game
from Colors import color
from tkinter import *


class Ui(ABC):
    @abstractmethod
    def run(self):
        raise NotImplementedError


class Gui(Ui):
    # TODO: create futoshiki grid
    MARGIN = 50
    SIDE = 100

    def __init__(self):
        self.__game_win = None
        root = Tk()
        root.title("Futoshiki")
        root.geometry("500x500")
        frame = Frame(root)
        frame.pack()

        Button(frame, text="Play", command=self.__play_game, height=2, width=30).pack(
            fill=X
        )
        Button(frame, text="Quit", command=self.__quit, height=2).pack(fill=X)

        self.__root = root

    def __play_game(self):
        if self.__game_win:
            return

        WIDTH = HEIGHT = Gui.MARGIN * 2 + Gui.SIDE * 7
        self.__game = Game()
        game_win = Toplevel(self.__root)
        game_win.title("Puzzle")
        game_win.geometry("800x600")

        self.__canvas = Canvas(game_win, width=WIDTH, height=HEIGHT)
        self.__canvas.pack(fill=BOTH, side=TOP)

        clear_button = Button(game_win, text="Clear answers")
        clear_button.pack(fill=BOTH, side=BOTTOM)

        self.__draw_grid()
        self.__draw_puzzle()

        self.__canvas.bind("<Button-1>", self.__cell_clicked)
        self.__canvas.bind("<Key>", self.__key_pressed)

    def __draw_grid(self):
        for row in range(self.__game.GRID_SIZE):
            for l in range(self.__game.GRID_SIZE * 2):
                # vertical lines
                x0 = Gui.MARGIN + l * Gui.SIDE
                y0 = Gui.MARGIN * (row + 1) + Gui.SIDE * row
                x1 = Gui.MARGIN + l * Gui.SIDE
                y1 = Gui.MARGIN * (row + 1) + Gui.SIDE * row + Gui.SIDE
                self.__canvas.create_line(x0, y0, x1, y1)

            for l in range(self.__game.GRID_SIZE):
                # horizontal lines
                x0 = Gui.MARGIN + l * 2 * Gui.SIDE
                y0 = Gui.MARGIN * (row + 1) + Gui.SIDE * row
                x1 = Gui.MARGIN + l * 2 * Gui.SIDE + Gui.SIDE
                y1 = Gui.MARGIN * (row + 1) + Gui.SIDE * row
                self.__canvas.create_line(x0, y0, x1, y1)
                self.__canvas.create_line(x0, y0 + Gui.SIDE, x1, y1 + Gui.SIDE)

    def __cell_clicked(self):
        pass

    def __key_pressed(self):
        pass

    def __draw_puzzle(self):
        pass

    def __quit(self):
        self.__root.quit()

    def run(self):
        self.__root.mainloop()


class Terminal(Ui):
    def __init__(self):
        self.__game = Game()

    def __get_input(self):
        while True:
            try:
                row = int(input("Enter row: "))
                column = int(input("Enter column: "))
                if 1 <= row <= Game.GRID_SIZE and 1 <= column <= Game.GRID_SIZE:
                    break
                else:
                    print("Invalid input. Please try again")
            except ValueError():
                print("invalid input")

        while True:
            choice = input("Enter number to play or x to clear: ")
            if choice == "x":
                break
            try:
                if 1 <= int(choice) <= Game.GRID_SIZE:
                    break
                else:
                    print("Invalid input. Please try again")
            except:
                print("invalid input")

        return row, column, choice

    def run(self):
        while not self.__game.check():
            print(self.__game)
            row, col, choice = self.__get_input()
            if self.__game.is_valid(row, col, choice):
                self.__game.play(row, col, choice)
        print(self.__game)
        print("puzzle correct!")
