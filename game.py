import pygame
import random

# Инициализация Pygame
pygame.init()

# Настройки экрана
width_display = 720
hight_display = 480

screen = pygame.display.set_mode((width_display, hight_display))

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)

block = 10

x, y = 400, 300  # начальная позиция первого игрока
x1, y1 = 480, 0  # начальная позиция второго игрока

# Класс для создания первого объекта
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))  # Размер объекта
        self.image.fill(RED)  # Цвет объекта
        self.rect = self.image.get_rect()  # Получаем прямоугольник для объекта
        self.rect.center = (x, y)  # Начальная позиция объекта

    def update(self):
        # Логика движения объекта (в данном случае - клавиши W, A, S, D)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 10
        if keys[pygame.K_RIGHT]:
            self.rect.x += 10
        if keys[pygame.K_UP]:
            self.rect.y -= 10
        if keys[pygame.K_DOWN]:
            self.rect.y += 10

# Класс для создания второго объекта
class Player2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))  # Размер объекта
        self.image.fill(RED)  # Цвет объекта
        self.rect = self.image.get_rect()  # Получаем прямоугольник для объекта
        self.rect.center = (x1, y1)  # Начальная позиция объекта
        self.direction = random.randint(0, 3)  # Направление движения (0, 1, 2, 3)

    def update(self):
        global x1, y1
        # Обновление координат второго игрока в зависимости от направления
        if self.direction == 0:
            y1 += block  # Вниз
        if self.direction == 1:
            y1 -= block  # Вверх
        if self.direction == 2:
            x1 += block  # Вправо
        if self.direction == 3:
            x1 -= block  # Влево

        # Обновляем позицию объекта
        self.rect.center = (x1, y1)

        # Если второй игрок выходит за пределы экрана, меняем направление
        if x1 >= width_display or x1 <= 0 or y1 >= hight_display or y1 <= 0:
            self.direction = random.randint(0, 3)  # Случайное новое направление
            # Перемещаем объект в центр
            x1, y1 = width_display // 2, hight_display // 2
            self.rect.center = (x1, y1)

# Создаем объекты игроков
player = Player()
player2 = Player2()

running = True

def check_loose(x, y):
    if x >= width_display or x <= 0 or y >= hight_display or y <= 0:
        return False  # Игра закончена
    return True  # Игра продолжается

# Группа спрайтов для обновления
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(player2)

# Главный игровой цикл
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обновляем состояние объектов
    player.update()  # обновляем первого игрока
    player2.update()  # обновляем второго игрока

    # Получаем текущие координаты
    x, y = player.rect.center
    x1, y1 = player2.rect.center

    # Проверяем, не вышел ли объект за пределы экрана
    running = check_loose(x, y)
    if not running:
        print("Игра окончена!")
        break

    # Рисуем фон
    screen.fill(WHITE)

    # Отображаем объекты на экране
    all_sprites.draw(screen)

    # Обновляем экран
    pygame.display.flip()

    # Ограничиваем частоту кадров
    pygame.time.Clock().tick(10)

# Закрытие Pygame
pygame.quit()
