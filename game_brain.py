import random

moves_dict = {('R', 'P'): 'P',
              ('R', 'S'): 'R',
              ('S', 'P'): 'S'}

user_comp = ['Computer', 'Player']


class GameBrain:

    def __init__(self):
        self.__computerAction = None
        self.__computerOptions = ['R', 'P', 'S']
        self.__gameScore = {"Player": 0, "Computer": 0}
        self.__pairs = [['R', 'P'], ['R', 'S'], ['P', 'S']]
        self.__score_dict = {'Computer': 0, 'Player': 0}

    def getWinner(self, playerAction):
        self.__computerAction = self.__computerOptions[random.randint(0, 2)]
        print(
            f"Computer Action : {self.__computerAction} |||| Player Action : {playerAction}")
        print("-------------------------------------------")
        move_check = (self.__computerAction, playerAction)

        if moves_dict.get(move_check):
            self.__score_dict[user_comp[move_check.index(
                moves_dict.get(move_check))]] += 1

        elif moves_dict.get(move_check[::-1]):
            self.__score_dict[user_comp[move_check.index(
                moves_dict.get(move_check[::-1]))]] += 1

        else:
            print("Tie")

    def getResult(self, playerAction):
        self.getWinner(playerAction)
        print(self.__score_dict)


game_brain = GameBrain()
game_brain.getResult('R')
