import pygame
import sys

pygame.init()
pygame.display.set_caption("Tractor")  # Название игры
pygame.display.set_icon(pygame.image.load('images/tractor_icon.png'))  # Иконка игры
width, height = 980, 700  # Размеры окна
screen = pygame.display.set_mode((width, height))  # Создаем screen, чтобы обращаться к нему для отрисовки на нем
# объектов

# Отображение трактора в зависимости от направления движения
tracImage = pygame.image.load("images\\trac-left.png")
tracLeft = pygame.image.load("images\\trac-left.png")
tracRight = pygame.image.load("images\\trac-right.png")
tracUp = pygame.image.load("images\\trac-up.png")
tracDown = pygame.image.load("images\\trac-down.png")

x, y = width // 2, height // 2  # Начальные координаты трактора
trac_speed = 5  # Скорость трактора
distanceTractorToBorder = 0  # Расстояние трактора от границы

BROWN = (174, 123, 48)  # Цвет поля после вспашки
YELLOW = (207, 232, 46)  # Цвет поля до вспашки

tracObject = pygame.Rect(x, y, 10, 10)  # Объект трактора, поверх которого накладываем картинку трактора
colorField = YELLOW  # Исходный цвет поля до вспашки
colorField1 = YELLOW  # Исходный цвет поля до вспашки
colorField2 = YELLOW  # Исходный цвет поля до вспашки
colorField3 = YELLOW  # Исходный цвет поля до вспашки
colorField4 = YELLOW  # Исходный цвет поля до вспашки
colorField5 = YELLOW  # Исходный цвет поля до вспашки

# Поля для вспашки
field = pygame.Rect(200, 200, 25, 25)  # Поле
field1 = pygame.Rect(225, 200, 25, 25)  # Поле
field2 = pygame.Rect(250, 200, 25, 25)  # Поле
field3 = pygame.Rect(200, 225, 25, 25)  # Поле
field4 = pygame.Rect(225, 225, 25, 25)  # Поле
field5 = pygame.Rect(250, 225, 25, 25)  # Поле


running = True

while running:
    pygame.display.update()
    pygame.time.delay(50)
    screen.fill((35, 223, 41))

    # Движение трактора. В elif мы указываем, как будет двигаться трактор рядом с границей
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and x - trac_speed > 25:
        tracImage = tracLeft
        x -= trac_speed
    elif keys[pygame.K_LEFT]:
        tracImage = tracLeft
        distanceTractorToBorder = x - 25
        x = x - distanceTractorToBorder
    if keys[pygame.K_RIGHT] and x + trac_speed < width - 25:
        tracImage = tracRight
        x += trac_speed
    elif keys[pygame.K_RIGHT] and x < width:
        tracImage = tracRight
        distanceTractorToBorder = width - 25 - 1 - x
        x = x + distanceTractorToBorder
    if keys[pygame.K_UP] and y - trac_speed > 25:
        y -= trac_speed
        tracImage = tracUp
    elif keys[pygame.K_UP]:
        tracImage = tracUp
        distanceTractorToBorder = y - 25
        y = y - distanceTractorToBorder
    if keys[pygame.K_DOWN] and y + trac_speed < height - 25:
        tracImage = tracDown
        y += trac_speed
    elif keys[pygame.K_DOWN]:
        tracImage = tracDown
        distanceTractorToBorder = height - 25 - 1 - y
        y = y + distanceTractorToBorder

    tracObject.x = x  # Меняем координаты трактора по x
    tracObject.y = y  # Меняем координаты трактора по y

    # Проверяем, наехал ли трактор на поле или нет
    if tracObject.colliderect(field):
        colorField = BROWN
    if tracObject.colliderect(field1):
        colorField1 = BROWN
    if tracObject.colliderect(field2):
        colorField2 = BROWN
    if tracObject.colliderect(field3):
        colorField3 = BROWN
    if tracObject.colliderect(field4):
        colorField4 = BROWN
    if tracObject.colliderect(field5):
        colorField5 = BROWN

    # pygame.draw.rect(screen, color2, rect1) # можно раскомментировать, чтобы посмотреть физический объект трактора
    pygame.draw.rect(screen, colorField, field)  # отрисовка поля
    pygame.draw.rect(screen, colorField1, field1)  # отрисовка поля
    pygame.draw.rect(screen, colorField2, field2)  # отрисовка поля
    pygame.draw.rect(screen, colorField3, field3)  # отрисовка поля
    pygame.draw.rect(screen, colorField4, field4)  # отрисовка поля
    pygame.draw.rect(screen, colorField5, field5)  # отрисовка поля
    screen.blit(tracImage, (x, y))  # отрисовка картинки трактора

    # Корректное завершение программы
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
