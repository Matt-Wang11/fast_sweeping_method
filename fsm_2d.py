import numpy as np
import threading


class FastSweepingMethodTwoDimension:

    """
    :param f: The cost function (currently only supporting constants)
    :param h: The distance between each discretized point
    :param dim: size of one side of the square grid
    :param points: points to calculate distance for 2d tuple
    """

    def __init__(self, f, h: int, dim: int, *points: tuple) -> None:
        self.dim = dim
        self.f = f
        self.h = h
        self.grid = np.full(
            shape=(dim, dim), fill_value=dim**2, dtype=np.float64)

        # Set the fixed points
        for i, j in points:
            self.grid[j, i] = 0

    def solve(self) -> None:
        # Up-Right
        first_sweep = Sweep(np.copy(self.grid), self.f, self.h,
                            (0, self.dim, 1), (self.dim-1, -1, -1))

        # Up-Left
        second_sweep = Sweep(np.copy(self.grid), self.f, self.h,
                             (self.dim-1, -1, -1), (self.dim-1, -1, -1))

        # Down-Right
        third_sweep = Sweep(np.copy(self.grid), self.f, self.h,
                            (0, self.dim, 1), (0, self.dim, 1))

        # Down-Left
        fourth_sweep = Sweep(np.copy(self.grid), self.f, self.h, 
                             (self.dim-1, -1, -1), (0, self.dim, 1))

        first_sweep.start()
        second_sweep.start()
        third_sweep.start()
        fourth_sweep.start()

        first_sweep.join()
        second_sweep.join()
        third_sweep.join()
        fourth_sweep.join()

        self.join_grids(first_sweep.grid, second_sweep.grid,
                        third_sweep.grid, fourth_sweep.grid)

    def join_grids(self, g1, g2, g3, g4) -> None:
        for j in range(self.dim):
            for i in range(self.dim):
                self.grid[j, i] = min(g1[j, i], g2[j, i], g3[j, i], g4[j, i])

    def print_formatted_grid(self):
        for row in self.grid:
            for n in row:
                print("%6.3f" % n, end=" ")
            print()


class Sweep(threading.Thread):

    def __init__(self, grid, f, h, x_range: tuple, y_range: tuple) -> None:
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
                    self.u_new(self.x_min(i, j), self.y_min(i, j)),
                    self.grid[j, i]
                )

    def u_new(self, u_x, u_y):
        if (np.abs(u_x-u_y) >= self.h * self.f):
            return min(u_x, u_y) + self.f * self.h
        else:
            return np.divide(u_x + u_y + 
                             np.sqrt(2.0 * self.f**2 * self.h**2 - (u_x-u_y)**2), 
                             2.0)

    def x_min(self, i, j):
        if i - 1 < 0:
            return self.grid[j, i+1]
        elif i + 1 >= self.dim:
            return self.grid[j, i-1]
        
        return min(self.grid[j, i-1], self.grid[j, i+1])

    def y_min(self, i, j):
        if j - 1 < 0:
            return self.grid[j+1, i]
        elif j + 1 >= self.dim:
            return self.grid[j-1, i]

        return min(self.grid[j-1, i], self.grid[j+1, i])


if __name__ == "__main__":
    f = 1
    h = 1
    dimension = 7
    p1 = (1, 1)

    fsm = FastSweepingMethodTwoDimension(f, h, dimension, p1)

    fsm.solve()
    fsm.print_formatted_grid()
