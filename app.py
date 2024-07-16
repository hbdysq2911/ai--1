import pygame
from source import tools,setup
from source.states import main_chat



def main():
    game = tools.Game()

    state=main_chat.Mainchat()
    game.run(state)

if __name__ == '__main__':
    main()