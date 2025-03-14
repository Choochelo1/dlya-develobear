import pygame
import random

# Инициализация Pygame
pygame.init()

# Настройки экрана
width_display = 1420
hight_display = 780

screen = pygame.display.set_mode((width_display, hight_display))

# Цвета
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

block = 20

# Начальные позиции игроков
x, y = 300, 390  
x1, y1 = 1120, 390  

# Списки для хранения следов
player1_trail = []
player2_trail = []

# Максимальная длина следов
max_trail_length = 100

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
            self.rect.x -= block
        if keys[pygame.K_RIGHT]:
            self.rect.x += block
        if keys[pygame.K_UP]:
            self.rect.y -= block
        if keys[pygame.K_DOWN]:
            self.rect.y += block

        # Добавляем текущую позицию в след
        player1_trail.append(self.rect.center)
        if len(player1_trail) > max_trail_length:
            player1_trail.pop(0)  # Убираем самый старый след

# Класс для создания второго объекта
class Player2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))  # Размер объекта
        self.image.fill(GREEN)  # Цвет объекта
        self.rect = self.image.get_rect()  # Получаем прямоугольник для объекта
        self.rect.center = (x1, y1)  # Начальная позиция объекта

    def update(self):
        # Логика движения второго игрока с контролем с помощью клавиш
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= block
        if keys[pygame.K_d]:
            self.rect.x += block
        if keys[pygame.K_w]:
            self.rect.y -= block
        if keys[pygame.K_s]:
            self.rect.y += block

        # Добавляем текущую позицию в след
        player2_trail.append(self.rect.center)
        if len(player2_trail) > max_trail_length:
            player2_trail.pop(0)  # Убираем самый старый след

# Функция для перезапуска игры
def reset_game():
    global player1_trail, player2_trail, player, player2, x, y, x1, y1, running
    # Сброс состояния игры
    player1_trail = []
    player2_trail = []
    x, y = 300, 390  
    x1, y1 = 1120, 390
    all_sprites.empty()
    player = Player()  # Инициализация первого игрока
    player2 = Player2()  # Инициализация второго игрока
    all_sprites.add(player)
    all_sprites.add(player2)
    running = True


# Функция для проверки проигрыша
def check_loose(x, y, x1, y1, player1_trail, player2_trail):
    # Проверяем столкновение с границами
    if x >= width_display or x <= 0 or y >= hight_display or y <= 0 or x1 >= width_display or x1 <= 0 or y1 >= hight_display or y1 <= 0:
        return False, "Игра завершена! Один из игроков вышел за пределы экрана."

    # Проверка на пересечение следов
    for trail_x, trail_y in player1_trail:
        if (x1 == trail_x and y1 == trail_y):
            return False, "Игрок 2 проиграл!"

    for trail_x, trail_y in player2_trail:
        if (x == trail_x and y == trail_y):
            return False, "Игрок 1 проиграл!"

    return True, ""

# Создаем объекты игроков
player = Player()
player2 = Player2()

# Группа спрайтов для обновления
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(player2)

running = True
winner_text = ""

# Главный игровой цикл
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()  # Если закрывается окно (крестик), выходим из игры

    # Обновляем состояние объектов
    player.update()  # обновляем первого игрока
    player2.update()  # обновляем второго игрока

    # Получаем текущие координаты
    x, y = player.rect.center
    x1, y1 = player2.rect.center

    # Проверяем, не вышел ли объект за пределы экрана или не столкнулись ли игроки
    running, winner_text = check_loose(x, y, x1, y1, player1_trail, player2_trail)
    if not running:
        print(winner_text)

        # Отображаем надпись о проигравшем
        font = pygame.font.Font(None, 36)
        text = font.render(winner_text, True, (255, 255, 255))
        screen.fill(BLACK)
        screen.blit(text, (width_display // 2 - text.get_width() // 2, hight_display // 2 - text.get_height() // 2))
        pygame.display.flip()

        # Ожидаем нажатие клавиши для перезапуска игры
        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting_for_input = False
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Перезапуск при нажатии R
                        reset_game()
                        waiting_for_input = False
                    elif event.key == pygame.K_q:  # Выход из игры при нажатии Q
                        waiting_for_input = False
                        running = False

    # Рисуем фон
    screen.fill(BLACK)

    # Рисуем следы за игроками
    for trail_x, trail_y in player1_trail:
        pygame.draw.circle(screen, RED, (trail_x, trail_y), 5)

    for trail_x, trail_y in player2_trail:
        pygame.draw.circle(screen, GREEN, (trail_x, trail_y), 5)

    # Отображаем объекты на экране
    all_sprites.draw(screen)

    # Обновляем экран
    pygame.display.flip()

    # Ограничиваем частоту кадров
    pygame.time.Clock().tick(10)


