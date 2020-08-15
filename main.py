import os
import cv2
import time
from imutils.video import VideoStream
import argparse
import numpy as np
from utils.game_brain import GameBrain
from utils.roi_class import ROI
from utils.myconstants import videostream_const_dict
from utils.frame_constants import *
from utils.videostream import *
from collections import deque
from tensorflow.keras.models import load_model

# Get commandline arguments
args = get_arguments()
# Load model
model_used = os.path.join('models', args["model"])
print("[INFO] loading model ...")
model = load_model(model_used)
print("[INFO] model loaded succesfully !")
# Start Webcam
print("[INFO] Initializing webcam...")
vs = VideoStream(src=args["webcam"]).start()
time.sleep(1)
# Frame dimensions are captured to set limits for ROI box.
# The frame is a numpy array.
frame_base = vs.read()

print(f"Frame dims are :{frame_base.shape[1]}x{frame_base.shape[0]}")

# values for ROI object

player_roi_values = get_player_roi(frame_base)
computer_roi_values = get_computer_roi(frame_base)

# background subtraction
bgModel = None
prevpred = None
isBgCaptured = 0
computer_move = 'None'

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
    frame = vs.read()
    img_to_show = computer_roi.show_computer_action(computer_move)
    frame[comp_coords[0]:comp_coords[1], comp_coords[2]:comp_coords[3]
          ] = computer_roi.show_computer_action(computer_move)

    thresh = videostream_initialize(player_roi, frame, isBgCaptured, bgModel,
                                    videostream_const_dict['learningRate'])

    if isBgCaptured == 1:
        prediction, score = predict_rgb_image_mobilenet(thresh, model)
        pred_deque.append(prediction)

        if pred_deque != prev_pred and (pred_deque.count(pred_deque[0]) == len(pred_deque)) and len(pred_deque) == args["buffer"]:
            prev_pred = pred_deque.copy()
            print(f"Prediction : {prediction}")
            computer_move = game_brain.getWinner(prediction)
            score_dict = game_brain.getCurrentScore()
            print(f"Current Score : {score_dict}")

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
        game_brain.resetScore()
    player_roi.action_control(key)
