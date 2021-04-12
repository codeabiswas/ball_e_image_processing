class GoalDistanceCalculator:
    def __init__(self):

        # Lax Goal is 72 inches (i.e.: 6 ft) - it is also square.
        self.lax_goal_length = 72

        self.focal_length = 10

    def get_focal_length(self, pixels_perceived, known_distance):
        """Helper function to get the focal length of the lens
        """

        # Focal length of camera = (Pixels of one side X distance from object to camera)/Actual width of the object
        return (pixels_perceived*known_distance)/self.lax_goal_length

    def get_obj_distance(self, pixels_perceived):
        return (self.lax_goal_length * self.focal_length)/pixels_perceived


def main():
    pass


if __name__ == "__main__":
    main()
