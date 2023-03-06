from PIL import Image
import numpy as np

# Not my code
def img_output(grid, obstacles, path):
	for x in obstacles:
		grid[x] = 0
	
	grid = 150 * grid / grid.max()

	for x in path:
		grid[x] = 200
	
	for x in obstacles:
		grid[x] = 255
		
	img = Image.fromarray(np.uint8(grid))
	img.show()

    # img.save(f"images/img.png")
