import pygame


class BlockType:
    def __init__(self, idblock, sprite):
        self.idblock = idblock
        self.sprite = sprite


class Block(pygame.sprite.Sprite):
    def __init__(self, blocktype, pos):
        super(Block, self).__init__()
        self.blocktype = blocktype
        self.image = pygame.image.load(self.blocktype.sprite)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0] * 32
        self.rect.y = pos[1] * 32
        self.x = pos[0]
        self.y = pos[1]
