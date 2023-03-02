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
    """

    def __init__(self, func_i_j, h: int, dim: int, 
                 *points: tuple, fill_value=1e10) -> None:
        self.dim = dim
        self.func_i_j = func_i_j
        self.h = h
        self.grid = np.full(
            shape=(dim, dim), fill_value=fill_value, dtype=np.float64)

        # Set the fixed points
        for i, j in points:
            self.grid[j, i] = 0

    def solve(self) -> None:
        # Up-Right
        first_sweep = Sweep(np.copy(self.grid), self.func_i_j, self.h,
                            (0, self.dim, 1), (self.dim-1, -1, -1))

        # Up-Left
        second_sweep = Sweep(np.copy(self.grid), self.func_i_j, self.h,
                             (self.dim-1, -1, -1), (self.dim-1, -1, -1))

        # Down-Right
        third_sweep = Sweep(np.copy(self.grid), self.func_i_j, self.h,
                            (0, self.dim, 1), (0, self.dim, 1))

        # Down-Left
        fourth_sweep = Sweep(np.copy(self.grid), self.func_i_j, self.h, 
                             (self.dim-1, -1, -1), (0, self.dim, 1))

        first_sweep.start()
        second_sweep.start()
        third_sweep.start()
        fourth_sweep.start()

        first_sweep.join()
        second_sweep.join()
        third_sweep.join()
        fourth_sweep.join()

        self.print_formatted_grid(first_sweep.grid)
        print()
        self.print_formatted_grid(second_sweep.grid)
        print()
        self.print_formatted_grid(third_sweep.grid)
        print()
        self.print_formatted_grid(fourth_sweep.grid)
        print()

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
        if (np.abs(u_x-u_y) >= self.h * self.f(i, j)):
            return min(u_x, u_y) + self.f(i, j) * self.h
        else:
            return np.divide(u_x + u_y + 
                             np.sqrt(2.0 * self.f(i, j)**2 * self.h**2 - 
                                     (u_x-u_y)**2), 
                             2.0)

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
    # Might be smart to have f already calculated on a grid point and then we access the value
    f = lambda i, j: (i+1)
    h = 1
    dimension = 7
    p1 = (3, 3)

    fsm = FastSweepingMethodTwoDimension(f, h, dimension, p1)

    fsm.solve()
    fsm.print_formatted_grid(fsm.grid)
