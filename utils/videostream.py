from .roi_class import ROI
import numpy as np
import cv2
import utils.myconstants as myconstants


def remove_background(frame, bgModel, learningRate):
    """Removes background from Picture

    Args:
        frame (np array): frame captured in form of numpy array
        bgModel (backgroundSubtraction): Background Subtraction Model OpenCV
        learningRate (float): Learning rate of BgSubtraction Model, Use 0

    Returns:
        np array: frame with no background
    """
    fgmask = bgModel.apply(frame, learningRate=learningRate)
    kernel = np.ones((2, 2), np.uint8)
    fgmask = cv2.erode(fgmask, kernel, iterations=2)
    fgmask = cv2.dilate(fgmask, None, iterations=2)

    res = cv2.bitwise_and(frame, frame, mask=fgmask)
    return res


def videostream_initialize(player_roi, frame, isBgCaptured, bgModel, learningRate, score, moves, final_winner):
    """Starts webcam

    Args:
        roi (roi object): ROI class object
        frame (np array): captured frame from webcam
        isBgCaptured (bool): To use background capture on every frame
        bgModel (backgroundSubtraction model): Background Subtraction Model OpenCV
        learningRate (float): Learniong rate of BgSubtraction Model, Use 0

    Returns:
        np array: different types of frame based on command line argument.
    """
    frame = cv2.flip(frame, 1)
    # create vertices in form of tuples for cv2.rectangle
    A, C = player_roi.create_box()
    # display initial values of ROI box
    # values = player_roi.display_val()
    # draw the rectangle on screen
    cv2.rectangle(frame, A, C, myconstants.player_box_color, 2)
    cv2.putText(frame, score, (frame.shape[1]//4-30, 40), cv2.FONT_HERSHEY_DUPLEX,
                1, myconstants.score_color, thickness=1)

    cv2.putText(frame, moves, (frame.shape[1]//4+37, 70), cv2.FONT_HERSHEY_SIMPLEX,
                0.7, myconstants.move_color, thickness=2)

    if final_winner == 'Press Z for results':
        cv2.putText(frame, final_winner, (frame.shape[1]//4+50, 100), cv2.FONT_HERSHEY_DUPLEX,
                    0.6, myconstants.press_z_color, thickness=1)
    else:
        cv2.putText(frame, final_winner, (frame.shape[1]//4+30, 160), cv2.FONT_HERSHEY_SIMPLEX,
                    1.7, myconstants.final_winner_color, thickness=2)

    cv2.rectangle(
        frame, (frame.shape[1]-120, frame.shape[0]-15), (frame.shape[1]-12, frame.shape[0]-35), myconstants.reset_bg_color, -1)

    cv2.putText(frame, 'X --> Reset',
                (frame.shape[1]-120, frame.shape[0]-20), cv2.FONT_HERSHEY_PLAIN, 1, myconstants.x_reset_color, thickness=1)
    # draw the coordinates on screen
    # cv2.putText(frame, values, (50, 30),
    #             cv2.FONT_HERSHEY_SIMPLEX, 1, (10, 240, 50))
    # display the frame
    cv2.imshow('Camera', frame)
    # check if movement of ROI is out of bounds. If yes, bring it back to previous state.
    player_roi.check_all()
    # slice of the ROI from frame.
    roi_zone = player_roi.create_roi_zone()
    img_orig_roi = frame[roi_zone[0]:roi_zone[1], roi_zone[2]:roi_zone[3]]

    if isBgCaptured == 1:
        img = img_orig_roi
        img = remove_background(img, bgModel, learningRate)
        #cv2.imshow('orig_no_Bg', img)

        # convert to binary image
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #cv2.imshow('grayscale', gray)
        blur = cv2.GaussianBlur(gray, (11, 11), 0)

        ret, thresh = cv2.threshold(
            blur, 60, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        # cv2.imshow('mask', thresh)

        return thresh

    else:
        return None

    # cv2.waitkey(0)
    # cv2.destroyAllWindows()
