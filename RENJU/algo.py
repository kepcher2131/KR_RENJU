# функция реализует минимаксный алгоритм
def attack(player, otherplayer, depth, maxdepth, A, B):
    a = [] # обновляем списки
    b = []
    # проверка победы бота и достижения макс глубины поиска ходов
    if isgameover(player) or depth == maxdepth:
        e = evaluate(player, otherplayer) # возврат оценки эффективности хода
        return e
    # лучшие значения координаты и оценки эффективности хода
    bestmove = None
    bestscore = -1000
    move = getmoves(player, otherplayer) # получение координат лучшего хода
    for m in move:
        a = player+[(m)] # записываем координаты искомого хода в список ходов бота
        b = otherplayer+[] # записываем пустые координаты хода игрока
        score = attack(b, a, depth+1, maxdepth, -B, -max(A, bestscore)) # рекурсивно вызываем функцию
        score = -score
        if score > bestscore: # если лучшее значение < текущего
            bestscore = score # присваиваем текущее лучшему
            bestmove = m # ход становится лучшим
            if bestscore >= B: # альфа-бета отсечение
                return bestscore
    if depth == 0: # если ход бота
        player.append((bestmove)) # записываем координаты лучшего хода
    return bestscore # возвращаем лучшую оценку

# функция для определения победы бота, вернет Тру если найдется пятерка камней бота
def isgameover(play):
    I = 0
    while I < len(play): # пока не закончились ходы бота
        a = (play[I][0], play[I][1])
        n = 1
        while n <= 5:
            if (a[0]+40 * n, a[1]) in play: # поиск 5 горизонтальных
                n = n+1
            else:
                break
        if n == 5:
            return True
        n = 1
        while n <= 5:
            if (a[0]+40 * n, a[1]+40 * n) in play: # поиск 5 диагональных вниз-вправо
                n = n+1
            else:
                break
        if n == 5:
            return True
        n = 1
        while n <= 5:
            if (a[0]+40 * n, a[1]-40 * n) in play: # поиск 5 диагональных вниз-влево
                n = n+1
            else:
                break
        if n == 5:
            return True
        n = 1
        while n <= 5:
            if (a[0], a[1]+40 * n) in play: # поиск 5 вертикальных
                n = n+1
            else:
                break
        if n == 5:
            return True
        I = I+1

def getmoves(pl1, pl2):
    moves = [] # список для ходов бота
    used = pl1+pl2 # все использованные ходы
    p = [] # обновляем список
    s1 = 0
    for u in used:# проверка на доступность клетки и ход бота
        if (u[0], u[1]-40) not in used:
            if (u[0], u[1]-40) not in moves:
                moves.append((u[0], u[1]-40)) # вверх
        if (u[0]+40, u[1]-40) not in used:
            if (u[0]+40, u[1]-40) not in moves:
                moves.append((u[0]+40, u[1]-40)) # вверх-вправо
        if (u[0]+40, u[1]) not in used:
            if (u[0]+40, u[1]) not in moves:
                moves.append((u[0]+40, u[1])) # вправо
        if (u[0]+40, u[1]+40) not in used:
            if (u[0]+40, u[1]+40) not in moves:
                moves.append((u[0]+40, u[1]+40)) # вниз-вправо
        if (u[0], u[1]+40) not in used:
            if (u[0], u[1]+40) not in moves:
                moves.append((u[0], u[1]+40)) # вниз
        if (u[0]-40, u[1]+40) not in used:
            if (u[0]-40, u[1]+40) not in moves:
                moves.append((u[0]-40, u[1]+40)) # вниз-влево
        if (u[0]-40, u[1]) not in used:
            if (u[0]-40, u[1]) not in moves:
                moves.append((u[0]-40, u[1])) # влево
        if (u[0]-40, u[1]-40) not in used:
            if (u[0]-40, u[1]-40) not in moves:
                moves.append((u[0]-40, u[1]-40)) # вверх-влево
    s1 = 0
    des = [] # список для лучших ходов
    for m in moves:
        if m[0] > 0 and m[0] < 600 and m[1] > 0 and m[1] < 600: # проверка хода бота в пределах поля
            p = []
            p = pl1+[m] # запись последнего хода
            s2 = evaluate(p, pl2) # оценка эффективности хода
            if s2 > s1: # если нашелся ход лучше
                s1 = s2 # запоминаем оценку
                des = [] # обновляем список лучших ходов
                if m not in des:
                    des.append((m)) # записываем координаты хода
            if s2 == s1: # если оценки равны
                if m not in des:
                    des.append((m)) # записываем координаты хода
    return des

