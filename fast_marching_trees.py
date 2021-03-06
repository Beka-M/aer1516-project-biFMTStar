"""
Fast Marching Trees (FMT*)
@author: huiming zhou
"""

import os
import sys
import math
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import time
from matplotlib import animation, rc

sys.path.append(os.path.dirname(os.path.abspath(__file__)) +
                "/../../Sampling_based_Planning/")

import env, plotting, utils


class Node:
    def __init__(self, n):
        self.x = n[0]
        self.y = n[1]
        self.parent = None
        self.cost = np.inf


class FMT:
    def __init__(self, x_start, x_goal, search_radius, n):
        self.x_init = Node(x_start)
        self.x_goal = Node(x_goal)
        self.search_radius = search_radius

        self.env = env.Env()
        self.plotting = plotting.Plotting(x_start, x_goal)
        self.utils = utils.Utils()

        self.fig, self.ax = plt.subplots()
        self.delta = self.utils.delta
        self.x_range = self.env.x_range
        self.y_range = self.env.y_range
        self.obs_circle = self.env.obs_circle
        self.obs_rectangle = self.env.obs_rectangle
        self.obs_boundary = self.env.obs_boundary

        self.V = set()
        self.V_unvisited = set()
        self.V_open = set()
        self.V_closed = set()
        self.sample_numbers = n
        self.coll_checks = 0
        self.success = True
        self.time_elapsed = 0

    def Init(self):
        samples = self.SampleFree()

        self.x_init.cost = 0.0
        self.V.add(self.x_init)
        self.V.update(samples)
        self.V_unvisited.update(samples)
        self.V_unvisited.add(self.x_goal)
        self.V_open.add(self.x_init)

    def Planning(self):
        start_t = time.time()
        self.Init()
        z = self.x_init
        n = self.sample_numbers
        rn = self.search_radius * math.sqrt((math.log(n) / n))
        Visited = []

        while z is not self.x_goal:
            V_open_new = set()
            X_near = self.Near(self.V_unvisited, z, rn)
            Visited.append(z)

            for x in X_near:
                Y_near = self.Near(self.V_open, x, rn)
                cost_list = {y: y.cost + self.Cost(y, x) for y in Y_near}
                y_min = min(cost_list, key=cost_list.get)

                self.coll_checks += 1
                if not self.utils.is_collision(y_min, x):
                    x.parent = y_min
                    V_open_new.add(x)
                    self.V_unvisited.remove(x)
                    x.cost = y_min.cost + self.Cost(y_min, x)

            self.V_open.update(V_open_new)
            self.V_open.remove(z)
            self.V_closed.add(z)

            if not self.V_open:
                print("open set empty!")
                self.success = False
                break

            cost_open = {y: y.cost for y in self.V_open}
            z = min(cost_open, key=cost_open.get)

        self.time_elapsed = time.time()-start_t
        print('time elapsed: ', self.time_elapsed)
        print('cost', self.x_goal.cost)
        print('collison checks: ', self.coll_checks)
        # node_end = self.ChooseGoalPoint()
        path_x, path_y = self.ExtractPath()
        print(path_x, path_y)
        self.animation(path_x, path_y, Visited[1: len(Visited)])

    def ChooseGoalPoint(self):
        Near = self.Near(self.V, self.x_goal, 2.0)
        cost = {y: y.cost + self.Cost(y, self.x_goal) for y in Near}

        return min(cost, key=cost.get)

    def ExtractPath(self):
        path_x, path_y = [], []
        node = self.x_goal

        while node.parent:
            path_x.append(node.x)
            path_y.append(node.y)
            node = node.parent

        path_x.append(self.x_init.x)
        path_y.append(self.x_init.y)

        return path_x, path_y

    def Cost(self, x_start, x_end):
        if self.utils.is_collision(x_start, x_end):
            return np.inf
        else:
            return self.calc_dist(x_start, x_end)

    @staticmethod
    def calc_dist(x_start, x_end):
        return math.hypot(x_start.x - x_end.x, x_start.y - x_end.y)

    @staticmethod
    def Near(nodelist, z, rn):
        return {nd for nd in nodelist
                if 0 < (nd.x - z.x) ** 2 + (nd.y - z.y) ** 2 <= rn ** 2}

    def SampleFree(self):
        n = self.sample_numbers
        delta = self.utils.delta
        Sample = set()

        ind = 0
        while ind < n:
            node = Node((random.uniform(self.x_range[0] + delta, self.x_range[1] - delta),
                         random.uniform(self.y_range[0] + delta, self.y_range[1] - delta)))
            if self.utils.is_inside_obs(node):
                continue
            else:
                Sample.add(node)
                ind += 1

        return Sample

    def animation(self, path_x, path_y, visited):
        self.plot_grid("Fast Marching Trees (FMT*)")

        for node in self.V:
            plt.plot(node.x, node.y, marker='.', color='lightgrey', markersize=3)

        count = 0
        for node in visited:
            count += 1
            plt.plot([node.x, node.parent.x], [node.y, node.parent.y], '-g')
            plt.gcf().canvas.mpl_connect(
                'key_release_event',
                lambda event: [exit(0) if event.key == 'escape' else None])
            if count % 10 == 0:
                plt.pause(0.001)

        plt.plot(path_x, path_y, linewidth=2, color='red')
        plt.pause(0.01)
        # plt.close()
        plt.show()

    def plot_grid(self, name):

        for (ox, oy, w, h) in self.obs_boundary:
            self.ax.add_patch(
                patches.Rectangle(
                    (ox, oy), w, h,
                    edgecolor='black',
                    facecolor='black',
                    fill=True
                )
            )

        for (ox, oy, w, h) in self.obs_rectangle:
            self.ax.add_patch(
                patches.Rectangle(
                    (ox, oy), w, h,
                    edgecolor='black',
                    facecolor='gray',
                    fill=True
                )
            )

        for (ox, oy, r) in self.obs_circle:
            self.ax.add_patch(
                patches.Circle(
                    (ox, oy), r,
                    edgecolor='black',
                    facecolor='gray',
                    fill=True
                )
            )

        plt.plot(self.x_init.x, self.x_init.y, "bs", linewidth=3)
        plt.plot(self.x_goal.x, self.x_goal.y, "rs", linewidth=3)

        plt.title(name)
        plt.axis("equal")


