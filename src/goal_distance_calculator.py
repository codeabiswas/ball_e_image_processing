import math


class GoalDistanceCalculator:
    """This helper class uses the Triangle Similarity algorithm to find the distance between the goal and Ball-E
    """

    def __init__(self, points_drawn):
        """Initializer for the distance finder between Ball-E and the Goal

        Args:
            points_drawn ([list]): List of tuples including (x,y) coordinates containing the user selected points on the picture
        """

        # Lax Goal is 72 inches (i.e.: 6 ft) - it is also square.
        self.lax_goal_length = 72

        # Focal length of the camera
        self.focal_length = 10

        # Collection of the four points that user drew on the picture
        # NOTE: This list will always include points (tuples in (x,y)) in the following order:
        # 1. Top Left
        # 2. Top Right
        # 3. Bottom Right
        # 4. Bottom Left
        self.points_drawn = points_drawn

    def get_obj_distance(self):
        """Distance from Ball-E to goal calculator

        Returns:
            [float]: Distance from Ball-E to goal in inches
        """

        # Find the length of the line drawn by the two bottom points in pixels
        pixels_perceived = math.sqrt((self.points_drawn[3][0] - self.points_drawn[2][0])**2 + (
            self.points_drawn[3][1] - self.points_drawn[2][1])**2)

        # New distance = (Known object distance * camera's focal length)/pixels perceived
        return (self.lax_goal_length * self.focal_length)/pixels_perceived


def main():
    """Execute checks for above class
    """

    distance_finder = GoalDistanceCalculator([(0, 0), (0, 1), (1, 0), (1, 1)])

    print(distance_finder.get_obj_distance())


if __name__ == "__main__":
    main()
