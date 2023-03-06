from fsm_2d import FastSweepingMethodTwoDimension
from path_finder import PathFinder
from image_output import img_output
import numpy as np

def main():
	    # f, h, dim, points, obstacles, fill_value
    arg1 = (lambda i, j: (i+1)**2 + (j+1)**2, 1, 7, (1, 1), None)
    arg2 = (lambda i, j: 1, 1, 7, (1, 1), None)
    arg3 = (lambda i, j: (i+1)**2 + (j+1)**2, 1, 7, (3, 3), None)
    arg4 = (lambda i, j: 1, 1, 7, ((1, 1), (4, 5)), None)
    arg5 = (lambda i, j: np.sin(i)+1, 1, 11, ((5, 5)), None)
    arg6 = (lambda i, j: 1, 1, 11, ((0, 5)), ((5, 2), (5, 3), (5, 4), (5, 5), (5, 6)))

    fsm = FastSweepingMethodTwoDimension(*arg2)
    fsm.solve(n=4)
    fsm.print_formatted_grid(fsm.grid)
    
    path_finder = PathFinder(fsm.grid)
    path = path_finder.find_path(point=(5, 6))
    print(path)


if __name__ == "__main__":
	main()
