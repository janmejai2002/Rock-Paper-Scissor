import random
from .myconstants import moves_dict, user_comp


class GameBrain:

    def __init__(self):
        self.__computerAction = None
        self.__computerOptions = ['R', 'P', 'S']
        self.__gameScore = {"Player": 0, "Computer": 0}
        self.__pairs = [['R', 'P'], ['R', 'S'], ['P', 'S']]
        self.__score_dict = {'Computer': 0, 'Player': 0}
        self.result = 'Press Z for results'

    def getWinner(self, playerAction):
        if playerAction != 'None':
            self.__computerAction = self.__computerOptions[random.randint(
                0, 2)]

            # print(
            #     f"Computer Action : {self.__computerAction} |||| Player Action : {playerAction}")
            # print("-------------------------------------------")
            move_check = (self.__computerAction, playerAction)

            if moves_dict.get(move_check):
                self.__score_dict[user_comp[move_check.index(
                    moves_dict.get(move_check))]] += 1

            elif moves_dict.get(move_check[::-1]):
                self.__score_dict[user_comp[move_check.index(
                    moves_dict.get(move_check[::-1]))]] += 1

            else:
                # print('Tie')
                pass

            return self.__computerAction

        else:
            # print("Waiting for player move")
            return 'None'

    def getFinalResult(self):
        player_score = self.__score_dict['Player']
        computer_score = self.__score_dict['Computer']
        if player_score > computer_score:
            self.result = 'Player Wins'

        elif player_score < computer_score:
            self.result = 'Computer Wins'

        elif player_score == computer_score:
            self.result = "It's a tie"
        return self.result

    def getCurrentScore(self):
        return f"Player : {self.__score_dict['Player']} | Computer : {self.__score_dict['Computer']}"

    def resetScore(self):
        self.__score_dict = {'Computer': 0, 'Player': 0}

    def resetResult(self):
        self.result = 'Press Z for results'
        return self.result
