import numpy as np
import threading

"""
Something wrong with cost function value combining with equation. 
Check coordinate with math, coordinates start with 0,0 at top left
"""

class FastSweepingMethodTwoDimension:

    """
    :param f: The cost function
    :param h: The distance between each discretized point
    :param dim: size of one side of the square grid
    :param points: points to calculate distance for 2d tuple
    :param obstacles: 
    """

    def __init__(self, func_i_j, h: int, dim: int, points: tuple[tuple[int]], 
                 obstacles: tuple[tuple[int]], fill_value=1e10) -> None:
        if isinstance(points[0], int):
            points = (points,)
        self.dim = dim
        self.func_i_j = self.calculate_f(func_i_j, obstacles)
        self.h = h
        self.grid = np.full(
            shape=(dim, dim), fill_value=fill_value, dtype=np.float64)

        # Set the fixed points
        for i, j in points:
            self.grid[j, i] = 0

    def calculate_f(self, f, obstacles):
        f_new = np.zeros(shape=(self.dim, self.dim))

        for j in range(self.dim):
            for i in range(self.dim):
                f_new[j, i] = f(i, j)
        
        if obstacles is not None:
            if isinstance(obstacles[0], int):
                obstacles = (obstacles,)

            for (i, j) in obstacles:
                f_new[j, i] = np.inf

        return f_new

    def solve(self, n=4) -> None:
        for _ in range(n):
            temp_grid = np.copy(self.grid)

            # Up-Right
            first_sweep = Sweep(temp_grid, self.func_i_j, self.h,
                                (0, self.dim, 1), (self.dim-1, -1, -1))

            # Up-Left
            second_sweep = Sweep(temp_grid, self.func_i_j, self.h,
                                (self.dim-1, -1, -1), (self.dim-1, -1, -1))

            # Down-Right
            third_sweep = Sweep(temp_grid, self.func_i_j, self.h,
                                (0, self.dim, 1), (0, self.dim, 1))

            # Down-Left
            fourth_sweep = Sweep(temp_grid, self.func_i_j, self.h, 
                                (self.dim-1, -1, -1), (0, self.dim, 1))

            first_sweep.start()
            second_sweep.start()
            third_sweep.start()
            fourth_sweep.start()

            first_sweep.join()
            second_sweep.join()
            third_sweep.join()
            fourth_sweep.join()

            self.__join_grids(first_sweep.grid, second_sweep.grid,
                            third_sweep.grid, fourth_sweep.grid)

    def __join_grids(self, g1, g2, g3, g4) -> None:
        for j in range(self.dim):
            for i in range(self.dim):
                self.grid[j, i] = min(g1[j, i], g2[j, i], g3[j, i], g4[j, i])

    def print_formatted_grid(self, g, format="%7.3f"):
        for row in g:
            for n in row:
                print(format % n, end=" ")
            print()


class Sweep(threading.Thread):

    def __init__(self, grid, f, h: int, x_range: tuple, y_range: tuple) -> None:
        super().__init__()
        self.grid = grid
        self.h = h
        self.f = f
        self.dim = len(self.grid)
        self.x_range = x_range
        self.y_range = y_range

    def run(self) -> None:
        # sweep through based on x_range and y_range
        for j in range(*self.y_range):
            for i in range(*self.x_range):
                self.grid[j, i] = min(
                    self.__u_new(self.__x_min(i, j), self.__y_min(i, j), i, j),
                    self.grid[j, i]
                )

    def __u_new(self, u_x, u_y, i, j):
        if (np.abs(u_x-u_y) >= self.h * self.f[j, i]):
            return min(u_x, u_y) + self.f[j, i] * self.h
        else:
            return np.divide(u_x + u_y + 
                             np.sqrt(2.0 * self.f[j, i]**2 * self.h**2 - 
                                     (u_x-u_y)**2), 2.0)

    def __x_min(self, i, j):
        if i - 1 < 0:
            return self.grid[j, i+1]
        elif i + 1 >= self.dim:
            return self.grid[j, i-1]
        
        return min(self.grid[j, i-1], self.grid[j, i+1])

    def __y_min(self, i, j):
        if j - 1 < 0:
            return self.grid[j+1, i]
        elif j + 1 >= self.dim:
            return self.grid[j-1, i]

        return min(self.grid[j-1, i], self.grid[j+1, i])


if __name__ == "__main__":
    # f, h, dim, points, obstacles, fill_value
    arg1 = (lambda i, j: (i+1)**2 + (j+1)**2, 1, 7, (1, 1), None)
    arg2 = (lambda i, j: 1, 1, 7, (1, 1), None)
    arg3 = (lambda i, j: (i+1)**2 + (j+1)**2, 1, 7, (3, 3), None)
    arg4 = (lambda i, j: 1, 1, 7, ((1, 1), (4, 5)), None)

    fsm = FastSweepingMethodTwoDimension(*arg4)

    fsm.solve(n=4)
    fsm.print_formatted_grid(fsm.grid)
