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

def is_in_rectangle(mouse_x, mouse_y, left, top, right, down):
    return mouse_x > left and mouse_x < right and \
        mouse_y > top and mouse_y < down

def rectangle_clicked(mouse_x, mouse_y, left, top, p_g, event):
    return is_in_rectangle(mouse_x, mouse_y, left, top, left + p_g, top + p_g)\
    and event.type == pygame.MOUSEBUTTONDOWN

def click(s, x, y, mouse_x, mouse_y, p_l, p_g, c, event):
    coordinates = list

    for i in range(x):
        for j in range(y):
            left = p_l + (i * p_l) + (i * p_g)
            top = p_l + (j * p_l) + (j * p_g)

            if rectangle_clicked(mouse_x, mouse_y, left, top, p_g, event):
                pygame.draw.rect(surface=s, color=c, 
                                 rect=pygame.Rect(left, top, p_g, p_g))
                coordinates = [i, j]
                break;
    
    return coordinates

def main():
    x_len = 50
    y_len = 50
    pixels_per_grid = 10
    pixels_per_line = 1

    pygame.init()

    screen = pygame.display.set_mode(
        [x_len * pixels_per_grid + (x_len+1) * pixels_per_line,
        y_len * pixels_per_grid + (y_len+1) * pixels_per_line])

    is_running = True
    draw_rectangles(screen, x_len, y_len, pixels_per_line, pixels_per_grid)

    while is_running:
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            click(screen, x_len, y_len, mouse[0], mouse[1], 
                  pixels_per_line, pixels_per_grid, (0, 255, 0), event)
            
            if event.type == pygame.QUIT:
                is_running = False

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
