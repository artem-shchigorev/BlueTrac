import pygame
import sys
import random
from button import ImageButton

pygame.init()
pygame.display.set_caption("Tractor")  # Название игры
pygame.display.set_icon(pygame.image.load('images/tractor_icon.png'))  # Иконка игры
width, height = 1000, 700  # Размеры окна
screen = pygame.display.set_mode((width, height))  # Создаем screen, чтобы обращаться к нему для отрисовки на нем
# объектов

# Картинки для отображения трактора в зависимости от направления движения
tracImage = pygame.image.load("images\\trac-down.png")  # Начальное отображение трактора
tracLeft = pygame.image.load("images\\trac-left.png")
tracRight = pygame.image.load("images\\trac-right.png")
tracUp = pygame.image.load("images\\trac-up.png")
tracDown = pygame.image.load("images\\trac-down.png")
# Картинки для полей и камней
fieldImage = pygame.image.load("images\\field_image.png")
plowedFieldImage = pygame.image.load("images\\plowed.png")
rockImage = pygame.image.load("images\\rock.png")

trac_background = pygame.image.load("images\\red_tractor_icon.png")

bear = pygame.image.load("images\\bear.jpg")  # Загружаем и масштабируем картинку медведя
bearImage = pygame.transform.scale(bear, (40, 40))
bearObject = pygame.Rect(400, 350, 40, 40)

x, y = 950, 650  # Начальные координаты трактора
trac_speed = 5  # Скорость трактора
distanceTractorToBorder = 0  # Расстояние трактора от границы
tracObject = pygame.Rect(x, y, 25, 25)  # Объект трактора, поверх которого накладываем картинку трактора
statusTrac = True  # Состояние трактора (поломан или цел)

bearX, bearY = 400, 350  # Начальные координаты медведя
bX, bY = 400, 350  # Изменения координат медведя
bearSpeed = 10  # Скорость медведя
bearSpeedY = 10  # Скорость медведя по y
bear_is_on_field = 0  # Медведь на поле или нет

# Поля для вспашки
YELLOW = (207, 232, 46)  # Цвет поля до вспашки
GRAY = (154, 140, 140)
fieldList = [None] * 140  # Создаем лист с участками невспаханных полей
a = 200  # координаты невспаханного поля
b = 200
# В этом цикле создаем ячейки с невспаханными полями и добавляем их в список
for i in range(0, 140):
    fieldList[i] = pygame.Rect(a, b, 25, 25)
    b += 25
    if b == 450:
        b = 200
        a += 25

rockList = [None] * 18  # Создаем лист с камнями
a = 0  # координаты камней
min_val = 70  # Минимальное и максимальное значение координаты y для камней
max_val = 675
for i in range(0, 18):  # В этом цикле создаем камни по всей карте в рандомных местах
    rockList[i] = pygame.Rect(a, random.randint(min_val, max_val), 20, 20)
    a += 50

plowed_field = pygame.Rect(200, 200, 350, 250)  # Вспаханное поле

pointsScored = 0  # Счетчик вспаханных полей
font = pygame.font.Font(None, 36)  # Шрифт счетчика

# Создание кнопки
start_button = ImageButton(width/2-(128/2), height/2, 128, 64, "PLAY", "images\\buttons\\button_for_meny.png", "", "")
exit_button = ImageButton(width/2-(128/2), height/2+70, 128, 64, "EXIT", "images\\buttons\\button_for_meny.png", "", "")
screen.blit(trac_background, (0, -150))
menu = True
while menu:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or statusTrac == False:
            pygame.quit()
            sys.exit()
    pygame.display.update()  # обновление экрана
    start_button.check_hover(pygame.mouse.get_pos())
    menu = start_button.handle_event(event)
    start_button.draw(screen)
    exit_button.check_hover(pygame.mouse.get_pos())
    statusTrac = exit_button.handle_event(event)
    exit_button.draw(screen)


