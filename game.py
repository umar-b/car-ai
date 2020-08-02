import pygame
from pygame.math import Vector2
import math
import os


class Car:
    def __init__(self, x, y):
        self.pos = Vector2(x, y)
        self.speed = 0.0
        self.angle = 0.0
        self.distance = 0
        self.time_spent = 0

    def update(self, dt):
        self.pos += ((math.cos(math.radians(360 - self.angle)) * self.speed) * dt,
                     (math.sin(math.radians(360 - self.angle)) * self.speed) * dt)

        self.distance += self.speed
        self.time_spent += 1

        if self.pos[0] < 20:
            self.pos[0] = 20
        elif self.pos[0] > 1280 - 120:
            self.pos[0] = 1280 - 120

        if self.pos[1] < 20:
            self.pos[1] = 20
        elif self.pos[1] > 720 - 120:
            self.pos[1] = 720 - 120


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Car AI")
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.car = Car(0, 0)
        self.ticks = 128
        self.exit = False

    def run(self):
        resources_dir = os.path.realpath("./resources")
        image_path = os.path.join(resources_dir, "car_small.png")
        car_image = pygame.image.load(image_path)
        while not self.exit:
            dt = self.clock.get_time() / 100

            # Event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            # User input
            pressed = pygame.key.get_pressed()

            if pressed[pygame.K_UP]:
                if self.car.speed > 10:
                    self.car.speed = 10
                elif self.car.speed < 1:
                    self.car.speed = 1
                else:
                    self.car.speed += 2 * dt

            if pressed[pygame.K_DOWN]:
                if self.car.speed < -10:
                    self.car.speed = -10
                else:
                    self.car.speed -= 1 * dt

            if pressed[pygame.K_RIGHT]:
                self.car.angle -= 0.5
            elif pressed[pygame.K_LEFT]:
                self.car.angle += 0.5

            # Logic
            self.car.update(dt)

            # Drawing
            self.screen.fill((0, 0, 0))
            rotated = pygame.transform.rotate(car_image, self.car.angle)
            self.screen.blit(rotated, self.car.pos)
            pygame.display.flip()
            self.clock.tick(self.ticks)
            print("Time spent: " + str(self.car.time_spent), end="\r")
            print("Distance: " + str(self.car.distance), end="\r")
            print("Speed: " + str(self.car.speed), end="\r", flush=True)
        pygame.quit()
