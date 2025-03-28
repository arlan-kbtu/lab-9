import pygame
import sys

pygame.init()

# Размеры окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint App")

# Цвета
WHITE = (255, 255, 255)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (0, 102, 204)
YELLOW = (255, 223, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
PINK = (255, 105, 180)
TEAL = (0, 128, 128)
GRAY = (240, 240, 240)

clock = pygame.time.Clock()
screen.fill(WHITE)

# Переменные
drawing = False
start_pos = None
mode = "draw"  # "draw", "rect", "circle", "square", "right_triangle", "equilateral_triangle", "rhombus", "erase"
color = DARK_BLUE
radius = 5

font = pygame.font.SysFont(None, 24)

# Кнопки интерфейса
buttons = {
    "pen": pygame.Rect(10, 10, 80, 40),
    "rect": pygame.Rect(100, 10, 80, 40),
    "circle": pygame.Rect(190, 10, 80, 40),
    "square": pygame.Rect(280, 10, 80, 40),
    "right_triangle": pygame.Rect(370, 10, 80, 40),
    "equilateral_triangle": pygame.Rect(460, 10, 80, 40),
    "rhombus": pygame.Rect(550, 10, 80, 40),
    "eraser": pygame.Rect(640, 10, 80, 40),
}

# Кнопки цветов
color_buttons = {
    "yellow": pygame.Rect(10, 60, 40, 40),
    "orange": pygame.Rect(60, 60, 40, 40),
    "purple": pygame.Rect(110, 60, 40, 40),
    "pink": pygame.Rect(160, 60, 40, 40),
    "teal": pygame.Rect(210, 60, 40, 40),
}

def draw_interface():
    """Отрисовка кнопок интерфейса."""
    for key, rect in buttons.items():
        pygame.draw.rect(screen, LIGHT_BLUE, rect, border_radius=5)
        pygame.draw.rect(screen, DARK_BLUE, rect, 2, border_radius=5)
        label = font.render(key.replace("_", " ").capitalize(), True, DARK_BLUE)
        screen.blit(label, (rect.x + 5, rect.y + 10))

    for key, rect in color_buttons.items():
        pygame.draw.rect(screen, eval(key.upper()), rect, border_radius=5)
        pygame.draw.rect(screen, DARK_BLUE, rect, 2, border_radius=5)

def handle_buttons(pos):
    """Обработка нажатий на кнопки."""
    global mode, color
    for key, rect in buttons.items():
        if rect.collidepoint(pos):
            mode = key
            return
    for key, rect in color_buttons.items():
        if rect.collidepoint(pos):
            color = eval(key.upper())

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if any(button.collidepoint(event.pos) for button in buttons.values()) or \
                   any(button.collidepoint(event.pos) for button in color_buttons.values()):
                    handle_buttons(event.pos)
                else:
                    drawing = True
                    start_pos = event.pos

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and drawing:
                end_pos = event.pos
                x1, y1 = start_pos
                x2, y2 = end_pos
                w, h = abs(x2 - x1), abs(y2 - y1)

                if mode == "rect":
                    pygame.draw.rect(screen, color, (min(x1, x2), min(y1, y2), w, h), 2)
                elif mode == "square":
                    side = min(w, h)
                    pygame.draw.rect(screen, color, (x1, y1, side, side), 2)
                elif mode == "circle":
                    radius = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)
                    pygame.draw.circle(screen, color, start_pos, radius, 2)
                elif mode == "right_triangle":
                    pygame.draw.polygon(screen, color, [(x1, y1), (x1, y2), (x2, y2)], 2)
                elif mode == "equilateral_triangle":
                    h = int((3 ** 0.5 / 2) * w)
                    pygame.draw.polygon(screen, color, [(x1, y2), (x1 + w // 2, y2 - h), (x2, y2)], 2)
                elif mode == "rhombus":
                    pygame.draw.polygon(screen, color, [(x1 + w // 2, y1), (x1, y1 + h // 2), 
                                                         (x1 + w // 2, y2), (x2, y1 + h // 2)], 2)
                drawing = False

        elif event.type == pygame.MOUSEMOTION:
            if drawing and mode == "draw":
                pygame.draw.line(screen, color, start_pos, event.pos, radius)
                start_pos = event.pos
            elif drawing and mode == "erase":
                pygame.draw.circle(screen, WHITE, event.pos, radius)

    draw_interface()
    pygame.display.update()
    clock.tick(60)
