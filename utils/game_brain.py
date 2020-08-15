import random
from .myconstants import moves_dict, user_comp


class GameBrain:

    def __init__(self):
        self.__computerAction = None
        self.__computerOptions = ['R', 'P', 'S']
        self.__gameScore = {"Player": 0, "Computer": 0}
        self.__pairs = [['R', 'P'], ['R', 'S'], ['P', 'S']]
        self.__score_dict = {'Computer': 0, 'Player': 0}

    def getWinner(self, playerAction):
        if playerAction != 'None':
            self.__computerAction = self.__computerOptions[random.randint(
                0, 2)]
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

        else:
            print("Waiting for you :D")

    def getFinalResult(self):
        player_score = self.__score_dict['Player']
        computer_score = self.__score_dict['Computer']
        if player_score > computer_score:
            return f'Player Wins\n\tPlayer : {player_score}\n\tComputer : {computer_score}'

        if player_score < computer_score:
            return f'Computer Wins\n\tComputer : {computer_score}\n\tPlayer : {player_score}'

        if player_score == computer_score:
            return f'Match Tied\n\tPlayer : {player_score}\n\tComputer : {computer_score}'

    def getCurrentScore(self):
        return self.__score_dict
