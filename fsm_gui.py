import pygame

# figure out mouse click and get coordinate of the box for clicking
# Implement pygame.time.get_ticks() to time program and space out the path advancement

def draw_rectangles(s, x, y, p_l, p_g, c=(255, 255, 255)):
    for i in range(x):
        for j in range(y):
            pygame.draw.rect(surface=s, color=c,
                             rect=pygame.Rect(p_l + (i * p_l) + (i * p_g), 
                                              p_l + (j * p_l) + (j * p_g), 
                                              p_g, p_g))

def main():
    x_len = 50
    y_len = 50
    pixels_per_grid = 10
    pixels_per_line = 1

    pygame.init()

    screen = pygame.display.set_mode(
        [x_len * pixels_per_grid + (x_len+1) * pixels_per_line,
        y_len * pixels_per_grid + (y_len+1) * pixels_per_line])

    grids = []

    is_running = True
    draw_rectangles(screen, x_len, y_len, pixels_per_line, pixels_per_grid)
    pygame.display.flip()

    while is_running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
