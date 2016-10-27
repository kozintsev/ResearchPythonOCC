# coding=utf-8
import math


def math_rez(D, r_min, angle, gamma, alpha):
    """
    Расчёт чего здесь происходит пока не ясно
    :param D: Диаметр
    :param r_min: минимальный радиус резца
    :param angle:
    :param gamma:
    :param alpha:
    :return:
    """
    h_d = r_min * math.sin(gamma)
    h_p = (D / 2) * math.sin(gamma + alpha)
    l = r_min * math.cosh(gamma) + (D / 2) * math.cos(gamma + alpha)
    a = math.sqrt((angle ** 2) - (h_d ** 2))
    r = math.sqrt((h_p ** 2) + ((l - a) ** 2))
    return r
