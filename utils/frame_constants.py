import argparse
from .myconstants import gesture_names
import numpy as np
import cv2


def get_player_roi(frame_base):
    roi_x = frame_base.shape[1]//2
    roi_y = frame_base.shape[0]//2
    roi_h = frame_base.shape[1]//5
    roi_w = frame_base.shape[1]//5
    return [roi_x, roi_y, roi_h, roi_w]


def get_computer_roi(frame_base):
    game_roi_x = 30
    game_roi_y = frame_base.shape[0] - 30
    game_roi_h = 100
    game_roi_w = 100
    return [game_roi_x, game_roi_y, game_roi_h, game_roi_w]


def predict_rgb_image_mobilenet(thresh, model):
    """Return prediction from image

    Args:
        image (np array): the frame captured in form of array
        model (.h5 file): trained model

    Returns:
        prediction: integer prediction matched by gesture_list dictionary
    """
    image = np.stack((thresh,) * 3, axis=-1)
    image = cv2.resize(image, (224, 224))
    image = image.reshape(1, 224, 224, 3)
    image = np.array(image, dtype='float32')
    image /= 255
    pred_array = model.predict(image)
    #print(f'pred_array: {pred_array}')
    result = gesture_names[np.argmax(pred_array)]

    score = float("%0.2f" % (max(pred_array[0]) * 100))

    if score > 85.0:
        #print(f'Result: {result}  Score: {score}')
        return result, score
    else:
        return 'None', 0.0


def get_arguments():
    ap = argparse.ArgumentParser()

    ap.add_argument("-w", "--webcam", type=int, default=0, help="Webcam source, if 0 does not work try changing \
        to 1, external webcams might register on 1")

    ap.add_argument("-m", "--model", type=str, default="mobilenetv2_ver_1.0.h5", help="Name of model in str to be used. Model should be placed inside \
        models dir. Default : \"model1\"")

    ap.add_argument("-b", "--buffer", type=int, default=2,
                    help="Buffer size for deque. Use to change sensitivity. Default:2")

    args = vars(ap.parse_args())

    return args
