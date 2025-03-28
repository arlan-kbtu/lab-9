import pygame, sys
from pygame.locals import *
import random, time

pygame.init()

# Основные настройки игры
FPS = 60
FramePerSec = pygame.time.Clock()

# Цвета
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Параметры экрана
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COINS = 0  
COINS_FOR_SPEED_UP = 5  # Количество монет для увеличения скорости врага

# Шрифты
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Загрузка изображений
background = pygame.image.load("AnimatedStreet.png")
coin_image = pygame.image.load("coin.png")  

# Окно игры
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Racer with Coins")

class Enemy(pygame.sprite.Sprite):
    """Класс врага, движущегося вниз по экрану."""
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        """Движение врага вниз по экрану."""
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.bottom > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class Player(pygame.sprite.Sprite):
    """Класс игрока, управляющего машиной."""
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        """Движение игрока влево и вправо по нажатию клавиш."""
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

class Coin(pygame.sprite.Sprite):
    """Класс монеты с разной стоимостью."""
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(coin_image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(30, SCREEN_WIDTH - 30), 0)
        self.value = random.choice([1, 2, 3])  # Стоимость монеты

    def move(self):
        """Движение монеты вниз по экрану."""
        self.rect.move_ip(0, SPEED - 2)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# Создание объектов
P1 = Player()
E1 = Enemy()

# Группы спрайтов
enemies = pygame.sprite.Group()
coins = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
enemies.add(E1)

# Таймеры
INC_SPEED = pygame.USEREVENT + 1
SPAWN_COIN = pygame.USEREVENT + 2
pygame.time.set_timer(INC_SPEED, 1000)
pygame.time.set_timer(SPAWN_COIN, 1500)

while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5  # Постепенное увеличение скорости
        if event.type == SPAWN_COIN:
            coin = Coin()
            coins.add(coin)
            all_sprites.add(coin)
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Отображение фона
    DISPLAYSURF.blit(background, (0, 0))

    # Отображение очков и количества монет
    score_text = font_small.render(f"Счёт: {SCORE}", True, BLACK)
    coin_text = font_small.render(f"Монеты: {COINS}", True, BLACK)
    DISPLAYSURF.blit(score_text, (10, 10))
    DISPLAYSURF.blit(coin_text, (SCREEN_WIDTH - 120, 10))

    # Движение всех объектов
    for entity in all_sprites:
        entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)

    # Проверка на сбор монет
    collected = pygame.sprite.spritecollide(P1, coins, True)
    for coin in collected:
        COINS += coin.value  # Учитываем стоимость монеты

    # Увеличение скорости врага при наборе N монет
    if COINS >= COINS_FOR_SPEED_UP:
        SPEED += 1
        COINS = 0  # Сброс счётчика после ускорения

    # Проверка столкновения с врагом
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('crash.wav').play()
        time.sleep(1)
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))
        pygame.display.update()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    pygame.display.update()
    FramePerSec.tick(FPS)
