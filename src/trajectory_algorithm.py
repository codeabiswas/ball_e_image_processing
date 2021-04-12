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
        self.diag_dist_from_center = math.sqrt(8)
        self.straight_dist_from_center = 2

        # Required distances for pitch (in ft.)
        self.bottom_dist = 1
        self.middle_dist = 3
        self.top_dist = 5

    def calc_yaw(self, target):
        """Calculates the yaw of the trajectory from the center of the goal

        Args:
            target (string): Which section of the goal the ball will be shot at (TL, TM, TR, CL, CM, CR, BL, BM, BR)

        Returns:
            float/int: The angle in degrees
        """

        # If target is TL or BL, then it is a negative angle based on a diagonal distance
        if "L" in target and ("T" in target or "B" in target):
            return -math.degrees(math.atan(self.diag_dist_from_center/self.distance_from_goal))
        # If target is TR or BR, then it is a positive angle based on a diagonal distance
        elif "R" in target and ("T" in target or "B" in target):
            return math.degrees(math.atan(self.diag_dist_from_center/self.distance_from_goal))
        # If target is CM, then yaw angle is 0 (since there is no change from the center of the goal)
        elif "CM" in target:
            return 0
        # For all other targets (i.e.: TM, CL, CR, BM)
        else:
            return math.degrees(math.atan(self.straight_dist_from_center/self.distance_from_goal))

    def calc_pitch(self, target):
        """Calculates the pitch of the trajectory from the ground

        Args:
            target (string): Which section of the goal the ball will be shot at (TL, TM, TR, CL, CM, CR, BL, BM, BR)

        Returns:
            float/int: The angle in degrees
        """

        # If target is Bottom of the goal, then it is negative angle
        if "B" in target:
            return -math.degrees(math.atan(self.bottom_dist/self.distance_from_goal))
        # If target is center of the goal, then it is positive angle
        elif "C" in target:
            return math.degrees(math.atan(self.middle_dist/self.distance_from_goal))
        # If target is top of the goal, then it is positive angle
        elif "T" in target:
            return math.degrees(math.atan(self.top_dist/self.distance_from_goal))


def main():
    pass


if __name__ == "__main__":
    main()
