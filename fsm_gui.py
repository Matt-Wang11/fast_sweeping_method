import pygame

# figure out mouse click and get coordinate of the box for clicking
# Implement pygame.time.get_ticks() to time program and space out the path advancement
class FSM_GUI:

    def __init__(self, x_len, y_len, pixels_per_grid, pixels_per_line) -> None:
        self.x = x_len
        self.y = y_len
        self.p_g = pixels_per_grid
        self.p_l = pixels_per_line

    def draw_rectangles(self, s, c=(255, 255, 255)):
        for i in range(self.x):
            for j in range(self.y):
                pygame.draw.rect(surface=s, color=c,
                                rect=pygame.Rect(self.__get_edge(i), 
                                                 self.__get_edge(j), 
                                                 self.p_g, self.p_g))

    def is_in_rectangle(self, mouse_x, mouse_y, left, top, right, down):
        return mouse_x > left and mouse_x < right and \
            mouse_y > top and mouse_y < down

    def rectangle_clicked(self, mouse_x, mouse_y, left, top, event):
        return self.is_in_rectangle(mouse_x, mouse_y, left, top, left + self.p_g, top + self.p_g)\
        and event.type == pygame.MOUSEBUTTONDOWN

    def click(self, s, mouse_x, mouse_y, c, event):
        coordinates = list

        for i in range(self.x):
            for j in range(self.y):
                left = self.__get_edge(i)
                top = self.__get_edge(j)

                if self.rectangle_clicked(mouse_x, mouse_y, left, top, event):
                    pygame.draw.rect(surface=s, color=c, 
                                    rect=pygame.Rect(left, top, self.p_g, self.p_g))
                    coordinates = [i, j]
                    break;
        
        return coordinates

    def run(self):
        pygame.init()

        screen = pygame.display.set_mode(
            [self.x * self.p_g + (self.x + 1) * self.p_l,
            self.y * self.p_g + (self.y + 1) * self.p_l])

        is_running = True
        self.draw_rectangles(screen)

        while is_running:
            mouse = pygame.mouse.get_pos()

            for event in pygame.event.get():
                self.click(screen, mouse[0], mouse[1], (0, 255, 0), event)
                
                if event.type == pygame.QUIT:
                    is_running = False

            pygame.display.flip()

        pygame.quit()

    def __get_edge(self, n):
        return self.p_l + (n * self.p_l) + (n * self.p_g)


if __name__ == "__main__":
    app = FSM_GUI(50, 50, 10, 1)
    app.run()
