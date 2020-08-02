import pygame
import sys
import math
import random
import numpy as np
import scipy as sc
from scipy.spatial import ConvexHull
from scipy import interpolate
import argparse
import json

# read json file
with open('settings.json', 'r') as file:
    data = file.read()

# parse the file
obj = json.loads(data)


def gen_points(min=int(obj["min_points"]), max=int(obj["max_points"]), margin=int(obj["margin"]), min_distance=int(obj["min_distance"])):
    point_count = random.randrange(min, max+1, 1)
    points = []
    for i in range(point_count):
        x = random.randrange(margin, 1280 - margin + 1, 1)
        y = random.randrange(margin, 720 - margin + 1, 1)
        distances = list(filter(lambda x: x < min_distance, [
                         math.sqrt((p[0]-x)**2 + (p[1]-y)**2) for p in points]))
        if len(distances) == 0:
            points.append((x, y))
    return np.array(points)


def get_convexHull_points(points):
    hull = ConvexHull(points)
    return hull.points


def push_apart(points, distance):
    for i in range(len(points)):
        for j in range(i+1, len(points)):
            point_distance = math.sqrt((points[i][0]-points[j][0])**2 +
                                       (points[i][1]-points[j][1])**2)
            if point_distance < distance:
                dx = points[j][0] - points[i][0]
                dy = points[j][1] - points[i][1]
                dl = math.sqrt(dx*dx + dy*dy)
                dx /= dl
                dy /= dl
                dif = distance - dl
                dx *= dif
                dy *= dif
                points[j][0] = int(points[j][0] + dx)
                points[j][1] = int(points[j][1] + dy)
                points[i][0] = int(points[i][0] - dx)
                points[i][1] = int(points[i][1] - dy)
    return points


def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    screen.fill([58, 156, 53])

    pygame.display.set_caption("Track")
    while True:  # main loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()


if __name__ == "__main__":
    main()
