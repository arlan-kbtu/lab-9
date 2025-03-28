import pygame
import random

# Цвета
BLUE = (50, 153, 213)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

# Параметры экрана
DIS_WIDTH = 600
DIS_HEIGHT = 400
SNAKE_BLOCK = 10

pygame.init()
display = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
pygame.display.set_caption("Snake Game with Timed Food")
clock = pygame.time.Clock()

font_style = pygame.font.SysFont("Verdana", 20)

def print_snake(snake_list):
    """Отображает змейку на экране."""
    for x in snake_list:
        pygame.draw.rect(display, BLACK, [x[0], x[1], SNAKE_BLOCK, SNAKE_BLOCK])

def show_score(score, level):
    """Отображает счет и уровень."""
    value = font_style.render(f"Score: {score}  Level: {level}", True, WHITE)
    display.blit(value, [10, 10])

def generate_food(snake_list):
    """Создает новую еду в случайной позиции, учитывая змейку."""
    while True:
        food_x = round(random.randrange(0, DIS_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
        food_y = round(random.randrange(0, DIS_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0
        if [food_x, food_y] not in snake_list:
            return food_x, food_y, random.choice([1, 2, 3])  # Разные веса еды (1, 2 или 3 очка)

def main():
    game_over = False
    x1 = DIS_WIDTH / 2
    y1 = DIS_HEIGHT / 2
    x1_change = 0
    y1_change = 0

    snake_list = []
    snake_length = 1
    score = 0
    level = 1
    speed = 10

    # Начальные параметры еды
    food_x, food_y, food_value = generate_food(snake_list)
    food_timer = pygame.time.get_ticks()  # Время появления еды

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -SNAKE_BLOCK
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = SNAKE_BLOCK
                    x1_change = 0

        # Проверка на выход за границы экрана
        if x1 >= DIS_WIDTH or x1 < 0 or y1 >= DIS_HEIGHT or y1 < 0:
            game_over = True

        # Движение змейки
        x1 += x1_change
        y1 += y1_change

        # Очистка экрана
        display.fill(BLUE)

        # Проверка таймера еды (исчезает через 5 секунд)
        if pygame.time.get_ticks() - food_timer > 5000:
            food_x, food_y, food_value = generate_food(snake_list)
            food_timer = pygame.time.get_ticks()  # Обновление таймера

        # Отображение еды
        pygame.draw.rect(display, RED, [food_x, food_y, SNAKE_BLOCK, SNAKE_BLOCK])

        # Проверка столкновения змейки с самой собой
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        for block in snake_list[:-1]:
            if block == snake_head:
                game_over = True

        print_snake(snake_list)
        show_score(score, level)
        pygame.display.update()

        # Проверка съедания еды
        if x1 == food_x and y1 == food_y:
            food_x, food_y, food_value = generate_food(snake_list)
            food_timer = pygame.time.get_ticks()  # Сброс таймера еды
            snake_length += 1
            score += food_value  # Добавление очков в зависимости от "веса" еды
            if score % 5 == 0:  # Каждые 5 очков повышаем уровень
                level += 1
                speed += 2

        clock.tick(speed)

    pygame.quit()

main()
