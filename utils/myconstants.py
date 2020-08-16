# defining movements and size change steps for ROI. Increase for faster movement
import os

videostream_const_dict = {'movement_steps': 5,
                          'size_change_steps': 1,
                          'bgSubThreshold': 60,
                          'learningRate': 0,
                          }

moves_dict = {('R', 'P'): 'P',
              ('R', 'S'): 'R',
              ('S', 'P'): 'S'}

user_comp = ['Computer', 'Player']

root_dir = os.getcwd()
rock_path = os.path.join(root_dir, 'imgs', 'Rock.png')
paper_path = os.path.join(root_dir, 'imgs', 'Paper.png')
scissor_path = os.path.join(root_dir, 'imgs', 'Scissor.png')
none_path = os.path.join(root_dir, 'imgs', 'None_Image.png')


gesture_names = {0: 'None',
                 1: 'P',
                 2: 'R',
                 3: 'S'}


player_box_color = (255, 0, 98)
score_color = (159, 184, 0)
move_color = (201, 0, 151)
press_z_color = (83, 36, 240)
final_winner_color = (0, 255, 0)


reset_bg_color = (66, 233, 245)
x_reset_color = (0, 0, 255)
