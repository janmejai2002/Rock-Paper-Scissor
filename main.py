import os
import cv2
import time
from imutils.video import VideoStream
import argparse
import numpy as np
from utils.game_brain import GameBrain
from utils.roi_class import ROI
from utils.myconstants import videostream_const_dict
from utils.helper_functions import *
from utils.videostream import *
from collections import deque
from tensorflow.keras.models import load_model

# Get commandline arguments
args = get_arguments()
# Load model
model_used = os.path.join('models', args["model"])
print("[INFO] loading model ...")
model = load_model(model_used)
print("[INFO] Model loaded succesfully !")
# Start Webcam
print("[INFO] Initializing webcam...")
vs = VideoStream(src=args["webcam"]).start()
time.sleep(1)
# Frame dimensions are captured to set limits for ROI box.
# The frame is a numpy array.
frame_base = vs.read()

print(f"[INFO] Frame dims are : {frame_base.shape[1]}x{frame_base.shape[0]}")

# values for ROI object

player_roi_values = get_player_roi(frame_base)
computer_roi_values = get_computer_roi(frame_base)

# background subtraction
bgModel = None
prevpred = None
isBgCaptured = 0
computer_move = 'None'
set_prediction = 'None'
final_winner = 'Press Z for results'
thresh = None

# for prediction sensitivity
pred_deque = deque(maxlen=args["buffer"])
prev_pred = deque(maxlen=args["buffer"])

# using roi class to initiailze a box
player_roi = ROI(player_roi_values, frame_base,
                 videostream_const_dict['movement_steps'], videostream_const_dict['size_change_steps'], isMovable=True)

computer_roi = ROI(computer_roi_values, frame_base,
                   videostream_const_dict['movement_steps'], videostream_const_dict['size_change_steps'], isMovable=False)

comp_coords = computer_roi.create_roi_zone()
# game_brain
game_brain = GameBrain()

while True:
    moves = f"P : {set_prediction} | C : {computer_move}"
    frame = vs.read()
    # img_to_show = computer_roi.show_computer_action(computer_move)
    if isinstance(thresh, np.ndarray):
        thresh = stack_to_three_and_reverse(thresh)
        frame[0:128, frame_base.shape[1]-128:frame_base.shape[1]] = thresh
    else:
        frame[0:128, frame_base.shape[1]-128:frame_base.shape[1]] = cv2.flip(cv2.imread(
            os.path.join('imgs', 'Before_BG_sub.png')), 1)

    frame[comp_coords[0]:comp_coords[1], comp_coords[2]:comp_coords[3]
          ] = computer_roi.show_computer_action(computer_move)
    thresh = videostream_initialize(player_roi, frame, isBgCaptured, bgModel,
                                    videostream_const_dict['learningRate'], game_brain.getCurrentScore(), moves, final_winner)
    # if isinstance(thresh, np.ndarray):
    #     thresh_show = cv2.flip(cv2.resize(
    #         thresh, (128, 128)), 1)

    if isBgCaptured == 1:
        prediction, score = predict_rgb_image_mobilenet(thresh, model)
        pred_deque.append(prediction)

        if pred_deque != prev_pred and (pred_deque.count(pred_deque[0]) == len(pred_deque)) and len(pred_deque) == args["buffer"]:
            prev_pred = pred_deque.copy()
            # print(f"Prediction : {prediction}")

            # Align the '|' in moves with upper
            # The closest I could do it.
            if prediction != 'None':
                set_prediction = f"  {prediction}  "
            else:
                set_prediction = prediction
            # get computer move after player move has been predicted.
            computer_move = game_brain.getWinner(prediction)
            score_dict = game_brain.getCurrentScore()
            # print(f"Current Score : {score_dict}")

    key = cv2.waitKey(10) & 0xFF

    if key == ord('q'):
        break
    if key == ord('b'):
        bgModel = cv2.createBackgroundSubtractorMOG2(
            0, videostream_const_dict['bgSubThreshold'])
        time.sleep(1)
        isBgCaptured = 1
        print('[INFO] Background Captured. Model with start making predictions')

    if key == ord('x'):
        final_winner = game_brain.resetResult()
        game_brain.resetScore()
        print(final_winner)

    if key == ord('z') or key == ord('Z'):
        final_winner = game_brain.getFinalResult()

    player_roi.action_control(key)
