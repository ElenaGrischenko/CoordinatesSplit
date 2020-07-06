from parameters import delta, step, R
from numpy import pi, cos, sin, tan
import numpy as np


def point(temp, x1, y1, x2, y2, find):
    k = float(y1 - y2) / (x1 - x2)
    b = y2 - k * x2
    if find == 'y':
        return k * temp + b
    elif find == 'x':
        return float((temp - b) / k)


def radFromGrad(grad):
    return grad * pi / 180


def find_vertex_coordinates(coordinates):
    points_x, points_y = [], []
    x_line = coordinates[:, 0].min()
    xx, xy = [], []
    while x_line <= coordinates[:, 0].max():
        idx, tempY = [], []
        for i in range(0, coordinates.shape[0] - 1):
            if coordinates[i, 0] < x_line < coordinates[i + 1, 0] or coordinates[i, 0] > x_line > coordinates[
                i + 1, 0] or coordinates[i, 0] == x_line:
                idx.append(i)
        for i in idx:
            if coordinates[i, 0] == x_line:
                tempY.append(coordinates[i, 1])
            else:
                tempY.append(
                    point(x_line, coordinates[i, 0], coordinates[i, 1], coordinates[i + 1, 0], coordinates[i + 1, 1],
                          'y'))
        if len(tempY) == 1:
            xx.extend([x_line] * 2)
            xy.extend(tempY * 2)
        elif len(tempY) % 2 == 0:
            tempY.sort()
            xx.extend([x_line] * len(tempY))
            xy.extend(tempY)
        elif len(tempY) > 1 and len(tempY) % 2 == 1:
            PlusDelta, MinusDelta = [], []
            for i in range(0, coordinates.shape[0] - 1):
                if coordinates[i, 0] < x_line + delta < coordinates[i + 1, 0] or coordinates[i, 0] > x_line + delta > \
                        coordinates[i + 1, 0] or coordinates[i, 0] == x_line + delta:
                    PlusDelta.append(i)
                elif coordinates[i, 0] < x_line - delta < coordinates[i + 1, 0] or coordinates[i, 0] > x_line - delta > \
                        coordinates[i + 1, 0] or coordinates[i, 0] == x_line - delta:
                    MinusDelta.append(i)
            if len(PlusDelta) > len(tempY):
                i = 0
                while i < len(tempY):
                    if idx[i] != PlusDelta[i] and idx[i] == PlusDelta[i + 1]:
                        if tempY[i] == max(tempY) or tempY[i] == min(tempY):
                            xx.extend([x_line] * 2)
                            xy.extend([tempY[i]] * 2)
                            i += 1
                        else:
                            xx.extend([x_line] * 4)
                            xy.extend([tempY[i - 1], tempY[i], tempY[i], tempY[i + 1]])
                            i += 2
                    elif idx[i] == PlusDelta[i] and idx[i + 1] == PlusDelta[i + 1]:
                        xx.extend([x_line] * 2)
                        xy.extend([tempY[i], tempY[i + 1]])
                        i += 2
                    elif idx[i] == PlusDelta[i] and idx[i + 1] != PlusDelta[i + 1]:
                        i += 1
            else:
                i = 0
                while i < len(tempY):
                    if idx[i] != MinusDelta[i] and idx[i] == MinusDelta[i + 1]:
                        if idx[i] != PlusDelta[i] and idx[i] == PlusDelta[i + 1]:
                            xx.extend([x_line] * 2)
                            xy.extend([tempY[i]] * 2)
                            i += 1
                        else:
                            xx.extend([x_line] * 4)
                            xy.extend([tempY[i - 1], tempY[i], tempY[i], tempY[i + 1]])
                            i += 2
                    elif idx[i] == MinusDelta[i] and idx[i + 1] == MinusDelta[i + 1]:
                        xx.extend([x_line] * 2)
                        xy.extend([tempY[i], tempY[i + 1]])
                        i += 2
                    elif idx[i] == MinusDelta[i] and idx[i + 1] != MinusDelta[i + 1]:
                        i += 1
        x_line += step

    Yline = coordinates[:, 1].min()
    while Yline <= coordinates[:, 1].max():
        for i in range(0, len(xx), 2):
            if xy[i] <= Yline <= xy[i + 1] or xy[i] >= Yline >= xy[i + 1]:
                points_x.append(xx[i])
                points_y.append(Yline)
        Yline += step

    return points_x, points_y


def sectors(points_x, points_y):
    sector_x, sector_y = [], []
    alpha = radFromGrad(30)
    for i in range(len(points_x)):
        x0 = points_x[i]
        y0 = points_y[i]
        sector_x.extend([x0, x0, x0, x0 + R * cos(alpha), x0, x0 - R * cos(alpha)])
        sector_y.extend([y0, y0 + R, y0, y0 - R * sin(alpha), y0, y0 - R * sin(alpha)])

    return sector_x, sector_y


def one_sector(x0, y0):
    sector_x, sector_y = [], []
    alpha = radFromGrad(30)
    sector_x.extend([x0, x0, x0, x0 + R * cos(alpha), x0, x0 - R * cos(alpha)])
    sector_y.extend([y0, y0 + R, y0, y0 - R * sin(alpha), y0, y0 - R * sin(alpha)])

    return sector_x, sector_y


def vertex_belonging_sector(x0, y0, points_x, points_y):
    k1 = tan(radFromGrad(150))
    b1 = y0 - k1 * x0

    k2 = tan(radFromGrad(30))
    b2 = y0 - k2 * x0

    sector1, sector2, sector3 = [], [], []
    for i in range(0, len(points_x)):
        x, y = points_x[i], points_y[i]
        if pow(x - x0, 2) + pow(y - y0, 2) <= pow(R, 2):
            if y >= k1 * x + b1 and x >= x0:
                sector1.append((points_x[i], points_y[i]))
            if y <= k1 * x + b1 and y <= k2 * x + b2:
                sector2.append((points_x[i], points_y[i]))
            if y >= k2 * x + b2 and x <= x0:
                sector3.append((points_x[i], points_y[i]))

    return np.array(sector1), np.array(sector2), np.array(sector3)