def main():
        # x_start = (6, 6)  # Starting node
        x_start = (18, 8)
        x_goal = (40, 25)  # Goal node
        # x_start = (2, 2)
        # x_goal = (47, 27)

        # fmt = FMT(x_start, x_goal, 40, 500)
        # fmt.plot_grid("Bidirectional Fast Marching Trees (Bi-FMT*)")
        # plt.show()

        col_check_res = []
        cost_res = []
        time_elp_res = []
        suc_rate_res = []
        sample_n = [500, 1000, 1500, 2000, 2500, 3000]
        for n in sample_n:
            col_check = 0
            cost = 0
            time_elp = 0
            suc_rate = 0
            for run in range(100):
                print(n, run)
                fmt = FMT(x_start, x_goal, 40, n)
                fmt.Planning()

                if fmt.success:
                    suc_rate += fmt.success
                    time_elp += fmt.time_elapsed
                    cost += fmt.x_goal.cost
                    col_check += fmt.coll_checks

            if suc_rate:
                time_elp = time_elp / suc_rate
                time_elp_res.append(time_elp)
                cost = cost / suc_rate
                cost_res.append(cost)
                col_check = col_check / suc_rate
                col_check_res.append(col_check)
                suc_rate = suc_rate / 100
                suc_rate_res.append(suc_rate)
            else:
                time_elp_res.append(np.inf)
                cost_res.append(np.inf)
                col_check_res.append(np.inf)
                suc_rate_res.append(0)

        return time_elp_res, cost_res, col_check_res, suc_rate_res


if __name__ == '__main__':
    main()