def evaluate(pl1, play):
    p = []
    p = pl1+[]
    pl2 = play+[]
    p.remove(p[len(p)-1]) # удаляем пустой список
    m = pl1[len(pl1)-1] # записываем последний ход
    # поиск 5 в ряд
    # горизонтально 
    if (m[0]+40, m[1]) in p and (m[0]+80, m[1]) in p and (m[0]+120, m[1]) in p and (m[0]+160, m[1]) in p:
        return 10
    if (m[0]-40, m[1]) in p and (m[0]-80, m[1]) in p and (m[0]-120, m[1]) in p and (m[0]-160, m[1]) in p:
        return 10
    if (m[0]-40, m[1]) in p and (m[0]+40, m[1]) in p and (m[0]+80, m[1]) in p and (m[0]+120, m[1]) in p:
        return 10
    if (m[0]-80, m[1]) in p and (m[0]-40, m[1]) in p and (m[0]+40, m[1]) in p and (m[0]+80, m[1]) in p:
        return 10
    if (m[0]-120, m[1]) in p and (m[0]-80, m[1]) in p and (m[0]-40, m[1]) in p and (m[0]+40, m[1]) in p:
        return 10
    # вертикально
    if (m[0], m[1]+40) in p and (m[0], m[1]+80) in p and (m[0], m[1]+120) in p and (m[0], m[1]+160) in p:
        return 10
    if (m[0], m[1]-40) in p and (m[0], m[1]-80) in p and (m[0], m[1]-120) in p and (m[0], m[1]-160) in p:
        return 10
    if (m[0], m[1]-40) in p and (m[0], m[1]+40) in p and (m[0], m[1]+80) in p and (m[0], m[1]+120) in p:
        return 10
    if (m[0], m[1]-80) in p and (m[0], m[1]-40) in p and (m[0], m[1]+40) in p and (m[0], m[1]+80) in p:
        return 10
    if (m[0], m[1]-120) in p and (m[0], m[1]-80) in p and (m[0], m[1]-40) in p and (m[0], m[1]+40) in p:
        return 10
    # диагональных вниз-вправо 
    if (m[0]+40, m[1]+40) in p and (m[0]+80, m[1]+80) in p and (m[0]+120, m[1]+120) in p and (m[0]+160, m[1]+160) in p:
        return 10
    if (m[0]-40, m[1]-40) in p and (m[0]-80, m[1]-80) in p and (m[0]-120, m[1]-120) in p and (m[0]-160, m[1]-160) in p:
        return 10
    if (m[0]-40, m[1]-40) in p and (m[0]+40, m[1]+40) in p and (m[0]+80, m[1]+80) in p and (m[0]+120, m[1]+120) in p:
        return 10
    if (m[0]-80, m[1]-80) in p and (m[0]-40, m[1]-40) in p and (m[0]+40, m[1]+40) in p and (m[0]+80, m[1]+80) in p:
        return 10
    if (m[0]-120, m[1]-120) in p and (m[0]-80, m[1]-80) in p and (m[0]-40, m[1]-40) in p and (m[0]+40, m[1]+40) in p:
        return 10
    # диагональных вниз-влево
    if (m[0]-40, m[1]+40) in p and (m[0]-80, m[1]+80) in p and (m[0]-120, m[1]+120) in p and (m[0]-160, m[1]+160) in p:
        return 10
    if (m[0]+40, m[1]-40) in p and (m[0]+80, m[1]-80) in p and (m[0]+120, m[1]-120) in p and (m[0]+160, m[1]-160) in p:
        return 10
    if (m[0]-40, m[1]+40) in p and (m[0]+40, m[1]-40) in p and (m[0]+80, m[1]-80) in p and (m[0]+120, m[1]-120) in p:
        return 10
    if (m[0]-80, m[1]+80) in p and (m[0]-40, m[1]+40) in p and (m[0]+40, m[1]-40) in p and (m[0]+80, m[1]-80) in p:
        return 10
    if (m[0]-120, m[1]+120) in p and (m[0]-80, m[1]+80) in p and (m[0]-40, m[1]+40) in p and (m[0]+40, m[1]-40) in p:
        return 10
    # диагональных вниз-вправо

    # ПОИСК ХОДОВ, БЛОКИРУЮЩИХ ЧЕТВЕРКИ ПРОТИВНИКА, КОТОРЫЕ РАЗБЛОКИРОВАЛИ СОСЕДНИЕ УЗЛЫ
    # горизонтально 
    if (m[0]+40, m[1]) in pl2 and (m[0]+80, m[1]) in pl2 and (m[0]+120, m[1]) in pl2 and (m[0]+160, m[1]) in pl2:
        return 9
    if (m[0]-40, m[1]) in pl2 and (m[0]-80, m[1]) in pl2 and (m[0]-120, m[1]) in pl2 and (m[0]-160, m[1]) in pl2:
        return 9
    if (m[0]-40, m[1]) in pl2 and (m[0]+40, m[1]) in pl2 and (m[0]+80, m[1]) in pl2 and (m[0]+120, m[1]) in pl2:
        return 9
    if (m[0]-80, m[1]) in pl2 and (m[0]-40, m[1]) in pl2 and (m[0]+40, m[1]) in pl2 and (m[0]+80, m[1]) in pl2:
        return 9
    if (m[0]-120, m[1]) in pl2 and (m[0]-80, m[1]) in pl2 and (m[0]-40, m[1]) in pl2 and (m[0]+40, m[1]) in pl2:
        return 9
    # вертикально
    if (m[0], m[1]+40) in pl2 and (m[0], m[1]+80) in pl2 and (m[0], m[1]+120) in pl2 and (m[0], m[1]+160) in pl2:
        return 9
    if (m[0], m[1]-40) in pl2 and (m[0], m[1]-80) in pl2 and (m[0], m[1]-120) in pl2 and (m[0], m[1]-160) in pl2:
        return 9
    if (m[0], m[1]-40) in pl2 and (m[0], m[1]+40) in pl2 and (m[0], m[1]+80) in pl2 and (m[0], m[1]+120) in pl2:
        return 9
    if (m[0], m[1]-80) in pl2 and (m[0], m[1]-40) in pl2 and (m[0], m[1]+40) in pl2 and (m[0], m[1]+80) in pl2:
        return 9
    if (m[0], m[1]-120) in pl2 and (m[0], m[1]-80) in pl2 and (m[0], m[1]-40) in pl2 and (m[0], m[1]+40) in pl2:
        return 9
    # диагональных вниз-вправо
    if (m[0]+40, m[1]+40) in pl2 and (m[0]+80, m[1]+80) in pl2 and (m[0]+120, m[1]+120) in pl2 and (
    m[0]+160, m[1]+160) in pl2:
        return 9
    if (m[0]-40, m[1]-40) in pl2 and (m[0]-80, m[1]-80) in pl2 and (m[0]-120, m[1]-120) in pl2 and (
    m[0]-160, m[1]-160) in pl2:
        return 9
    if (m[0]-40, m[1]-40) in pl2 and (m[0]+40, m[1]+40) in pl2 and (m[0]+80, m[1]+80) in pl2 and (
    m[0]+120, m[1]+120) in pl2:
        return 9
    if (m[0]-80, m[1]-80) in pl2 and (m[0]-40, m[1]-40) in pl2 and (m[0]+40, m[1]+40) in pl2 and (
    m[0]+80, m[1]+80) in pl2:
        return 9
    if (m[0]-120, m[1]-120) in pl2 and (m[0]-80, m[1]-80) in pl2 and (m[0]-40, m[1]-40) in pl2 and (
    m[0]+40, m[1]+40) in pl2:
        return 9
    # диагональных вниз-влево
    if (m[0]-40, m[1]+40) in pl2 and (m[0]-80, m[1]+80) in pl2 and (m[0]-120, m[1]+120) in pl2 and (
    m[0]-160, m[1]+160) in pl2:
        return 9
    if (m[0]+40, m[1]-40) in pl2 and (m[0]+80, m[1]-80) in pl2 and (m[0]+120, m[1]-120) in pl2 and (
    m[0]+160, m[1]-160) in pl2:
        return 9
    if (m[0]-40, m[1]+40) in pl2 and (m[0]+40, m[1]-40) in pl2 and (m[0]+80, m[1]-80) in pl2 and (
    m[0]+120, m[1]-120) in pl2:
        return 9
    if (m[0]-80, m[1]+80) in pl2 and (m[0]-40, m[1]+40) in pl2 and (m[0]+40, m[1]-40) in pl2 and (
    m[0]+80, m[1]-80) in pl2:
        return 9
    if (m[0]-120, m[1]+120) in pl2 and (m[0]-80, m[1]+80) in pl2 and (m[0]-40, m[1]+40) in pl2 and (
    m[0]+40, m[1]-40) in pl2:
        return 9

    # ПОИСК ЧЕТВЕРОК (ОБЕ СТОРОНЫ РАЗБЛОКИРОВАНЫ)
    # горизонтально
    if (m[0]-40, m[1]) not in pl2 and (m[0]+40, m[1]) in p and (m[0]+80, m[1]) in p and (
    m[0]+120, m[1]) in p and (m[0]+160, m[1]) not in pl2:
        return 8
    if (m[0]-80, m[1]) not in pl2 and (m[0]-40, m[1]) in p and (m[0]+40, m[1]) in p and (
    m[0]+80, m[1]) in p and (m[0]+120, m[1]) not in pl2:
        return 8
    if (m[0]-120, m[1]) not in pl2 and (m[0]-80, m[1]) in p and (m[0]-40, m[1]) in p and (
    m[0]+40, m[1]) in p and (m[0]+80, m[1]) not in pl2:
        return 8
    if (m[0]-160, m[1]) not in pl2 and (m[0]-120, m[1]) in p and (m[0]-80, m[1]) in p and (
    m[0]-40, m[1]) in p and (m[0]+40, m[1]) not in pl2:
        return 8
    # диагональных вниз-вправо
    if (m[0]-40, m[1]-40) not in pl2 and (m[0]+40, m[1]+40) in p and (m[0]+80, m[1]+80) in p and (
    m[0]+120, m[1]+120) in p and (m[0]+160, m[1]+160) not in pl2:
        return 8
    if (m[0]-80, m[1]-80) not in pl2 and (m[0]-40, m[1]-40) in p and (m[0]+40, m[1]+40) in p and (
    m[0]+80, m[1]+80) in p and (m[0]+120, m[1]+120) not in pl2:
        return 8
    if (m[0]-120, m[1]-120) not in pl2 and (m[0]-80, m[1]-80) in p and (m[0]-40, m[1]-40) in p and (
    m[0]+40, m[1]+40) in p and (m[0]+80, m[1]+80) not in pl2:
        return 8
    if (m[0]-160, m[1]-160) not in pl2 and (m[0]-120, m[1]-120) in p and (m[0]-80, m[1]-80) in p and (
    m[0]-40, m[1]-40) in p and (m[0]+40, m[1]+40) not in pl2:
        return 8
    # диагональных вниз-влево
    if (m[0]-40, m[1]+40) not in pl2 and (m[0]+40, m[1]-40) in p and (m[0]+80, m[1]-80) in p and (
    m[0]+120, m[1]-120) in p and (m[0]+160, m[1]-160) not in pl2:
        return 8
    if (m[0]-80, m[1]+80) not in pl2 and (m[0]-40, m[1]+40) in p and (m[0]+40, m[1]-40) in p and (
    m[0]+80, m[1]-80) in p and (m[0]+120, m[1]-120) not in pl2:
        return 8
    if (m[0]-120, m[1]+120) not in pl2 and (m[0]-80, m[1]+80) in p and (m[0]-40, m[1]+40) in p and (
    m[0]+40, m[1]-40) in p and (m[0]+80, m[1]-80) not in pl2:
        return 8
    if (m[0]-160, m[1]+160) not in pl2 and (m[0]-120, m[1]+120) in p and (m[0]-80, m[1]+80) in p and (
    m[0]-40, m[1]+40) in p and (m[0]+40, m[1]-40) not in pl2:
        return 8
    # вертикально
    if (m[0], m[1]-40) not in pl2 and (m[0], m[1]+40) in p and (m[0], m[1]+80) in p and (
    m[0], m[1]+120) in p and (m[0], m[1]+160) not in pl2:
        return 8
    if (m[0], m[1]-80) not in pl2 and (m[0], m[1]-40) in p and (m[0], m[1]+40) in p and (
    m[0], m[1]+80) in p and (m[0], m[1]+120) not in pl2:
        return 8
    if (m[0], m[1]-120) not in pl2 and (m[0], m[1]-80) in p and (m[0], m[1]-40) in p and (
    m[0], m[1]+40) in p and (m[0], m[1]+80) not in pl2:
        return 8
    if (m[0], m[1]-160) not in pl2 and (m[0], m[1]-120) in p and (m[0], m[1]-80) in p and (
    m[0], m[1]-40) in p and (m[0], m[1]+40) not in pl2:
        return 8

    pin = 0
    # ПОИСК ЧЕТВЕРОК (ОДНА СТОРОНА РАЗБЛОКИРОВАНА)
    # горизонтально 
    if ((m[0]-40, m[1]) not in pl2 or (m[0]+160, m[1]) not in pl2) and (m[0]+40, m[1]) in p and (
    m[0]+80, m[1]) in p and (m[0]+120, m[1]) in p:
        pin = 7
    elif ((m[0]-80, m[1]) not in pl2 or (m[0]+120, m[1]) not in pl2) and (m[0]-40, m[1]) in p and (
    m[0]+40, m[1]) in p and (m[0]+80, m[1]) in p:
        pin = 7
    elif ((m[0]-120, m[1]) not in pl2 or (m[0]+80, m[1]) not in pl2) and (m[0]-80, m[1]) in p and (
    m[0]-40, m[1]) in p and (m[0]+40, m[1]) in p:
        pin = 7
    elif ((m[0]-160, m[1]) not in pl2 or (m[0]+40, m[1]) not in pl2) and (m[0]-120, m[1]) in p and (
    m[0]-80, m[1]) in p and (m[0]-40, m[1]) in p:
        pin = 7
    # диагональных вниз-вправо 
    elif ((m[0]-40, m[1]-40) not in pl2 or (m[0]+160, m[1]+160) not in pl2) and (
    m[0]+40, m[1]+40) in p and (m[0]+80, m[1]+80) in p and (m[0]+120, m[1]+120) in p:
        pin = 7
    elif ((m[0]-80, m[1]-80) not in pl2 or (m[0]+120, m[1]+120) not in pl2) and (
    m[0]-40, m[1]-40) in p and (m[0]+40, m[1]+40) in p and (m[0]+80, m[1]+80) in p:
        pin = 7
    elif ((m[0]-120, m[1]-120) not in pl2 or (m[0]+80, m[1]+80) not in pl2) and (
    m[0]-80, m[1]-80) in p and (m[0]-40, m[1]-40) in p and (m[0]+40, m[1]+40) in p:
        pin = 7
    elif ((m[0]-160, m[1]-160) not in pl2 or (m[0]+40, m[1]+40) not in pl2) and (
    m[0]-120, m[1]-120) in p and (m[0]-80, m[1]-80) in p and (m[0]-40, m[1]-40) in p:
        pin = 7
    # диагональных вниз-влево
    elif ((m[0]-40, m[1]+40) not in pl2 or (m[0]+160, m[1]-160) not in pl2) and (
    m[0]+40, m[1]-40) in p and (m[0]+80, m[1]-80) in p and (m[0]+120, m[1]-120) in p:
        pin = 7
    elif ((m[0]-80, m[1]+80) not in pl2 or (m[0]+120, m[1]-120) not in pl2) and (
    m[0]-40, m[1]+40) in p and (m[0]+40, m[1]-40) in p and (m[0]+80, m[1]-80) in p:
        pin = 7
    elif ((m[0]-120, m[1]+120) not in pl2 or (m[0]+80, m[1]-80) not in pl2) and (
    m[0]-80, m[1]+80) in p and (m[0]-40, m[1]+40) in p and (m[0]+40, m[1]-40) in p:
        pin = 7
    elif ((m[0]-160, m[1]+160) not in pl2 or (m[0]+40, m[1]-40) not in pl2) and (
    m[0]-120, m[1]+120) in p and (m[0]-80, m[1]+80) in p and (m[0]-40, m[1]+40) in p:
        pin = 7
    # вертикально
    elif ((m[0], m[1]-40) not in pl2 or (m[0], m[1]+160) not in pl2) and (m[0], m[1]+40) in p and (
    m[0], m[1]+80) in p and (m[0], m[1]+120) in p:
        pin = 7
    elif ((m[0], m[1]-80) not in pl2 or (m[0], m[1]+120) not in pl2) and (m[0], m[1]-40) in p and (
    m[0], m[1]+40) in p and (m[0], m[1]+80) in p:
        pin = 7
    elif ((m[0], m[1]-120) not in pl2 or (m[0], m[1]+80) not in pl2) and (m[0], m[1]-80) in p and (
    m[0], m[1]-40) in p and (m[0], m[1]+40) in p:
        pin = 7
    elif ((m[0], m[1]-160) not in pl2 or (m[0], m[1]+40) not in pl2) and (m[0], m[1]-120) in p and (
    m[0], m[1]-80) in p and (m[0], m[1]-40) in p:
        pin = 7
    # горизонтально 3к1
    elif (m[0]+40, m[1]) not in pl2 and (m[0]+80, m[1]) in p and (m[0]+120, m[1]) in p and (m[0]+160, m[1]) in p:
        pin = 7
    elif (m[0]-40, m[1]) not in pl2 and (m[0]-80, m[1]) in p and (m[0]-120, m[1]) in p and (m[0]-160, m[1]) in p:
        pin = 7
    # диагональных вниз-вправо 3к1
    elif (m[0]+40, m[1]+40) not in pl2 and (m[0]+80, m[1]+80) in p and (m[0]+120, m[1]+120) in p and (
    m[0]+160, m[1]+160) in p:
        pin = 7
    elif (m[0]-40, m[1]-40) not in pl2 and (m[0]-80, m[1]-80) in p and (m[0]-120, m[1]-120) in p and (
    m[0]-160, m[1]-160) in p:
        pin = 7
    # диагональных вниз-влево 3к1
    elif (m[0]+40, m[1]-40) not in pl2 and (m[0]+80, m[1]-80) in p and (m[0]+120, m[1]-120) in p and (
    m[0]+160, m[1]-160) in p:
        pin = 7
    elif (m[0]-40, m[1]+40) not in pl2 and (m[0]-80, m[1]+80) in p and (m[0]-120, m[1]+120) in p and (
    m[0]-160, m[1]+160) in p:
        pin = 7
    # вертикально 3к1
    elif (m[0], m[1]+40) not in pl2 and (m[0], m[1]+80) in p and (m[0], m[1]+120) in p and (m[0], m[1]+160) in p:
        pin = 7
    elif (m[0], m[1]-40) not in pl2 and (m[0], m[1]-80) in p and (m[0], m[1]-120) in p and (m[0], m[1]-160) in p:
        pin = 7

    temp = 1
    # ПОИСК ТРОЕК (ТРИ НЕЗАБЛОКИРОВАННЫХ СМЕЖНЫХ УЗЛА)&(ДВА НЕЗАБЛОКИРОВАННЫХ СМЕЖНЫХ УЗЛА)
    # горизонтально
    if (m[0]-40, m[1]) not in pl2 and (m[0]+40, m[1]) in p and (m[0]+80, m[1]) in p and (m[0]+120, m[1]) not in pl2:
        if (m[0]-80, m[1]) not in pl2 and (m[0]+160, m[1]) not in pl2:
            temp = 5
        elif (m[0]-80, m[1]) not in pl2 or (m[0]+160, m[1]) not in pl2:
            temp = 0
        else:
            temp = 2
    # диагональных вниз-вправо
    if (m[0]-40, m[1]-40) not in pl2 and (m[0]+40, m[1]+40) in p and (m[0]+80, m[1]+80) in p and (
    m[0]+120, m[1]+120) not in pl2:
        if (m[0]-80, m[1]-80) not in pl2 and (m[0]+160, m[1]+160) not in pl2:
            temp = 5
        elif (m[0]-80, m[1]-80) not in pl2 or (m[0]+160, m[1]+160) not in pl2:
            temp = 0
        else:
            temp = 2
    # диагональных вниз-влево 
    if (m[0]-40, m[1]+40) not in pl2 and (m[0]+40, m[1]-40) in p and (m[0]+80, m[1]-80) in p and (
    m[0]+120, m[1]-120) not in pl2:
        if (m[0]-80, m[1]+80) not in pl2 and (m[0]+160, m[1]-160) not in pl2:
            temp = 5
        elif (m[0]-80, m[1]+80) not in pl2 or (m[0]+160, m[1]-160) not in pl2:
            temp = 0
        else:
            temp = 2
    # вертикально 
    if (m[0], m[1]-40) not in pl2 and (m[0], m[1]+40) in p and (m[0], m[1]+80) in p and (m[0], m[1]+120) not in pl2:
        if (m[0], m[1]-80) not in pl2 and (m[0], m[1]+160) not in pl2:
            temp = 5
        elif (m[0], m[1]-80) not in pl2 or (m[0], m[1]+160) not in pl2:
            temp = 0
        else:
            temp = 2
    if pin == 7:
        if temp == 5:
            return 7.5
        else:
            return 7

    # ПОИСК ХОДОВ, БЛОКИРУЮЩИХ ТРОЙКИ ПРОТИВНИКА С ТРЕМЯ СОСЕДНИМИ ПУСТЫМИ УЗЛАМИ
    # горизонтально 
    if (m[0]+40, m[1]) in pl2 and (m[0]+80, m[1]) in pl2 and (m[0]+120, m[1]) in pl2 and (
    m[0]+160, m[1]) not in p and (m[0]+200, m[1]) not in p:
        return 6
    if (m[0]-40, m[1]) in pl2 and (m[0]-80, m[1]) in pl2 and (m[0]-120, m[1]) in pl2 and (
    m[0]-160, m[1]) not in p and (m[0]-200, m[1]) not in p:
        return 6
    if (m[0]-40, m[1]) not in p and (m[0]+40, m[1]) in pl2 and (m[0]+80, m[1]) in pl2 and (
    m[0]+120, m[1]) in pl2 and (m[0]+160, m[1]) not in p:
        return 6
    if (m[0]+40, m[1]) not in p and (m[0]-40, m[1]) in pl2 and (m[0]-80, m[1]) in pl2 and (
    m[0]-120, m[1]) in pl2 and (m[0]-160, m[1]) not in p:
        return 6
    # диагональных вниз-вправо 
    if (m[0]+40, m[1]+40) in pl2 and (m[0]+80, m[1]+80) in pl2 and (m[0]+120, m[1]+120) in pl2 and (
    m[0]+160, m[1]+160) not in p and (m[0]+200, m[1]+200) not in p:
        return 6
    if (m[0]-40, m[1]-40) in pl2 and (m[0]-80, m[1]-80) in pl2 and (m[0]-120, m[1]-120) in pl2 and (
    m[0]-160, m[1]-160) not in p and (m[0]-200, m[1]-200) not in p:
        return 6
    if (m[0]-40, m[1]-40) not in p and (m[0]+40, m[1]+40) in pl2 and (m[0]+80, m[1]+80) in pl2 and (
    m[0]+120, m[1]+120) in pl2 and (m[0]+160, m[1]+160) not in p:
        return 6
    if (m[0]+40, m[1]+40) not in p and (m[0]-40, m[1]-40) in pl2 and (m[0]-80, m[1]-80) in pl2 and (
    m[0]-120, m[1]-120) in pl2 and (m[0]-160, m[1]-160) not in p:
        return 6
    # диагональных вниз-влево
    if (m[0]+40, m[1]-40) in pl2 and (m[0]+80, m[1]-80) in pl2 and (m[0]+120, m[1]-120) in pl2 and (
    m[0]+160, m[1]-160) not in p and (m[0]+200, m[1]-200) not in p:
        return 6
    if (m[0]-40, m[1]+40) in pl2 and (m[0]-80, m[1]+80) in pl2 and (m[0]-120, m[1]+120) in pl2 and (
    m[0]-160, m[1]+160) not in p and (m[0]-200, m[1]+200) not in p:
        return 6
    if (m[0]-40, m[1]+40) not in p and (m[0]+40, m[1]-40) in pl2 and (m[0]+80, m[1]-80) in pl2 and (
    m[0]+120, m[1]-120) in pl2 and (m[0]+160, m[1]-160) not in p:
        return 6
    if (m[0]+40, m[1]-40) not in p and (m[0]-40, m[1]+40) in pl2 and (m[0]-80, m[1]+80) in pl2 and (
    m[0]-120, m[1]+120) in pl2 and (m[0]-160, m[1]+160) not in p:
        return 6
    # вертикально
    if (m[0], m[1]+40) in pl2 and (m[0], m[1]+80) in pl2 and (m[0], m[1]+120) in pl2 and (
    m[0], m[1]+160) not in p and (m[0], m[1]+200) not in p:
        return 6
    if (m[0], m[1]-40) in pl2 and (m[0], m[1]-80) in pl2 and (m[0], m[1]-120) in pl2 and (
    m[0], m[1]-160) not in p and (m[0], m[1]-200) not in p:
        return 6
    if (m[0], m[1]-40) not in p and (m[0], m[1]+40) in pl2 and (m[0], m[1]+80) in pl2 and (
    m[0], m[1]+120) in pl2 and (m[0], m[1]+160) not in p:
        return 6
    if (m[0], m[1]+40) not in p and (m[0], m[1]-40) in pl2 and (m[0], m[1]-80) in pl2 and (
    m[0], m[1]-120) in pl2 and (m[0], m[1]-160) not in p:
        return 6

    # БЛОКИРОВАНИЕ УДАРОВ СОПЕРНИКА
    # горизонтально 2к1
    if (m[0]-80, m[1]) not in p and (m[0]-40, m[1]) in pl2 and (m[0]+40, m[1]) in pl2 and (
    m[0]+80, m[1]) in pl2 and (m[0]+120, m[1]) not in p:
        return 6
    if (m[0]-120, m[1]) not in p and (m[0]-80, m[1]) in pl2 and (m[0]-40, m[1]) in pl2 and (
    m[0]+40, m[1]) in pl2 and (m[0]+80, m[1]) not in p:
        return 6
    # диагональных вниз-вправо 2к1
    if (m[0]-80, m[1]-80) not in p and (m[0]-40, m[1]-40) in pl2 and (m[0]+40, m[1]+40) in pl2 and (
    m[0]+80, m[1]+80) in pl2 and (m[0]+120, m[1]+120) not in p:
        return 6
    if (m[0]-120, m[1]-120) not in p and (m[0]-80, m[1]-80) in pl2 and (m[0]-40, m[1]-40) in pl2 and (
    m[0]+40, m[1]+40) in pl2 and (m[0]+80, m[1]+80) not in p:
        return 6
    # диагональных вниз-влево 2к1
    if (m[0]-80, m[1]+80) not in p and (m[0]-40, m[1]+40) in pl2 and (m[0]+40, m[1]-40) in pl2 and (
    m[0]+80, m[1]-80) in pl2 and (m[0]+120, m[1]-120) not in p:
        return 6
    if (m[0]-120, m[1]+120) not in p and (m[0]-80, m[1]+80) in pl2 and (m[0]-40, m[1]+40) in pl2 and (
    m[0]+40, m[1]-40) in pl2 and (m[0]+80, m[1]-80) not in p:
        return 6
    # вертикально 2к1
    if (m[0], m[1]-80) not in p and (m[0], m[1]-40) in pl2 and (m[0], m[1]+40) in pl2 and (
    m[0], m[1]+80) in pl2 and (m[0], m[1]+120) not in p:
        return 6
    if (m[0], m[1]-120) not in p and (m[0], m[1]-80) in pl2 and (m[0], m[1]-40) in pl2 and (
    m[0], m[1]+40) in pl2 and (m[0], m[1]+80) not in p:
        return 6

    if temp == 5:
        return 5
    if temp == 0:
        return 4

    # ПОИСК СЛОМАННЫХ ТРОЕК
    # горизонтально 2к1
    if (m[0]+40, m[1]) in p and (m[0]+80, m[1]) not in pl2 and (m[0]+120, m[1]) in p:
        if (m[0]-40, m[1]) not in pl2 or (m[0]+160, m[1]) not in pl2:
            return 3
    # диагональных вниз-вправо 2к1
    if (m[0]+40, m[1]+40) in p and (m[0]+80, m[1]+80) not in pl2 and (m[0]+120, m[1]+120) in p:
        if (m[0]-40, m[1]-40) not in pl2 or (m[0]+160, m[1]+160) not in pl2:
            return 3
    # диагональных вниз-влево2к1
    if (m[0]+40, m[1]-40) in p and (m[0]+80, m[1]-80) not in pl2 and (m[0]+120, m[1]-120) in p:
        if (m[0]-40, m[1]+40) not in pl2 or (m[0]+160, m[1]-160) not in pl2:
            return 3
    # вертикально 2к1
    if (m[0], m[1]+40) in p and (m[0], m[1]+80) not in pl2 and (m[0], m[1]+120) in p:
        if (m[0], m[1]-40) not in pl2 or (m[0], m[1]+160) not in pl2:
            return 3

    # ПОИСК ДВОЕК
    if ((m[0]-40, m[1]) in p or (m[0]+40, m[1]) in p) and (m[0]-80, m[1]) not in pl2 and (
    m[0]-40, m[1]) not in pl2 and (m[0]+40, m[1]) not in pl2 and (m[0]+80, m[1]) not in pl2:
        return 2
    if ((m[0]-40, m[1]-40) in p or (m[0]+40, m[1]+40) in p) and (m[0]-80, m[1]-80) not in pl2 and (
    m[0]-40, m[1]-40) not in pl2 and (m[0]+40, m[1]+40) not in pl2 and (m[0]+80, m[1]+80) not in pl2:
        return 2
    if ((m[0]-40, m[1]+40) in p or (m[0]+40, m[1]-40) in p) and (m[0]-80, m[1]+80) not in pl2 and (
    m[0]-40, m[1]+40) not in pl2 and (m[0]+40, m[1]-40) not in pl2 and (m[0]+80, m[1]-80) not in pl2:
        return 2
    if ((m[0], m[1]-40) in p or (m[0], m[1]+40) in p) and (m[0], m[1]-80) not in pl2 and (
    m[0], m[1]-40) not in pl2 and (m[0], m[1]+40) not in pl2 and (m[0], m[1]+80) not in pl2:
        return 2
    if (m[0]-40, m[1]) in p and (m[0]+40, m[1]) not in pl2 and (m[0]+80, m[1]) not in pl2 and (
    m[0]+120, m[1]) not in pl2:
        return 2
    if (m[0]-40, m[1]-40) in p and (m[0]+40, m[1]+40) not in pl2 and (m[0]+80, m[1]+80) not in pl2 and (
    m[0]+120, m[1]+120) not in pl2:
        return 2
    if (m[0]-40, m[1]+40) in p and (m[0]+40, m[1]-40) not in pl2 and (m[0]+80, m[1]-80) not in pl2 and (
    m[0]+120, m[1]-120) not in pl2:
        return 2
    if (m[0], m[1]-40) in p and (m[0], m[1]+40) not in pl2 and (m[0], m[1]+80) not in pl2 and (
    m[0], m[1]+120) not in pl2:
        return 2
    if (m[0]+40, m[1]) in p and (m[0]+80, m[1]) not in pl2 and (m[0]+120, m[1]) not in pl2 and (
    m[0]+160, m[1]) not in pl2:
        return 2
    if (m[0]+40, m[1]+40) in p and (m[0]+80, m[1]+80) not in pl2 and (
    m[0]+120, m[1]+120) not in pl2 and (m[0]+160, m[1]+160) not in pl2:
        return 2
    if (m[0]+40, m[1]-40) in p and (m[0]+80, m[1]-80) not in pl2 and (
    m[0]+120, m[1]-120) not in pl2 and (m[0]+160, m[1]-160) not in pl2:
        return 2
    if (m[0], m[1]+40) in p and (m[0], m[1]+80) not in pl2 and (m[0], m[1]+120) not in pl2 and (
    m[0], m[1]+160) not in pl2:
        return 2
    if (m[0]-40, m[1]) not in pl2 and (m[0]+40, m[1]) in p and (m[0]+80, m[1]) not in pl2 and (
    m[0]+120, m[1]) not in pl2:
        return 2
    if (m[0]-40, m[1]-40) not in pl2 and (m[0]+40, m[1]+40) in p and (m[0]+80, m[1]+80) not in pl2 and (
    m[0]+120, m[1]+120) not in pl2:
        return 2
    if (m[0]-40, m[1]+40) not in pl2 and (m[0]+40, m[1]-40) in p and (m[0]+80, m[1]-80) not in pl2 and (
    m[0]+120, m[1]-120) not in pl2:
        return 2
    if (m[0], m[1]-40) not in pl2 and (m[0], m[1]+40) in p and (m[0], m[1]+80) not in pl2 and (
    m[0], m[1]+120) not in pl2:
        return 2
    if (m[0]-40, m[1]) in p and (m[0]-80, m[1]) not in pl2 and (m[0]-120, m[1]) not in pl2 and (
    m[0]+40, m[1]) not in pl2:
        return 2
    if (m[0]-40, m[1]-40) in p and (m[0]-80, m[1]-80) not in pl2 and (
    m[0]-120, m[1]-120) not in pl2 and (m[0]+40, m[1]+40) not in pl2:
        return 2
    if (m[0]-40, m[1]+40) in p and (m[0]-80, m[1]+80) not in pl2 and (
    m[0]-120, m[1]+120) not in pl2 and (m[0]+40, m[1]+40) not in pl2:
        return 2
    if (m[0], m[1]-40) in p and (m[0], m[1]-80) not in pl2 and (m[0], m[1]-120) not in pl2 and (
    m[0], m[1]+40) not in pl2:
        return 2
    if (m[0]-40, m[1]) in p and (m[0]-80, m[1]) not in pl2 and (m[0]-120, m[1]) not in pl2 and (
    m[0]-160, m[1]) not in pl2:
        return 2
    if (m[0]-40, m[1]-40) in p and (m[0]-80, m[1]-80) not in pl2 and (
    m[0]-120, m[1]-120) not in pl2 and (m[0]-160, m[1]-160) not in pl2:
        return 2
    if (m[0]-40, m[1]+40) in p and (m[0]-80, m[1]+80) not in pl2 and (
    m[0]-120, m[1]+120) not in pl2 and (m[0]-160, m[1]+160) not in pl2:
        return 2
    if (m[0], m[1]-40) in p and (m[0], m[1]-80) not in pl2 and (m[0], m[1]-120) not in pl2 and (
    m[0], m[1]-160) not in pl2:
        return 2
    if (m[0]-40, m[1]) not in pl2 and (m[0]-80, m[1]) not in pl2 and (m[0]-120, m[1]) not in pl2 and (
    m[0]+40, m[1]) in p:
        return 2
    if (m[0]-40, m[1]-40) not in pl2 and (m[0]-80, m[1]-80) not in pl2 and (
    m[0]-120, m[1]-120) not in pl2 and (m[0]+40, m[1]+40) in p:
        return 2
    if (m[0]-40, m[1]+40) not in pl2 and (m[0]-80, m[1]+80) not in pl2 and (
    m[0]-120, m[1]+120) not in pl2 and (m[0]+40, m[1]-40) in p:
        return 2
    if (m[0], m[1]-40) not in pl2 and (m[0], m[1]-80) not in pl2 and (m[0], m[1]-120) not in pl2 and (
    m[0], m[1]+40) in p:
        return 2

    return 0