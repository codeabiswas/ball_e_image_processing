"""
focal_length_finder.py
---
This file contains the VideoView, TrainingGoalCalibrationScreen, and FocalLengthFinder classes. This helps find out what the focal length of the lens is of the camera being used for the project.
---

Author: Andrei Biswas (@codeabiswas)
Date: May 4, 2021
Last Modified: May 08, 2021
"""

import math
import sys
from pathlib import Path

import cv2
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QBrush, QPainter, QPen, QPixmap
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QLabel, QMainWindow,
                             QPushButton, QSizePolicy, QVBoxLayout, QWidget)

import style_constants as sc
from component_button import GenericButton
from component_labels import ProfileLabel
from component_toolbar import ToolbarComponent
from window_test import TestWindow


class VideoView():
    """VideoView.

    This class gets the video stream from from the camera using OpenCV.
    """

    def __init__(self):
        """__init__.

        Initializes OpenCV appropriately
        """
        super().__init__()

    def run(self):
        """run.

        Captures the video stream
        """
        # capture from web cam
        cap = cv2.VideoCapture(self.gstreamer_pipeline(), cv2.CAP_GSTREAMER)
        while True:
            ret, cv_img = cap.read()
            cv2.imshow(cv_img)

            # When user presses 'q', save the image
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.imwrite('images/curr_img.png', cv_img)
                break

        # shut down capture system
        cap.release()
        # Close all frames
        cv2.destroyAllWindows()

    def gstreamer_pipeline(
        self,
        capture_width=1920,
        capture_height=1080,
        display_width=960,
        display_height=540,
        framerate=30,
        flip_method=0,
    ):
        """gstreamer_pipeline.

        Uses gstreamer to talk to camera module

        :param capture_width: Width (in pixels) to capture feed
        :param capture_height: Height (in pixels) to capture feed
        :param display_width: Width (in pixels) to display feed
        :param display_height: Height (in pixels) to display feed
        :param framerate: Framerate (in fps) to display feed
        :param flip_method: Argument for rotation of image capturing and displaying
        """

        return (
            "nvarguscamerasrc ! "
            "video/x-raw(memory:NVMM), "
            "width=(int)%d, height=(int)%d, "
            "format=(string)NV12, framerate=(fraction)%d/1 ! "
            "nvvidconv flip-method=%d ! "
            "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
            "videoconvert ! "
            "video/x-raw, format=(string)BGR ! appsink"
            % (
                capture_width,
                capture_height,
                framerate,
                flip_method,
                display_width,
                display_height,
            )
        )


