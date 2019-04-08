import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super(Player, self).__init__()
        self.x = pos[0]
        self.y = pos[1]
        self.image = pygame.image.load("images/player.png")
        self.rect = self.image.get_rect()
        self.rect.x = pos[0] * 32
        self.rect.y = pos[1] * 32
