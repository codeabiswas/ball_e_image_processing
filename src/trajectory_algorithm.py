"""
trajectory_algorithm.py
---
This file contains the TrajectoryAlgorithm class, which is used for calculating the angles by which the pitch and yaw need to move to shoot at the specified location in a goal
---

Author: Andrei Biswas (@codeabiswas)
Date: May 4, 2021
Last Modified: May 04, 2021
"""

import math


class TrajectoryAlgorithm:
    """This class contains all the helper methods required to calculate the trajectory of the lacrosse ball, given the distance from Ball-E to the goal. It uses simple inverse tan to calculate pitch and yaw (i.e.: invtan(Opposite/Adjacent))
    """

    def __init__(self, distance_from_goal):
        """Initialization method for Trajectory Algorithm. This will initialize all the distances from the center of the goal (for yaw) and distances from the ground (for pitch)

        Args:
            distance_from_goal ([float]): The distance of Ball-E from the Goal (in ft.)
        """
        # Distance of Ball-E from the Goal
        self.distance_from_goal = distance_from_goal

        # Required distances for yaw (in ft.)
        self.straight_dist_from_center = 2
        
        # NOTE: These constants are subject to change when the motor is tuned and tested with a real lacrosse goal
        self.mid_yaw_const = 0
        self.center_pitch_const = 0

        # Required distances for pitch (in ft.)
        self.top_dist = 2
        self.middle_dist = 0
        self.bottom_dist = 2

        # Gear Ratio for Yaw is 12.8:1
        self.gear_ratio_yaw = 12.8
        # Gear Ratio for Pitch is 9:1
        self.gear_ratio_pitch = 9

    def calc_yaw(self, target):
        """Calculates the yaw of the trajectory from the center of the goal

        Args:
            target (string): Which section of the goal the ball will be shot at (TL, TM, TR, CL, CM, CR, BL, BM, BR)

        Returns:
            float/int: The angle in degrees
        """

        # If target is to the left, then it is a negative angle based on a diagonal distance
        if "L" in target:
            return -math.degrees(math.atan(self.straight_dist_from_center/self.distance_from_goal))*self.gear_ratio_yaw
        # If target is M, then yaw angle is 0 (since there is no change from the center of the goal)
        elif "M" in target:
            return self.mid_yaw_const
        # If target is to the right, then it is a positive angle based on a diagonal distance
        elif "R" in target:
            return math.degrees(math.atan(self.straight_dist_from_center/self.distance_from_goal))*self.gear_ratio_yaw

    def calc_pitch(self, target):
        """Calculates the pitch of the trajectory from the ground

        Args:
            target (string): Which section of the goal the ball will be shot at (TL, TM, TR, CL, CM, CR, BL, BM, BR)

        Returns:
            float/int: The angle in degrees
        """

        # If target is top of the goal, then it is positive angle
        if "T" in target:
            return math.degrees(math.atan(self.top_dist/self.distance_from_goal))*self.gear_ratio_pitch
        # If target is center of the goal, then it is positive angle
        elif "C" in target:
            return self.center_pitch_const
        # If target is Bottom of the goal, then it is negative angle
        elif "B" in target:
            return -math.degrees(math.atan(self.bottom_dist/self.distance_from_goal))*self.gear_ratio_pitch


def main():
    """Main prototype/testing area. Code prototyping and checking happens here."""

    # Assume 15 ft. away
    trajectory_alg = TrajectoryAlgorithm(15)
    for shot_loc in ["TL", "TM", "TR", "CL", "CM", "CR", "BL", "BM", "BR"]:
        print("For {}:\nYaw={}\nPitch={}\n".format(shot_loc, trajectory_alg.calc_yaw(
            shot_loc), trajectory_alg.calc_pitch(shot_loc)))


if __name__ == "__main__":
    # Run the main function
    main()