class TrainingGoalCalibrationScreen(QWidget):
    """TrainingGoalCalibrationScreen.

    Screen for calibrating Ball-E with the goal
    """

    def __init__(self, parent=None):
        """__init__.

        Initializes the Widget object with appropriate arguments

        :param parent: Default arg.
        """

        super().__init__(parent=parent)

        # Set a title for the widget
        self.window_title = "Goal Calibration"

        # Tracks how many times the user has clicked on the image
        self.click_counter = 0

        screen_layout = QVBoxLayout()

        self.toolbar = ToolbarComponent(
            self.window_title, "Back to Goal Calib. \nSetup")

        screen_layout.addWidget(self.toolbar)

        self.info_label = ProfileLabel(
            "Please select the 4 corners of the goal, going clockwise from the top-left corner")
        screen_layout.addWidget(self.info_label)

        self.lax_goal_label = QLabel()
        screen_layout.addWidget(self.lax_goal_label)
        # NOTE: This will change to temp_training_lax_goal.png
        self.lax_goal_img_location = str(
            Path.home()) + '/Developer/ball_e_image_processing/src/focal_length_finder/images/curr_img.png'

        self.pixmap_object = QPixmap()
        self.pixmap_object.load(self.lax_goal_img_location)
        self.lax_goal_label.mousePressEvent = self.draw_user_input
        self.lax_goal_label.setPixmap(self.pixmap_object)

        self.button_layout = QHBoxLayout()
        self.reset_button = GenericButton("Reset")
        self.reset_button.clicked.connect(self.reset_lines)
        self.reset_button.setVisible(False)
        self.next_page_button = GenericButton("Next")
        self.next_page_button.setVisible(False)

        self.button_layout.addWidget(self.reset_button)
        self.button_layout.addWidget(self.next_page_button)

        screen_layout.addLayout(self.button_layout)

        # These store the coordinates ((x,y) tuples format) of where the user clicked on the image
        self.top_left_coord = None
        self.top_right_coord = None
        self.bottom_right_coord = None
        self.bottom_left_coord = None

        # Stores the abobe coordinates in this list
        self.selected_points = []

        self.setLayout(screen_layout)

    def update_lax_goal_pic(self):
        """update_lax_goal_pic.

        Updates the label with the latest image of the goal.
        """
        self.pixmap_object = QPixmap()
        self.pixmap_object.load(self.lax_goal_img_location)
        self.lax_goal_label.mousePressEvent = self.draw_user_input
        self.lax_goal_label.setPixmap(self.pixmap_object)

    def reset_lines(self):
        """reset_lines.

        Resets all the lines on the image that the user drew on and 'refreshes' the page on the image 
        such that the calibration process be redone
        """
        # Reset click counter
        self.click_counter = 0

        # Clear the image
        # NOTE: This will change to temp_training_lax_goal.png
        self.lax_goal_img_location = str(
            Path.home()) + '/Developer/ball_e_image_processing/src/focal_length_finder/images/curr_img.png'

        self.pixmap_object = QPixmap()
        self.pixmap_object.load(self.lax_goal_img_location)
        self.lax_goal_label.mousePressEvent = self.draw_user_input
        self.lax_goal_label.setPixmap(self.pixmap_object)

        self.reset_button.setVisible(False)
        self.next_page_button.setVisible(False)

        self.info_label.setText(
            "Please select the 4 corners of the goal, going clockwise from the top-left corner")

    def draw_user_input(self, event):
        """draw_user_input.

        Function that is called when the user clicks on the image

        :param event: Mouse click event
        """

        # Store the coordinates
        x_coord = event.pos().x()
        y_coord = event.pos().y()

        # While the user is still drawing the points around the goal
        if self.click_counter < 4:
            self.click_counter += 1

            # Set the painter object so that points can be visually seen on the image as the user clicks on them
            painter_obj = QPainter(self.pixmap_object)
            painter_obj.setPen(QPen(Qt.green, 12, Qt.SolidLine))
            painter_obj.setBrush(QBrush(Qt.green, Qt.SolidPattern))

            painter_obj.drawEllipse(event.pos(), 20, 20)

            painter_obj.end()

            # Update the image with the newly drawn point
            self.lax_goal_label.setPixmap(self.pixmap_object)

            # We assume that the user is going in a clockwise direction, starting with the top-left coordinate
            if self.click_counter == 1:
                self.top_left_coord = (x_coord, y_coord)
                self.selected_points.append(self.top_left_coord)

            elif self.click_counter == 2:
                self.top_right_coord = (x_coord, y_coord)
                self.selected_points.append(self.top_right_coord)

            elif self.click_counter == 3:
                self.bottom_right_coord = (x_coord, y_coord)
                self.selected_points.append(self.bottom_right_coord)

            # For the last drawn point
            elif self.click_counter == 4:
                self.bottom_left_coord = (x_coord, y_coord)
                self.selected_points.append(self.bottom_left_coord)
                # Make appropriate buttons visible, draw the lines given the coordinates to show the bounds,
                # and update the text to guide the user
                self.reset_button.setVisible(True)
                self.next_page_button.setVisible(True)
                self.draw_lines()
                self.info_label.setText(
                    "These will be your bounds. If you would like to redo this, click on the Reset button")

    def draw_lines(self):
        """draw_lines.

        This function draws the boundaries of the goal given the 4 coordinates drawn by the user
        """

        # Set the painter object so that the lines can be seen
        painter_obj = QPainter(self.pixmap_object)
        painter_obj.setPen(QPen(Qt.green, 12, Qt.SolidLine))

        # Draw the perimeter
        painter_obj.drawLine(
            self.top_left_coord[0], self.top_left_coord[1], self.top_right_coord[0], self.top_right_coord[1])

        painter_obj.drawLine(
            self.top_left_coord[0], self.top_left_coord[1], self.bottom_left_coord[0], self.bottom_left_coord[1])

        painter_obj.drawLine(
            self.top_right_coord[0], self.top_right_coord[1], self.bottom_right_coord[0], self.bottom_right_coord[1])

        painter_obj.drawLine(
            self.bottom_left_coord[0], self.bottom_left_coord[1], self.bottom_right_coord[0], self.bottom_right_coord[1])

        # Calculate Left and Right coordinates for the latitudes
        top_one_third_coord_left = (int((2/3)*(self.top_left_coord[0]))+int((1/3)*(self.bottom_left_coord[0])), int(
            (2/3)*(self.top_left_coord[1]))+int((1/3)*(self.bottom_left_coord[1])))
        top_two_third_coord_left = (int((1/3)*(self.top_left_coord[0]))+int((2/3)*(self.bottom_left_coord[0])), int(
            (1/3)*(self.top_left_coord[1]))+int((2/3)*(self.bottom_left_coord[1])))

        top_one_third_coord_right = (int((2/3)*(self.top_right_coord[0]))+int((1/3)*(self.bottom_right_coord[0])), int(
            (2/3)*(self.top_right_coord[1]))+int((1/3)*(self.bottom_right_coord[1])))
        top_two_third_coord_right = (int((1/3)*(self.top_right_coord[0]))+int((2/3)*(self.bottom_right_coord[0])), int(
            (1/3)*(self.top_right_coord[1]))+int((2/3)*(self.bottom_right_coord[1])))

        # Draw latitudes
        painter_obj.drawLine(top_one_third_coord_left[0], top_one_third_coord_left[1],
                             top_one_third_coord_right[0], top_one_third_coord_right[1])
        painter_obj.drawLine(top_two_third_coord_left[0], top_two_third_coord_left[1],
                             top_two_third_coord_right[0], top_two_third_coord_right[1])

        # Calculate Top and Bottom coordinates for the longitudes
        left_one_third_coord_top = (int((2/3)*(self.top_left_coord[0]))+int((1/3)*(self.top_right_coord[0])), int(
            (2/3)*(self.top_left_coord[1]))+int((1/3)*(self.top_right_coord[1])))
        left_two_third_coord_top = (int((1/3)*(self.top_left_coord[0]))+int((2/3)*(self.top_right_coord[0])), int(
            (1/3)*(self.top_left_coord[1]))+int((2/3)*(self.top_right_coord[1])))

        left_one_third_coord_bottom = (int((2/3)*(self.bottom_left_coord[0]))+int((1/3)*(self.bottom_right_coord[0])), int(
            (2/3)*(self.bottom_left_coord[1]))+int((1/3)*(self.bottom_right_coord[1])))
        left_two_third_coord_bottom = (int((1/3)*(self.bottom_left_coord[0]))+int((2/3)*(self.bottom_right_coord[0])), int(
            (1/3)*(self.bottom_left_coord[1]))+int((2/3)*(self.bottom_right_coord[1])))

        # Draw longitudes
        painter_obj.drawLine(left_one_third_coord_top[0], left_one_third_coord_top[1],
                             left_one_third_coord_bottom[0], left_one_third_coord_bottom[1])
        painter_obj.drawLine(left_two_third_coord_top[0], left_two_third_coord_top[1],
                             left_two_third_coord_bottom[0], left_two_third_coord_bottom[1])

        painter_obj.end()

        # Update the image label with the new lines
        self.lax_goal_label.setPixmap(self.pixmap_object)

    def get_window_title(self):
        """get_window_title.

        Getter function for Window Title
        """

        return self.window_title


