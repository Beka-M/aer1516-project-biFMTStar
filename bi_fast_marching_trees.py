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
import itertools
from matplotlib import animation, rc

sys.path.append(os.path.dirname(os.path.abspath(__file__)) +
                "/../../Sampling_based_Planning/")

import env, plotting, utils


class Node:
    def __init__(self, n):
        self.x = n[0]
        self.y = n[1]
        self.parent = {0: None, 1: None}
        self.cost = {0: np.inf, 1: np.inf}


class FMT:
    def __init__(self, x_start, x_goal, search_radius, n):
        self.x_init = Node(x_start)
        self.x_goal = Node(x_goal)
        self.x_meet = Node((-1, -1))
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

        self.V = {0: set(), 1: set()}
        self.V_unvisited = {0: set(), 1: set()}
        self.V_open = {0: set(), 1: set()}
        self.V_closed = {0: set(), 1: set()}

        self.sample_numbers = n
        self.tree = 0   # 1: use forward tree; 0: use backward tree
        self.coll_check = 0   # Record number of collision checks have done
        self.fail = False   # To compute success rate

    def Init(self):
        samples = self.SampleFree()

        self.x_init.cost[0] = 0.0
        self.V[0].add(self.x_init)
        self.V[0].update(samples)
        self.V_unvisited[0].update(samples)
        # self.VF_unvisited.add(self.x_goal)
        self.V_open[0].add(self.x_init)

        self.x_goal.cost[1] = 0.0
        self.V[1].add(self.x_goal)
        self.V[1].update(samples)
        self.V_unvisited[1].update(samples)
        # self.VB_unvisited.add(self.x_goal)
        self.V_open[1].add(self.x_goal)

    def Planning(self):
        start_t = time.time()
        self.Init()
        n = self.sample_numbers
        rn = self.search_radius * math.sqrt((math.log(n) / n))

        z = self.x_init
        Visited = []

        # while self.x_meet.x == -1:   # faster but not optimal, returns the first feasible path
        while z not in self.V_closed[not self.tree]:    # slower but seems to return optimal path as written in the paper
            Visited = self.ExpandTreeFromNode(z, rn, Visited)

            if not self.V_open[0] and not self.V_open[1]:
                print("Both open set empty!")
                self.fail = True
                break

            if not self.V_closed[1]:
                self.tree = not self.tree
                z = self.x_goal
                continue

            if not self.V_open[not self.tree]:
                cost_open = {y: y.cost[self.tree] for y in self.V_open[self.tree]}
                z = min(cost_open, key=cost_open.get)
            else:
                self.tree = not self.tree
                cost_open = {y: y.cost[self.tree] for y in self.V_open[self.tree]}
                z = min(cost_open, key=cost_open.get)

        print('time elapsed: ', time.time()-start_t)
        print('cost: ', self.x_meet.cost[0]+self.x_meet.cost[1])   # total cost of the final path (need to double-check this)
        print('Collison checks: ', self.coll_check)
        path_x, path_y = self.ExtractPath()
        self.animation(path_x, path_y, Visited[2: len(Visited)])
        # anim = animation.FuncAnimation(self.fig, self.animation(path_x, path_y, Visited[1: len(Visited)]), frames=10, interval=10, blit=True)
        # anim.save('fmt_animation.gif', writer="PillowWriter", fps=60)

    def ExpandTreeFromNode(self, z, rn, Visited):
        V_open_new = set()
        X_near = self.Near(self.V_unvisited[self.tree], z, rn)
        Visited.append(z)

        for x in X_near:
            Y_near = self.Near(self.V_open[self.tree], x, rn)
            cost_list = {y: y.cost[self.tree] + self.Cost(y, x) for y in Y_near}
            y_min = min(cost_list, key=cost_list.get)

            self.coll_check += 1
            if not self.utils.is_collision(y_min, x):
                x.parent[self.tree] = y_min
                V_open_new.add(x)
                self.V_unvisited[self.tree].remove(x)
                x.cost[self.tree] = y_min.cost[self.tree] + self.Cost(y_min, x)

                if x not in self.V_unvisited[not self.tree]:
                    if self.x_meet.x == -1:
                        self.x_meet = x
                    else:
                        if (self.x_meet.cost[0] + self.x_meet.cost[1]) > (x.cost[0] + x.cost[1]):
                            self.x_meet = x

        self.V_open[self.tree].update(V_open_new)
        self.V_open[self.tree].remove(z)
        self.V_closed[self.tree].add(z)
        print(self.tree, z.x, z.y)
        return Visited

    def ExtractPath(self):
        path_x, path_y, F_x, F_y, B_x, B_y = [], [], [], [], [], []

        self.tree = 0
        node = self.x_meet
        while node.parent[self.tree]:
            F_x.append(node.x)
            F_y.append(node.y)
            node = node.parent[self.tree]

        self.tree = 1
        node = self.x_meet
        while node.parent[self.tree]:
            B_x.append(node.x)
            B_y.append(node.y)
            node = node.parent[self.tree]

        path_x.append(self.x_goal.x)
        path_y.append(self.x_goal.y)
        B_x.reverse(), B_y.reverse()
        B_x.pop(-1), B_y.pop(-1)
        for x in B_x:
            path_x.append(x)
        for y in B_y:
            path_y.append(y)
        for x in F_x:
            path_x.append(x)
        for y in F_y:
            path_y.append(y)
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

        for node in self.V[0]:
            plt.plot(node.x, node.y, marker='.', color='lightgrey', markersize=3)

        count = 0
        for node in visited:
            count += 1
            if node.parent[0] and node.parent[1]:
                print(node, node.parent)
            if node.parent[0]:
                x = node.parent[0].x
                y = node.parent[0].y
            else:
                x = node.parent[1].x
                y = node.parent[1].y
            plt.plot([node.x, x], [node.y, y], '-g')
            plt.gcf().canvas.mpl_connect(
                'key_release_event',
                lambda event: [exit(0) if event.key == 'escape' else None])
            if count % 10 == 0:
                plt.pause(0.001)

        print('path x:', path_x)
        print('path y:', path_y)
        plt.plot(path_x, path_y, linewidth=2, color='red')
        plt.pause(0.01)
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
    x_start = (18, 8)  # Starting node
    x_goal = (37, 18)  # Goal node
    # x_start = (2, 2)
    # x_goal = (47, 27)

    fmt = FMT(x_start, x_goal, 40, 1000)
    # fmt.plot_grid("Fast Marching Trees (FMT*)")
    # plt.show()
    fmt.Planning()
    if fmt.fail:
        print('Failed to return path')
    else:
        print('Success!!!')


if __name__ == '__main__':
    main()
