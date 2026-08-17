import pygame

class Image:
    def __init__(self, image_path):
        self.image = pygame.image.load(image_path)
        self.position = [0,0]
        self.size = self.image.get_size()

    def resize(self, size):
        self.size = size

    def draw(self, surface):
        resized_image = pygame.transform.scale(self.image, self.size)
        surface.blit(resized_image, resized_image.get_rect())

    def move(self, position):
        self.position = position