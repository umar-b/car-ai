import pygame
from pygame.math import Vector2
import math
import os


class Car:
    def __init__(self, x, y, car_image, track):
        self.car_image = car_image
        self.track = track
        self.rotated = car_image
        self.pos = Vector2(x, y)
        self.speed = 0.0
        self.angle = 0.0
        self.distance = 0
        self.time_spent = 0

    # rotate the image from the center

    def draw(self, screen):
        blitRotate(screen, self.car_image, self.pos,
                   (self.car_image.get_rect().width/2, self.car_image.get_rect().height/2), self.angle)

    def update(self, dt):

        # deceleration and speed limits
        self.speed -= 0.5 * dt
        if self.speed > 15:
            self.speed = 15
        if self.speed < 1:
            self.speed = 0

        # update position
        self.pos.x += (math.cos(math.radians(-self.angle)) * self.speed) * dt
        self.pos.y += (math.sin(math.radians(-self.angle)) * self.speed) * dt

        # log distance and time
        self.distance += self.speed
        self.time_spent += 1


class Game:
    def __init__(self):
        pygame.init()

        # load paths
        resources_dir = os.path.realpath("./resources")
        map_path = os.path.join(resources_dir, "Track.jpg")
        image_path = os.path.join(resources_dir, "car_small.png")

        # load images
        map_image = pygame.image.load(map_path)
        car_image = pygame.image.load(image_path)

        pygame.display.set_caption("Car AI")

        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.car = Car(0, 0, car_image, map_image)
        self.ticks = 128  # 128 ticks smoother than 64??
        self.exit = False

    def run(self):
        while not self.exit:
            dt = self.clock.get_time() / 100

            # Event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            # User input
            pressed = pygame.key.get_pressed()

            if pressed[pygame.K_UP]:
                self.car.speed += 10 * dt

            if pressed[pygame.K_RIGHT]:
                self.car.angle -= 15 * dt
            elif pressed[pygame.K_LEFT]:
                self.car.angle += 15 * dt

            self.car.update(dt)

            # Drawing
            self.screen.blit(self.car.track, (0, 0))
            self.car.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(self.ticks)
            # print("Time spent: " + str(self.car.time_spent), end="\r", flush=True)
            # print("Distance: " + str(self.car.distance), end="\r", flush=True)
            # print("Speed: " + str(self.car.speed), end="\r", flush=True)
        pygame.quit()

# function for rotating image from stackoverflow


def blitRotate(surf, image, pos, originPos, angle):

    # calcaulate the axis aligned bounding box of the rotated image
    w, h = image.get_size()
    box = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
    box_rotate = [p.rotate(angle) for p in box]
    min_box = (min(box_rotate, key=lambda p: p[0])[
               0], min(box_rotate, key=lambda p: p[1])[1])
    max_box = (max(box_rotate, key=lambda p: p[0])[
               0], max(box_rotate, key=lambda p: p[1])[1])

    # calculate the translation of the pivot
    pivot = pygame.math.Vector2(originPos[0], -originPos[1])
    pivot_rotate = pivot.rotate(angle)
    pivot_move = pivot_rotate - pivot

    # calculate the upper left origin of the rotated image
    origin = (pos[0] - originPos[0] + min_box[0] - pivot_move[0],
              pos[1] - originPos[1] - max_box[1] + pivot_move[1])

    # get a rotated image
    rotated_image = pygame.transform.rotate(image, angle)

    # rotate and blit the image
    surf.blit(rotated_image, origin)

    # draw rectangle around the image
    # pygame.draw.rect(surf, (255, 0, 0),
    #                  (*origin, *rotated_image.get_size()), 2)
