"""
Environment for rrt_2D
@author: huiming zhou
"""


class Env:
    def __init__(self):
        self.x_range = (0, 50)
        self.y_range = (0, 30)
        self.obs_boundary = self.obs_boundary()
        self.obs_circle = self.obs_circle()
        self.obs_rectangle = self.obs_rectangle()

    @staticmethod
    def obs_boundary():
        obs_boundary = [
            [0, 0, 1, 30],
            [0, 30, 50, 1],
            [1, 0, 50, 1],
            [50, 1, 1, 30]
        ]
        return obs_boundary

    @staticmethod
    def obs_rectangle():
        # obs_rectangle = [
        #     [5, 9, 16, 2],
        #     [26, 18, 2, 9],
        #     [26, 4, 2, 12],
        # ]
        obs_rectangle = [
            [14, 9, 8, 2],
            [14, 4, 8, 3],
            [19, 7, 3, 2],
            [18, 22, 8, 3],
            [26, 7, 2, 12],
            # [32, 15, 8, 2],
            # [32, 19, 8, 2],
            # [32, 17, 4, 2]
            [34, 15, 2, 12]
        ]
        # obs_rectangle = [
        #     [14, 12, 8, 2],
        #     [18, 22, 8, 3],
        #     [26, 7, 2, 12],
        #     [32, 14, 10, 2]
        # ]
        return obs_rectangle

    @staticmethod
    def obs_circle():
        # obs_cir = []
        obs_cir = [
            [7, 12, 3],
            [46, 20, 2],
            [37, 7, 3],
        ]
        # obs_cir = [
        #     [7, 12, 3],
        #     [46, 20, 2],
        #     [15, 5, 2],
        #     [37, 7, 3],
        #     [37, 23, 3]
        # ]

        return obs_cir