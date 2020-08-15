#!/usr/bin/env python3
import os
import cv2
from .myconstants import rock_path, paper_path, scissor_path, none_path


class ROI:
    """
    Class for implementing actions on Region of Interest
    """
#  roi_values = [roi_x, roi_y, roi_h, roi_w]

    def __init__(self, roi_values, frame_base, movement_steps, size_change_steps, isMovable):
        self.x, self.y, self.h, self.w = roi_values[0], roi_values[1], roi_values[2], roi_values[3]
        self.frame_y, self.frame_x = frame_base.shape[:2]
        self.steps = movement_steps
        self.size_steps = size_change_steps
        self.action_imgs = {'R': rock_path,
                            'P': paper_path,
                            'S': scissor_path,
                            'None': none_path}
        self.isMovable = isMovable

    def display_val(self):
        """Display ROI bottom right (x,y) and dimenstions

        Returns:
            self: f-string with bottom right (x,y) and height and width
        """
        return f"x : {self.x}, y : {self.y}, h : {self.h}, w : {self.w}"

    # The following four functions are for movements
    def moveup(self):
        self.y -= self.steps

    def movedown(self):
        self.y += self.steps

    def moveleft(self):
        self.x -= self.steps

    def moveright(self):
        self.x += self.steps

    # Return Coords for Rectangle
    def create_box(self):
        A = (self.x, self.y)
        C = (self.x - self.w, self.y - self.h)
        return A, C

    def check_all(self):
        """
        Checks and corrects ROI so it is not out of bounds.
        """

        if self.y < 50:
            self.y = 50

        if self.y > self.frame_y:
            self.y = self.frame_y

        if self.x < 50:
            self.x = 50

        if self.x > self.frame_x:
            self.x = self.frame_x

        if self.w > self.frame_x:
            self.w = self.frame_x

        if self.h > self.frame_y:
            self.h = self.frame_y

        if self.w < 50:
            self.w = 50

        if self.h < 50:
            self.h = 50

        if self.x - self.w < 0:
            self.x = self.w

        if self.y - self.h < 0:
            self.y = self.h

    # Increase size of ROI
    def increase_size(self):
        self.h += self.size_steps
        self.w += self.size_steps
    # Decrease size of ROI

    def decrease_size(self):
        self.h -= self.size_steps
        self.w -= self.size_steps

    # Restore Shape of ROI in case of errors.
    def restore_shape(self):
        self.h = 224
        self.w = 224
        self.x = 100
        self.y = 100

    # Returns ROI top left and bottom right coords in a list
    # For slicing from frame
    def create_roi_zone(self):
        # format [y1,y2,x1,x2]
        y1 = self.y - self.h
        y2 = self.y
        x1 = self.x - self.w
        x2 = self.x
        return [y1, y2, x1, x2]

    # Keyboard contol for ROI
    def action_control(self, key):
        if self.isMovable == True:
            if key == ord('w') or key == ord('W'):
                self.moveup()
            elif key == ord('s') or key == ord('S'):
                self.movedown()
            elif key == ord('a') or key == ord('A'):
                self.moveleft()
            elif key == ord('d') or key == ord('D'):
                self.moveright()
            elif key == ord('i') or key == ord('I'):
                self.increase_size()
            elif key == ord('k') or key == ord('K'):
                self.decrease_size()
            elif key == ord('r') or key == ord('R'):
                self.restore_shape()
            else:
                pass
        else:
            pass

    def show_computer_action(self, action):
        img_to_show = self.action_imgs.get(action)
        return cv2.imread(img_to_show)
