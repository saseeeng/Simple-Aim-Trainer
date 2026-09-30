import random
import time
import pygame


class Target:
    def __init__(self, width, height, radius=30, lifetime=4.0):
        self.width = width
        self.height = height
        self.radius = radius
        self.lifetime = lifetime
        self.x = 0
        self.y = 0
        self.created_at = time.monotonic()
        self.move()

    def move(self):
        self.x = random.randint(self.radius, self.width - self.radius)
        self.y = random.randint(self.radius + 80, self.height - self.radius)
        self.created_at = time.monotonic()

    def is_expired(self):
        return time.monotonic() - self.created_at >= self.lifetime

    def is_clicked(self, mouse_x, mouse_y):
        distance_squared = (mouse_x - self.x) ** 2 + (mouse_y - self.y) ** 2
        return distance_squared <= self.radius ** 2

    def draw(self, screen):
        age = time.monotonic() - self.created_at
        alpha = max(0, int(255 * (1 - age / self.lifetime)))
        size = self.radius * 2
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        center = (self.radius, self.radius)

        pygame.draw.circle(surface, (220, 50, 50, alpha), center, self.radius)
        pygame.draw.circle(
            surface, (245, 245, 245, alpha), center, int(self.radius * 0.6)
        )
        pygame.draw.circle(
            surface, (220, 50, 50, alpha), center, int(self.radius * 0.3)
        )
        pygame.draw.circle(surface, (30, 30, 30, alpha), center, 3)

        screen.blit(surface, (self.x - self.radius, self.y - self.radius))