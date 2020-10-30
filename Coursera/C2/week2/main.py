#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import random
import math

SCREEN_DIM = (800, 600)
SPEED_SCALAR = 2


# =======================================================================================
# Класс для работы с векторами
# =======================================================================================

class Vec2d:
    def __init__(self, x, y):
        self.vec = (x, y)

    def __add__(self, other):
        """возвращает сумму двух векторов"""
        new_x = self.vec[0] + other.vec[0]
        new_y = self.vec[1] + other.vec[1]
        return Vec2d(new_x, new_y)

    def __sub__(self, other):
        """возвращает сумму двух векторов"""
        new_x = self.vec[0] - other.vec[0]
        new_y = self.vec[1] - other.vec[1]
        return Vec2d(new_x, new_y)

    def __mul__(self, scalar):
        """возвращает вектор умноженный на скаляр"""
        new_x = self.vec[0] * scalar
        new_y = self.vec[1] * scalar
        return Vec2d(new_x, new_y)

    def __len__(self):
        """возвращает длину вектора"""
        return math.sqrt(self.vec[0] ** 2 + self.vec[1] ** 2)

    def __getitem__(self, key):
        return self.vec[key]

    def int_pair(self):
        """возвращает произведение вектора на число"""
        return self.vec[0], self.vec[1]


# =======================================================================================
# Классы отвечающие за ортисовку ломаных
# =======================================================================================

class Polyline:
    def __init__(self, points=None, speeds=None):
        self.points = points or []
        self.speeds = speeds or []

    def add_point_and_speed(self, point, speed):
        self.points.append(point)
        self.speeds.append(speed)

    def set_points(self):
        for p in range(len(self.points)):
            self.points[p] += self.speeds[p]
            if self.points[p][0] > SCREEN_DIM[0] or self.points[p][0] < 0:
                self.speeds[p] = Vec2d(- self.speeds[p][0], self.speeds[p][1])
            if self.points[p][1] > SCREEN_DIM[1] or self.points[p][1] < 0:
                self.speeds[p] = Vec2d(self.speeds[p][0], -self.speeds[p][1])

    def draw_points(self, style="points", width=3, color=(255, 255, 255)):  # отрисовка ломаной
        if style == "line":
            for p_n in range(-1, len(self.points) - 1):
                pygame.draw.line(gameDisplay, color, (int(self.points[p_n][0]), int(self.points[p_n][1])),
                                 (int(self.points[p_n + 1][0]), int(self.points[p_n + 1][1])), width)

        elif style == "points":
            for p in self.points:
                pygame.draw.circle(gameDisplay, color,
                                   (int(p[0]), int(p[1])), width)

    def accelerate(self):
        self.speeds = [speed * 1.1 for speed in self.speeds]

    def drop_speed(self):
        self.speeds = [speed * 0.9 for speed in self.speeds]

    def drop_point(self):
        if self.points:
            self.points.pop()
            self.speeds.pop()


class Knot(Polyline):
    def __init__(self, points=None, count=0):
        self.points = points or []
        self.count = count

    def __get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return points[deg] * alpha + self.__get_point(points, alpha, deg - 1) * (1 - alpha)

    def __get_points(self, base_points, count):
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(self.__get_point(base_points, i * alpha))
        return res

    def get_knot(self):
        if len(self.points) < 3:
            return []
        res = []
        for i in range(-2, len(self.points) - 2):
            ptn = [(self.points[i] + self.points[i + 1]) * 0.5, self.points[i + 1],
                   (self.points[i + 1] + self.points[i + 2]) * 0.5]
            res.extend(self.__get_points(ptn, self.count))
        return res


# =======================================================================================
# Функция отрисовки окна команд
# =======================================================================================


def draw_help():
    """функция отрисовки экрана справки программы"""
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = [["F1", "Show Help"], ["R", "Restart"], ["P", "Pause/Play"], ['D', 'Remove Point'],
            ["Num+", "More points"], ["Num-", "Less points"], ["W", "Speed Up"], ["S", "Drop Speed"],
            ["", ""], [str(steps), "Current points"]]
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * i))


# =======================================================================================
# Основная программа
# =======================================================================================
if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    steps = 35
    working = True
    show_help = False
    pause = True
    polyline = Polyline()

    hue = 0
    color = pygame.Color(0)

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    polyline = Polyline()
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0
                if event.key == pygame.K_w:
                    polyline.accelerate()
                if event.key == pygame.K_s:
                    polyline.drop_speed()
                if event.key == pygame.K_d:
                    polyline.drop_point()

            if event.type == pygame.MOUSEBUTTONDOWN:
                polyline.points.append(Vec2d(event.pos[0], event.pos[1]))
                polyline.speeds.append(Vec2d(random.random() * SPEED_SCALAR, random.random() * SPEED_SCALAR))

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        polyline.draw_points()
        knot = Knot(polyline.points, steps)
        curve = Polyline(knot.get_knot())
        curve.draw_points("line", 3, color)

        if not pause:
            polyline.set_points()  # updating points positions
        if show_help:
            draw_help()

        pygame.display.flip()  # swapping buffers

    pygame.display.quit()
    pygame.quit()
    exit(0)
