from fsm_2d import FastSweepingMethodTwoDimension


class PathFinder:

    def __init__(self, grid: list[float]) -> None:
        self.grid = grid
        self.path = []
        self.x_len = len(grid[0])
        self.y_len = len(grid)

    def find_path(self, point: tuple[int]) -> list[float]:
        self.path.append(point)
        index = 0

        while not self.__source_found(self.path[index]):
            self.path.append(self.__find_smallest_neighbor(*self.path[index]))
            index += 1

        return self.path

    '''
    :param i: x coordinate
    :param j: y coordinate
    '''

    def __find_smallest_neighbor(self, i, j) -> tuple[int]:
        points = []

        if j < self.y_len-1:
            points.append([j+1, i])

        if j > 0:
            points.append([j-1, i])

        if i < self.x_len-1:
            points.append([j, i+1])

        if i > 0:
            points.append([j, i-1])

        if i < self.x_len-1 and j < self.y_len-1:
            points.append([j+1, i+1])

        if i < self.x_len-1 and j > 0:
            points.append([j-1, i+1])

        if i > 0 and j < self.y_len-1:
            points.append([j+1, i-1])

        if i > 0 and j > 0:
            points.append([j-1, i-1])

        # Create a list of values corresponding to the valid points
        values = list(map(lambda p: self.grid[p[0], p[1]], points))
        # Find the i, j coordinates of the min value
        return points[values.index(min(values))][::-1]

    def __source_found(self, point: tuple[int]) -> bool:
        return self.grid[point[1], point[0]] == 0


if __name__ == "__main__":
    f = 1
    h = 1
    dimension = 7
    p1 = (1, 1)

    fsm = FastSweepingMethodTwoDimension(f, h, dimension, p1)

    fsm.solve()
    fsm.print_formatted_grid()

    path_finder = PathFinder(fsm.grid)
    path = path_finder.find_path(point=(5, 6))
    print(path)