running = True
while running:
    pygame.display.update()  # обновление экрана
    pygame.time.delay(60)  # частота обновления
    screen.fill((35, 223, 41))  # заливка фона

    # Как только мы наберем 140 очков или сломаем трактор, игра закончится
    if pointsScored != 140 and statusTrac == True and not tracObject.colliderect(bearObject):

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

        # Проверяем, наехал ли трактор на поле или нет
        if tracObject.colliderect(
                plowed_field):  # Цикл ниже крутится только тогда, когда трактор находится в зоне вспашки
            for i in range(0, len(fieldList)):
                if tracObject.colliderect(fieldList[i]):  # Условие выполняется, если трактор наехал на поле
                    fieldList.pop(i)  # удаляем поле из листа с вспаханными полями
                    pointsScored += 1
                    break

        screen.blit(plowedFieldImage, (200, 200))  # отрисовка вспаханного поля

        for i in range(0, len(fieldList)):
            pygame.draw.rect(screen, YELLOW, fieldList[i])  # Рисуем невспаханные поля
            screen.blit(fieldImage, (fieldList[i].x, fieldList[i].y))
        for i in range(0, len(rockList)):
            screen.blit(rockImage, (rockList[i].x, rockList[i].y))
            if tracObject.colliderect(rockList[i]):
                statusTrac = False

        if abs(bearX - bX) < 10 and bearObject.colliderect(plowed_field) and bear_is_on_field == 0:
            bX = bearX + random.choice([-30, 30])
            bY = bearY + random.choice([-30, 30])
            if (bearX - bX) < 0:
                bearSpeed = 3
            else:
                bearSpeed = -3
            if (bearY - bY) < 0:
                bearSpeedY = 3
            else:
                bearSpeedY = -3
            screen.blit(bearImage, (bearX, bearY))
            bearObject.x = bearX
            bearObject.y = bearY
        elif not bearObject.colliderect(plowed_field) or bear_is_on_field != 0:
            bear_is_on_field += 1
            if bearObject.x >= 450:
                bearX = bearObject.x - 9
                bearObject.x = bearX
            else:
                bearX = bearObject.x + 9
                bearObject.x = bearX
            if bearObject.y >= 350:
                bearY = bearObject.y - 9
                bearObject.y = bearY
            else:
                bearY = bearObject.y + 9
                bearObject.y = bearY
            if bear_is_on_field == 4:
                bear_is_on_field = 0
                bX = bearObject.x
                bY = bearObject.y
            screen.blit(bearImage, (bearObject.x, bearObject.y))
        else:
            bearX = bearX + bearSpeed
            bearY = bearY + bearSpeedY
            screen.blit(bearImage, (bearX, bearY))
            bearObject.x = bearX
            bearObject.y = bearY

        # pygame.draw.rect(screen, YELLOW, tracObject) # можно раскомментировать, чтобы посмотреть физ. объект трактора
        tracObject.x = x  # Меняем координаты трактора по x
        tracObject.y = y  # Меняем координаты трактора по y
        screen.blit(tracImage, (x, y))  # отрисовка картинки трактора
        text = font.render(f"Score: {pointsScored}/140  НЕ НАЕЗЖАЙТЕ НА КАМНИ!!! ОПАСНО МЕДВЕДИ!!! 1 демо уровень",
                           True, (255, 255, 255))  # текст со счетчиком
        screen.blit(text, (10, 10))  # отображение счетчика
    else:
        if tracObject.colliderect(bearObject):
            bearSpeed = 0
            text = font.render(f"Вас съел медведь!", True, (255, 255, 255))  # текст со счетчиком
            screen.blit(text, (350, 320))  # отображение счетчика
            exit_button.check_hover(pygame.mouse.get_pos())
            running = exit_button.handle_event(event)
            exit_button.draw(screen)
        elif statusTrac == True:  # если все поля вспахали и трактор не сломал, мы побеждаем
            text = font.render(f"Вы вспахали все поле!", True, (255, 255, 255))  # текст со счетчиком
            screen.blit(text, (350, 320))  # отображение счетчика
            exit_button.check_hover(pygame.mouse.get_pos())
            running = exit_button.handle_event(event)
            exit_button.draw(screen)

        else:
            text = font.render(f"Вы наехали на камень и сломали трактор!", True, (255, 255, 255))  # текст со счетчиком
            screen.blit(text, (300, 320))  # отображение счетчика
            exit_button.check_hover(pygame.mouse.get_pos())
            running = exit_button.handle_event(event)
            exit_button.draw(screen)

    # Корректное завершение программы
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
