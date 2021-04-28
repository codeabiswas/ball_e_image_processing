import math


class TrajectoryAlgorithm:
    """This class contains all the helper methods required to calculate the trajectory of the lacrosse ball, given the distance from Ball-E to the goal. It uses simple inverse tan to calculate pitch and yaw (i.e.: SOH-CAH-TOA)
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

        # Required distances for pitch (in ft.)
        self.bottom_dist = 2
        self.middle_dist = 0
        self.top_dist = 2
        # self.bottom_dist = 1
        # self.middle_dist = 3
        # self.top_dist = 5

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
        # If target is to the right, then it is a positive angle based on a diagonal distance
        elif "R" in target:
            return math.degrees(math.atan(self.straight_dist_from_center/self.distance_from_goal))*self.gear_ratio_yaw
        # If target is CM, then yaw angle is 0 (since there is no change from the center of the goal)
        elif "M" in target:
            return 0

    def calc_pitch(self, target):
        """Calculates the pitch of the trajectory from the ground

        Args:
            target (string): Which section of the goal the ball will be shot at (TL, TM, TR, CL, CM, CR, BL, BM, BR)

        Returns:
            float/int: The angle in degrees
        """

        # If target is Bottom of the goal, then it is negative angle
        if "B" in target:
            return -math.degrees(math.atan(self.bottom_dist/self.distance_from_goal))*self.gear_ratio_pitch
        # If target is center of the goal, then it is positive angle
        elif "C" in target:
            return 0
            # return math.degrees(math.atan(self.middle_dist/self.distance_from_goal))*self.gear_ratio_pitch
        # If target is top of the goal, then it is positive angle
        elif "T" in target:
            return math.degrees(math.atan(self.top_dist/self.distance_from_goal))*self.gear_ratio_pitch


def main():
    # Assume 15 ft. away
    trajectory_alg = TrajectoryAlgorithm(15)
    for shot_loc in ["TL", "TM", "TR", "CL", "CM", "CR", "BL", "BM", "BR"]:
        print("For {}:\nYaw={}\nPitch={}\n".format(shot_loc, trajectory_alg.calc_yaw(
            shot_loc), trajectory_alg.calc_pitch(shot_loc)))


if __name__ == "__main__":
    main()
