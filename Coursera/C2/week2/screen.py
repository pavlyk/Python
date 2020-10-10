#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import random
import math

SCREEN_DIM = (800, 600)


class Vec2d():
    def __init__(self, x):
        self.x = x

    def length(self, x):
        """возвращает длину вектора"""
        return math.sqrt(self.x[0] * self.x[0] + self.x[1] * self.x[1])

    def __getitem__(self, i):
        return self.x[i]

    def int_pair(self):
        """возвращает пару координат, определяющих вектор (координаты точки конца вектора),
        координаты начальной точки вектора совпадают с началом системы координат (0, 0)"""
        return int(self.x[0]), int(self.x[1])

    def __sub__(self, y):
        """"возвращает разность двух векторов"""
        return self.x[0] - y[0], self.x[1] - y[1]

    @staticmethod
    def __add__(x, y):
        """возвращает сумму двух векторов"""
        return Vec2d((x[0] + y[0], x[1] + y[1]))

    def __mul__(self, k):
        """возвращает произведение вектора на число"""
        return Vec2d((self.x[0] * k, self.x[1] * k))

# =======================================================================================
# Функции, отвечающие за расчет сглаживания ломаной
# =======================================================================================

class Polyline():
    def __init__(self, points, count):
        self.points = points
        self.count = count
    
    def get_point(self, points, alpha, deg=None):
        """функция получает на вход 3 базовые точки и шаг например 1/35
        рекурсивно суммируем вектора начиная с самого первого
        v = add(mul(point[1], 1/35), mul(point[0], 34/35))
        потом то что получилось на этом шаге возвращаем в второй аргумент
        add(mul(point[2], 1/35), mul(v, 34/35))
        тоесть берем первый вектор с большим коэффициентом а другие все с маленьким
        далее когда alpha будет расти будет первый вектор с маленькам коэффициентом
        """
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        v1 = points[deg].__mul__(alpha)
        v2 = self.get_point(points, alpha, deg - 1).__mul__(1 - alpha)

        return Vec2d.__add__(v1, v2)

    def get_points(self, base_points, count):
        """функция получает на вход 3 базовые точки
        и кол-во шагов которые нужно добавить
        Получаем n промежуточных точек
        """
        alpha = 1 / count
        res = []
        for i in range(count):
            p = self.get_point(base_points, i * alpha)
            res.append(p)

        return res

    def set_points(self, speeds):
        """функция перерасчета координат опорных точек"""
        for p in range(len(self.points)):
            self.points[p] = Vec2d.__add__(self.points[p], speeds[p])
            if self.points[p][0] > SCREEN_DIM[0] or self.points[p][0] < 0:
                speeds[p] = [- speeds[p][0], speeds[p][1]]
            if self.points[p][1] > SCREEN_DIM[1] or self.points[p][1] < 0:
                speeds[p] = [speeds[p][0], -speeds[p][1]]


class Knot(Polyline):
    def __init__(self, points, count):
        super().__init__(points, count)

    def get_knot(self):
        if len(self.points) < 3:
            return []
        res = []
        for i in range(-2, len(self.points) - 2):
            ptn = []
            ptn.append(Vec2d.__add__(self.points[i], self.points[i + 1]).__mul__(0.5)) # Добавляем среднюю точку между i и i+1
            ptn.append(points[i + 1])
            ptn.append(Vec2d.__add__(self.points[i + 1], self.points[i + 2]).__mul__(0.5)) # Добавляем среднюю точку между i + 1 и i + 2
            res.extend(self.get_points(ptn, self.count)) # Дополняет список элементами из указанного объекта.
        return res


# =======================================================================================
# Функции отрисовки
# =======================================================================================
def draw_points(points, style="points", width=3, color=(255, 255, 255)):
    """функция отрисовки точек на экране"""
    if style == "line":
        for p_n in range(-1, len(points) - 1):
            intp1, intp2 = points[p_n].int_pair(), points[p_n + 1].int_pair()
            pygame.draw.line(gameDisplay, color,
                             (intp1[0], intp1[1]),
                             (intp2[0], intp2[1]), width)

    elif style == "points":
        for p in points:
            intp = p.int_pair()
            pygame.draw.circle(gameDisplay, color,
                               (intp[0], intp[1]), width)

def draw_help():
    """функция отрисовки экрана справки программы"""
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = []
    data.append(["F1", "Show Help"])
    data.append(["R", "Restart"])
    data.append(["P", "Pause/Play"])
    data.append(["Num+", "More points"])
    data.append(["Num-", "Less points"])
    data.append(["Q", "Speed Up"])
    data.append(["W", "Speed Down"])
    data.append(["D", "Delete last point"])
    data.append(["", ""])
    data.append([str(steps), "Current points"])

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
        (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * i))

def change_speed(speeds, change):
    for speed in speeds:
        speed[0] = 0.1 if speed[0] + change <= 0 else speed[0] + change 
        speed[1] = 0.1 if speed[1] + change <= 0 else speed[1] + change 

# =======================================================================================
# Основная программа
# =======================================================================================
if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    steps = 35
    working = True
    points = []
    speeds = []
    show_help = False
    pause = True

    hue = 0
    color = pygame.Color(0)
    knt = Knot(points, steps)

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    points = []
                    speeds = []
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0
                if event.key == pygame.K_d:
                    points.pop()
                if event.key == pygame.K_q:
                    change_speed(speeds, 1)
                if event.key == pygame.K_w:
                    change_speed(speeds, -1)

            if event.type == pygame.MOUSEBUTTONDOWN:
                points.append(Vec2d(event.pos))
                speeds.append([random.random() * 2, random.random() * 2])

        gameDisplay.fill((0, 0, 0)) # background color
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100) # (hue, saturation, lightness) alpha
        draw_points(points)
        knt.points = points
        draw_points(knt.get_knot(), "line", 3, color)
        if not pause:
            knt.set_points(speeds)
        if show_help:
            draw_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
