import algo
import pygame, sys
from pygame.locals import *

# загрузка изображений иконки окна и выбора новой или последней игры
i_icon = "images\icon.png"
mode = "images\selectmode.jpg"

# функция окна игрового поля mode1()
# первый аргумент в mode1() для определения цвета камня для игрока, 0 и 1 соответственно белый и черный
# второй аргумент в mode1() для определения возможности отмены хода, 0 и 1 соответственно True и False
# третий аргумент в mode1() для определения сохраненной или новой игры, 1 и 2 соответственно новая и сохр игра
def mode1(u, enabled, s):
    undo = 1
    # чтение из файла тему игрового поля
    fread = open('info\\theme.txt', 'r')
    default = "images\\" + fread.readline()
    fread.close()
    backimg = default
    # цвет камня для игрока, 0 и 1 соответственно белый и черный
    if u == 0:
        USER = "images\\blanc.png"
        AI = "images\\noir.png"
    elif u == 1:
        USER = "images\\noir.png"
        AI = "images\\blanc.png"
    # загрузка изображений подокон вне игрового поля
    i_icon = "images\icon.png"
    EXIT = "images\exit.png"
    PANE = "images\pane.jpg"
    ABOUT = "images\\about.png"
    WIN = "images\win.png"
    LOSE = "images\lost.png"
    YOU = "images\you.png"
    ME = "images\me.png"
    UNDO = "images\disabled.png"
    AGAIN = "images\\again.png"
    NOTHING = "images\waste.png"
    # создание массивов для ходов игрока и бота
    HUMAN = []
    BOT = []
    pygame.init()
    # загрузка изображения иконки окна игры
    icon = pygame.image.load(i_icon)
    pygame.display.set_icon(icon)
    # установка экрана на разрешение 960 x 640
    screen = pygame.display.set_mode((960, 640), 0, 32)
    # загрузка изображений темы игрового поля, бокового меню и информации
    background = pygame.image.load(backimg).convert()
    pane = pygame.image.load(PANE).convert()
    about = pygame.image.load(ABOUT).convert_alpha()
    win = pygame.image.load(WIN).convert_alpha()
    lost = pygame.image.load(LOSE).convert_alpha()
    no_undo = pygame.image.load(UNDO).convert_alpha()
    user = pygame.image.load(USER).convert_alpha()
    playAgain = pygame.image.load(AGAIN).convert_alpha()
    ai = pygame.image.load(AI).convert_alpha()
    you = pygame.image.load(YOU).convert_alpha()
    me = pygame.image.load(ME).convert_alpha()
    nothing = pygame.image.load(NOTHING).convert_alpha()
    escape = pygame.image.load(EXIT).convert_alpha()
    pygame.display.set_caption('RENJU')
    # загрузка экрана игрового поля и боковой панели меню на определенные позиции
    screen.blit(background, (0, 0))
    screen.blit(pane, (640, 0))
    # загрузка кнопки "отмена хода запрещена", если выбран режим без отмены хода
    if not enabled:
        screen.blit(no_undo, (640, 25))
    # первый ход для новой игры
    if s == 1:
        if u == 0:
            count = 1
            BOT.append((300, 300))
            screen.blit(ai, (300, 300))
            screen.blit(you, (650, 400))
        elif u == 1:
            HUMAN.append((300, 300))
            screen.blit(user, (300, 300))
            screen.blit(me, (650, 400))
            count = 1
        pygame.display.update()
    # восстановление доски, если игра сохранена
    elif s == 2:
        screen.blit(you, (650, 400))
        fread = open('info\savedGame.txt', 'r')
        fread.readline()
        fread.readline()
        count = int(fread.readline())
        line = fread.readline()
        # восстановление ходов игрока
        while not (line == "BOT\n"):
            X = int(line)
            Y = int(fread.readline())
            HUMAN.append((X, Y))
            line = fread.readline()
        line = fread.readline()
        # восстановление ходов бота
        while not (line == "END\n"):
            X = int(line)
            Y = int(fread.readline())
            BOT.append((X, Y))
            line = fread.readline()
        fread.close()
        # отрисовка камней игрока
        i = 0
        while i < len(HUMAN):
            screen.blit(user, HUMAN[i])
            pygame.display.update()
            i = i + 1
        # отрисовка камней бота
        i = 0
        while i < len(BOT):
            screen.blit(ai, BOT[i])
            pygame.display.update()
            i = i + 1
    # игровой цикл
    complete = False
    while True:
        pos = [0, 0]
        # получение события клика
        for event in pygame.event.get():
            # выход из игры, когда пользователь нажимает кнопку "Закрыть"
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # работа с дисплеем, когда он свернут
            if event.type == ACTIVEEVENT or event.type == 17:
                i = 0
                while i < len(HUMAN):
                    screen.blit(user, HUMAN[i])
                    pygame.display.update()
                    i = i + 1
                i = 0
                while i < len(BOT):
                    screen.blit(ai, BOT[i])
                    pygame.display.update()
                    i = i + 1
                    # определение позиции клика игрока
            if event.type == MOUSEBUTTONDOWN:
                pos = list(event.pos)
                flag = 0
                # позиция кнопки "RENJU"
                if pos[0] > 640 and pos[0] < 960 and pos[1] > 0 and pos[1] < 23:
                    screen.blit(about, (640, 87))
                    i = 0
                    while i < len(HUMAN):
                        screen.blit(user, HUMAN[i])
                        pygame.display.update()
                        i = i + 1
                    i = 0
                    while i < len(BOT):
                        screen.blit(ai, BOT[i])
                        pygame.display.update()
                        i = i + 1
                # перезапуск текущей игры
                if pos[0] > 670 and pos[0] < 760 and pos[1] > 500 and pos[1] < 590:
                    del (HUMAN)
                    del (BOT)
                    mode1(u, enabled, 1)
                # выход в меню выбора
                if pos[0] > 790 and pos[0] < 940 and pos[1] > 400 and pos[1] < 476:
                    del (HUMAN)
                    del (BOT)
                    pygame.quit()
                    select()
                # сохранение и выход из игры
                if pos[0] > 790 and pos[0] < 940 and pos[1] > 500 and pos[1] < 590:
                    if not complete:
                        # сохранение параметров игры
                        fwrite = open('info\savedGame.txt', 'w')
                        fwrite.write(str(u) + "\n")
                        fwrite.write(str(enabled) + "\n")
                        fwrite.write(str(count) + "\n")
                        # сохранение ходов игрока
                        i = 0
                        while i < len(HUMAN):
                            a = list(HUMAN[i])
                            fwrite.writelines(str(a[0]) + "\n" + str(a[1]) + "\n")
                            i = i + 1
                        # сохранение ходов бота
                        i = 0
                        fwrite.write("BOT\n")
                        while i < len(BOT):
                            a = list(BOT[i])
                            fwrite.writelines(str(a[0]) + "\n" + str(a[1]) + "\n")
                            i = i + 1
                        fwrite.write("END\n")
                        fwrite.close()
                        pygame.quit()
                        sys.exit()
                    # выход из игры без сохранения
                    elif complete:
                        pygame.quit()
                        sys.exit()
                # отмена хода игрока за белые или черные камни
                if (count % 2 == 1 and u == 0) or (count % 2 == 0 and u == 1):
                    # позиция кнопки "отмена хода"
                    if pos[0] > 640 and pos[0] < 960 and pos[1] > 25 and pos[1] < 90 and count > 2:
                        # если отмена хода доступна и игра не завершена, то
                        if undo == 1 and not complete and enabled:
                            undo = 0
                            del (HUMAN[len(HUMAN) - 1])
                            del (BOT[len(BOT) - 1])
                            count = count - 2
                            i = 0
                            while i < len(HUMAN):
                                screen.blit(user, HUMAN[i])
                                pygame.display.update()
                                i = i + 1
                            i = 0
                            while i < len(BOT):
                                screen.blit(ai, BOT[i])
                                pygame.display.update()
                                i = i + 1
                    # ход игрока
                    if pos[0] > 20 and pos[0] < 620 and pos[1] > 20 and pos[1] < 620 and not complete:
                        flag = 1
                    # определение места (центра), в котором должны быть размещены камни
                    if flag == 1:
                        X = pos[0] - pos[0] % 40
                        if pos[0] % 40 > 40 - pos[0] % 40:
                            X = X + 40
                        X = X - 20
                        Y = pos[1] - pos[1] % 40
                        if pos[1] % 40 > 40 - pos[1] % 40:
                            Y = Y + 40
                        Y = Y - 20
                        # проверка доступности хода
                        j = 0
                        while j < len(HUMAN):
                            if X == HUMAN[j][0] and Y == HUMAN[j][1]:
                                flag = 0
                                break
                            j = j + 1
                        j = 0
                        while j < len(BOT):
                            if X == BOT[j][0] and Y == BOT[j][1]:
                                flag = 0
                                break
                            j = j + 1
                    # сохранение последнего хода
                    if flag == 1:
                        undo = 1
                        screen.blit(me, (650, 400))
                        HUMAN.append((X, Y))
                        i = 0
                        # прорисовка ходов игрока
                        while i < len(HUMAN):
                            screen.blit(user, HUMAN[i])
                            pygame.display.update()
                            i = i + 1
                        # прорисовка ходов бота
                        i = 0
                        while i < len(BOT):
                            screen.blit(ai, BOT[i])
                            pygame.display.update()
                            i = i + 1
                        # проверка пяти камней в ряд после каждого шага для игрока
                        temp = 0
                        # горизонтально
                        if (X + 40, Y) in HUMAN and (X + 80, Y) in HUMAN and (X + 120, Y) in HUMAN and (
                                X + 160, Y) in HUMAN:
                            temp = 1
                        elif (X - 40, Y) in HUMAN and (X - 80, Y) in HUMAN and (X - 120, Y) in HUMAN and (
                                X - 160, Y) in HUMAN:
                            temp = 1
                        # вертикально
                        elif (X, Y + 40) in HUMAN and (X, Y + 80) in HUMAN and (X, Y + 120) in HUMAN and (
                                X, Y + 160) in HUMAN:
                            temp = 1
                        elif (X, Y - 40) in HUMAN and (X, Y - 80) in HUMAN and (X, Y - 120) in HUMAN and (
                                X, Y - 160) in HUMAN:
                            temp = 1
                        # диагонали вниз-вправо вверх-влево
                        elif (X + 40, Y + 40) in HUMAN and (X + 80, Y + 80) in HUMAN and (
                                X + 120, Y + 120) in HUMAN and (
                                X + 160, Y + 160) in HUMAN:
                            temp = 1
                        elif (X - 40, Y - 40) in HUMAN and (X - 80, Y - 80) in HUMAN and (
                                X - 120, Y - 120) in HUMAN and (
                                X - 160, Y - 160) in HUMAN:
                            temp = 1
                        # диагональ вверх-вправо вниз-влево
                        elif (X - 40, Y + 40) in HUMAN and (X - 80, Y + 80) in HUMAN and (
                                X - 120, Y + 120) in HUMAN and (
                                X - 160, Y + 160) in HUMAN:
                            temp = 1
                        elif (X + 40, Y - 40) in HUMAN and (X + 80, Y - 80) in HUMAN and (
                                X + 120, Y - 120) in HUMAN and (
                                X + 160, Y - 160) in HUMAN:
                            temp = 1
                        # горизонтально 1 к 3, 2 к 2
                        elif (X - 40, Y) in HUMAN and (X + 40, Y) in HUMAN and (X + 80, Y) in HUMAN and (
                                X + 120, Y) in HUMAN:
                            temp = 1
                        elif (X - 80, Y) in HUMAN and (X - 40, Y) in HUMAN and (X + 40, Y) in HUMAN and (
                                X + 80, Y) in HUMAN:
                            temp = 1
                        elif (X - 120, Y) in HUMAN and (X - 80, Y) in HUMAN and (X - 40, Y) in HUMAN and (
                                X + 40, Y) in HUMAN:
                            temp = 1
                        # вертикально 1 к 3, 2 к 2
                        elif (X, Y - 40) in HUMAN and (X, Y + 40) in HUMAN and (X, Y + 80) in HUMAN and (
                                X, Y + 120) in HUMAN:
                            temp = 1
                        elif (X, Y - 80) in HUMAN and (X, Y - 40) in HUMAN and (X, Y + 40) in HUMAN and (
                                X, Y + 80) in HUMAN:
                            temp = 1
                        elif (X, Y - 120) in HUMAN and (X, Y - 80) in HUMAN and (X, Y - 40) in HUMAN and (
                                X, Y + 40) in HUMAN:
                            temp = 1
                        # диагонали вниз-вправо вверх-влево
                        elif (X - 40, Y - 40) in HUMAN and (X + 40, Y + 40) in HUMAN and (X + 80, Y + 80) in HUMAN and (
                                X + 120, Y + 120) in HUMAN:
                            temp = 1
                        elif (X - 80, Y - 80) in HUMAN and (X - 40, Y - 40) in HUMAN and (X + 40, Y + 40) in HUMAN and (
                                X + 80, Y + 80) in HUMAN:
                            temp = 1
                        elif (X - 120, Y - 120) in HUMAN and (X - 80, Y - 80) in HUMAN and (
                                X - 40, Y - 40) in HUMAN and (X + 40, Y + 40) in HUMAN:
                            temp = 1
                        # диагональ вверх-вправо вниз-влево
                        elif (X - 40, Y + 40) in HUMAN and (X + 40, Y - 40) in HUMAN and (X + 80, Y - 80) in HUMAN and (
                                X + 120, Y - 120) in HUMAN:
                            temp = 1
                        elif (X - 80, Y + 80) in HUMAN and (X - 40, Y + 40) in HUMAN and (X + 40, Y - 40) in HUMAN and (
                                X + 80, Y - 80) in HUMAN:
                            temp = 1
                        elif (X - 120, Y + 120) in HUMAN and (X - 80, Y + 80) in HUMAN and (
                                X - 40, Y + 40) in HUMAN and (
                                X + 40, Y - 40) in HUMAN:
                            temp = 1
                        # объявление победителя
                        if temp == 1:
                            screen.blit(nothing, (650, 400))
                            screen.blit(win, (640, 87))
                            screen.blit(escape, (790, 500))
                            screen.blit(playAgain, (670, 500))
                            i = 0
                            while i < len(HUMAN):
                                screen.blit(user, HUMAN[i])
                                pygame.display.update()
                                i = i + 1
                            i = 0
                            while i < len(BOT):
                                screen.blit(ai, BOT[i])
                                pygame.display.update()
                                i = i + 1
                            pygame.display.update()
                            complete = True
                        count = count + 1
            # ход бота
            if ((count % 2 == 0 and u == 0) or (count % 2 == 1 and u == 1)) and not complete:
                # алгоритм для ии
                algo.attack(BOT, HUMAN, 0, 6, -1000, 1000)
                screen.blit(you, (650, 400))
                pygame.display.update()
                i = 0
                while i < len(HUMAN):
                    screen.blit(user, HUMAN[i])
                    pygame.display.update()
                    i = i + 1
                i = 0
                while i < len(BOT):
                    screen.blit(ai, BOT[i])
                    pygame.display.update()
                    i = i + 1
                X = BOT[len(BOT) - 1][0]
                Y = BOT[len(BOT) - 1][1]
                # проверка пяти камней в ряд после каждого шага для бота
                temp = 0
                # горизонтально
                if (X + 40, Y) in BOT and (X + 80, Y) in BOT and (X + 120, Y) in BOT and (X + 160, Y) in BOT:
                    temp = 1
                elif (X - 40, Y) in BOT and (X - 80, Y) in BOT and (X - 120, Y) in BOT and (X - 160, Y) in BOT:
                    temp = 1
                # вертикально
                elif (X, Y + 40) in BOT and (X, Y + 80) in BOT and (X, Y + 120) in BOT and (X, Y + 160) in BOT:
                    temp = 1
                elif (X, Y - 40) in BOT and (X, Y - 80) in BOT and (X, Y - 120) in BOT and (X, Y - 160) in BOT:
                    temp = 1
                # диагонали вниз-вправо вверх-влево
                elif (X + 40, Y + 40) in BOT and (X + 80, Y + 80) in BOT and (X + 120, Y + 120) in BOT and (
                        X + 160, Y + 160) in BOT:
                    temp = 1
                elif (X - 40, Y - 40) in BOT and (X - 80, Y - 80) in BOT and (X - 120, Y - 120) in BOT and (
                        X - 160, Y - 160) in BOT:
                    temp = 1
                # диагональ вверх-вправо вниз-влево
                elif (X - 40, Y + 40) in BOT and (X - 80, Y + 80) in BOT and (X - 120, Y + 120) in BOT and (
                        X - 160, Y + 160) in BOT:
                    temp = 1
                elif (X + 40, Y - 40) in BOT and (X + 80, Y - 80) in BOT and (X + 120, Y - 120) in BOT and (
                        X + 160, Y - 160) in BOT:
                    temp = 1
                # горизонтально 1к3 и 2к2
                elif (X - 40, Y) in BOT and (X + 40, Y) in BOT and (X + 80, Y) in BOT and (X + 120, Y) in BOT:
                    temp = 1
                elif (X - 80, Y) in BOT and (X - 40, Y) in BOT and (X + 40, Y) in BOT and (X + 80, Y) in BOT:
                    temp = 1
                elif (X - 120, Y) in BOT and (X - 80, Y) in BOT and (X - 40, Y) in BOT and (X + 40, Y) in BOT:
                    temp = 1
                # # вертикально 1к3 и 2к2
                elif (X, Y - 40) in BOT and (X, Y + 40) in BOT and (X, Y + 80) in BOT and (X, Y + 120) in BOT:
                    temp = 1
                elif (X, Y - 80) in BOT and (X, Y - 40) in BOT and (X, Y + 40) in BOT and (X, Y + 80) in BOT:
                    temp = 1
                elif (X, Y - 120) in BOT and (X, Y - 80) in BOT and (X, Y - 40) in BOT and (X, Y + 40) in BOT:
                    temp = 1
                # диагонали вниз-вправо вверх-влево
                elif (X - 40, Y - 40) in BOT and (X + 40, Y + 40) in BOT and (X + 80, Y + 80) in BOT and (
                        X + 120, Y + 120) in BOT:
                    temp = 1
                elif (X - 80, Y - 80) in BOT and (X - 40, Y - 40) in BOT and (X + 40, Y + 40) in BOT and (
                        X + 80, Y + 80) in BOT:
                    temp = 1
                elif (X - 120, Y - 120) in BOT and (X - 80, Y - 80) in BOT and (X - 40, Y - 40) in BOT and (
                        X + 40, Y + 40) in BOT:
                    temp = 1
                # диагональ вверх-вправо вниз-влево
                elif (X - 40, Y + 40) in BOT and (X + 40, Y - 40) in BOT and (X + 80, Y - 80) in BOT and (
                        X + 120, Y - 120) in BOT:
                    temp = 1
                elif (X - 80, Y + 80) in BOT and (X - 40, Y + 40) in BOT and (X + 40, Y - 40) in BOT and (
                        X + 80, Y - 80) in BOT:
                    temp = 1
                elif (X - 120, Y + 120) in BOT and (X - 80, Y + 80) in BOT and (X - 40, Y + 40) in BOT and (
                        X + 40, Y - 40) in BOT:
                    temp = 1
                # объявление победителя бота
                if temp == 1:
                    screen.blit(nothing, (650, 400))
                    screen.blit(lost, (640, 87))
                    screen.blit(escape, (790, 500))
                    screen.blit(playAgain, (670, 500))
                    i = 0
                    while i < len(HUMAN):
                        screen.blit(user, HUMAN[i])
                        pygame.display.update()
                        i = i + 1
                    i = 0
                    while i < len(BOT):
                        screen.blit(ai, BOT[i])
                        pygame.display.update()
                        i = i + 1
                    pygame.display.update()
                    complete = True
                count = count + 1
        screen.blit(background, (0, 0))

