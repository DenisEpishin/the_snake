import pygame
import random

# Константы для размеров поля и сетки
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20  # Размер одной клетки сетки
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE  # Количество клеток по ширине
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE  # Количество клеток по высоте

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка - Рекорд: 0')  # Изначально рекорд 0

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, x=0, y=0, color=BOARD_BACKGROUND_COLOR):
        self.position = (x, y)
        self.body_color = color

    def draw(self):
        """Метод должен быть переопределен в дочерних классах."""
        pass


class Apple(GameObject):
    """Класс, описывающий яблоко."""

    def __init__(self, snake_positions=(0, 0)):
        self.body_color = APPLE_COLOR
        self.randomize_position(snake_positions)

    def randomize_position(self, snake_positions):
        """Случайное размещение яблока на поле, исключая"""
        """размещения на змейке."""
        while True:
            self.position = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if self.position not in snake_positions:
                break

    def draw(self):
        """Отрисовка яблока на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, представляющий змейку."""

    def __init__(self):
        self.positions = [(GRID_SIZE, GRID_SIZE)]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.length = 2
        self.position = (0, 0)

    def update_direction(self):
        """Обновление направления движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Перемещение змейки в текущем направлении."""
        self.update_direction()
        head_x, head_y = self.get_head_position()
        new_head = (head_x + self.direction[0] * GRID_SIZE,
                    head_y + self.direction[1] * GRID_SIZE)

        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        """Отрисовка змейки на экране."""
        # Отрисовка всех сегментов, кроме головы
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Прямоугольник для головы
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)  # Рисуем голову
        # Рисуем границу головы
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает состояние змейки."""
        self.positions = [(GRID_SIZE, GRID_SIZE)]
        self.direction = RIGHT
        self.length = 1


def handle_keys(snake):
    """Обработка нажатий клавиш для управления змейкой."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Завершение игры при нажатии ESC
                pygame.quit()
                exit()
            elif event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main():
    """Основная функция игры."""
    pygame.init()

    snake = Snake()
    apple = Apple(snake.positions)

    high_score = 0  # Переменная для рекорда

    while True:
        clock.tick(SPEED)  # Ограничение скорости игры
        handle_keys(snake)  # Обработка нажатий клавиш
        snake.move()

        # Проверка на столкновение со стенами (появление с другой стороны)
        head_x, head_y = snake.get_head_position()  # Получение позиции головы
        if head_x < 0:
            head_x = SCREEN_WIDTH - GRID_SIZE
        elif head_x >= SCREEN_WIDTH:
            head_x = 0
        if head_y < 0:
            head_y = SCREEN_HEIGHT - GRID_SIZE
        elif head_y >= SCREEN_HEIGHT:
            head_y = 0
        snake.positions[0] = (head_x, head_y)  # Обновление позиции головы

        # Проверка на столкновение с яблоком
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

            # Обновление рекорда
            if snake.length > high_score:
                high_score = snake.length
                # Обновление заголовка
                pygame.display.set_caption(f'Змейка - Рекорд: {high_score}')

        # Проверка на столкновение с собой
        if snake.positions[0] in snake.positions[1:]:
            snake.reset()  # Сброс змейки

        # Отрисовка
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