class FocalLengthFinder:
    """FocalLengthFinder.

    This class finds the focal length of the camera and can be used to test the accuracy using the get_obj_distance function.
    """

    def __init__(self, points_drawn):
        """__init__.

        Initializes the class with required constants

        :param points_drawn: List of all the tuples consisting of the coordinates that the user has drawn
        """

        # Lax Goal is 72 inches (i.e.: 6 ft) - it is also square.
        self.lax_goal_length = 72

        # Focal length of the camera
        # NOTE: This is a random number that should be concretely set using the get_focal_length() function
        self.focal_length = 10

        # Collection of the four points that user drew on the picture
        # NOTE: This list will always include points (tuples in (x,y)) in the following order:
        # 1. Top Left
        # 2. Top Right
        # 3. Bottom Right
        # 4. Bottom Left
        self.points_drawn = points_drawn

    def get_obj_distance(self):
        """get_obj_distance.

        Getter function for the object distance using the Triangle Similarity algorithm
        """

        # Find the length of the line drawn by the two bottom points in pixels
        # NOTE: We use the two bottom points in the image because it is the least arbitrary (since it is in relation with the ground).
        # However, other points can also be used and experimented with if they yield better results.
        pixels_perceived = math.sqrt((self.points_drawn[3][0] - self.points_drawn[2][0])**2 + (
            self.points_drawn[3][1] - self.points_drawn[2][1])**2)

        # New distance = (Known object distance * camera's focal length)/pixels perceived
        return (self.lax_goal_length * self.focal_length)/pixels_perceived

    def get_focal_length(self, pixels_perceived, known_distance):
        """get_focal_length.

        Gets the focal length of the camera

        :param pixels_perceived: Length of a side (in pixels)
        :param known_distance: The given distance (in inches)
        """

        # Focal length of camera = (Pixels of one side * distance from object to camera)/Actual width of the object
        return (pixels_perceived * known_distance)/self.lax_goal_length


def run_app():
    """run_app.

    Returns the TrainingGoalCalibrationScreen object to get the points that the user selected
    """

    app = QApplication(sys.argv)
    calib_screen = TrainingGoalCalibrationScreen()
    # Display the widget
    win = TestWindow(calib_screen)
    win.show()
    app.exec_()

    return calib_screen


def main():
    """main.

    Main prototype/testing area. Code prototyping and checking happens here.
    """
    # 1. Move Ball-E set distance from the goal
    video_generator = VideoView()
    # 2. Take a picture with this camera and save it
    video_generator.run()
    # 3. Draw four points on the image to create a perimeter around the goal
    calib_screen = run_app()
    # 4. Calculate the pixels perceived using the two bottom points
    focal_length_finder = FocalLengthFinder(
        points_drawn=calib_screen.selected_points)
    # 5. Get focal length
    print("Focal Length of Camera: {} pixels".format(
        focal_length_finder.get_focal_length()))


if __name__ == "__main__":
    # Run the main function
    main()
