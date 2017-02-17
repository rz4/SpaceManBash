'''
SpaceManBash.py
Last Updated: 12/17/17

'''
from GameEngine import GameEngine

class SpaceManBash():
    """
    SpaceManBash class is used to create and run instance of SpaceManBash
    game.

    """

    def __init__(self):
        '''
        Method initiates SpaceManBash game engine and configurations.

        '''
        self.game_engine = GameEngine("../data/spacemanbash_config.dat")
        self.game_engine.game_data.switch_frame("MainMenuFrame")
        self.game_engine.run()


if __name__ == '__main__':

    game = SpaceManBash()