# окно выбора параметров игры
def select():
    user = 0
    undo = 0
    pygame.init()
    OPTIONS = "images\select.png"
    WINDOW1 = pygame.display.set_mode((660, 390))
    pygame.display.set_caption("RENJU")
    icon = pygame.image.load(i_icon)
    options = pygame.image.load(OPTIONS).convert_alpha()
    WINDOW1.blit(options, (0, 0))
    pygame.display.set_icon(icon)
    while True:
        pos = [0, 0]
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                pos = list(event.pos)
                # выбор цвета камня
                if pos[1] < 318 and pos[1] > 0:
                    if pos[0] < 330 and pos[0] > 0:
                        user = 1
                    if pos[0] < 660 and pos[0] > 330:
                        user = 0
                if pos[1] < 360 and pos[1] > 318:
                    # начать игру
                    if pos[0] < 660 and pos[0] > 440:
                        pygame.quit()
                        mode1(user, undo, 1)
                    # возможность отмены хода
                    if pos[0] < 440 and pos[0] > 220:
                        undo = 1
                    # смена темы игрового поля
                    if pos[0] < 220 and pos[0] > 0:
                        fread = open('info\\theme.txt', 'r')
                        prev = fread.readline()
                        fread.close()
                        img = list(prev)
                        img[4] = str((int(img[4]) + 1) % 7)
                        fwrite = open('info\\theme.txt', 'w')
                        i = 0
                        while i < len(img):
                            fwrite.writelines(img[i])
                            i = i + 1
                        fwrite.close()
        pygame.display.update()

# инициализация игры
def play_init():
    i_icon = "images\icon.png"
    mode = "images\selectmode.jpg"
    pygame.init()
    WINDOW1 = pygame.display.set_mode((660, 390))
    pygame.display.set_caption("RENJU")
    icon = pygame.image.load(i_icon)
    background = pygame.image.load(mode).convert()
    WINDOW1.blit(background, (0, 0))
    pygame.display.set_icon(icon)
    while True:
        pos = [0, 0]
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                pos = list(event.pos)
                # новая игра
                if pos[1] < 370 and pos[1] > 20:
                    if pos[0] < 320 and pos[0] > 20:
                        select()
                # возобновить последнюю сохраненную игру
                if pos[0] > 340 and pos[0] < 660 and pos[1] > 0 and pos[1] < 100:
                    fread = open('info\savedGame.txt', 'r')
                    u = int(fread.readline())
                    e = int(fread.readline())
                    fread.close()
                    mode1(u, e, 2)
        pygame.display.update()