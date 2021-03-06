from collections import deque

import pygame

from project.components import GraphicsComponent
from project.core.game import FPS
from project.utils import Direction
from .player_entity import Player


class PlayerGraphicsComponent(GraphicsComponent):
    def __init__(self):
        super().__init__()

        self.frame = 1
        self.idle = deque(self.load_textures('assets/textures/player/idle-0{}.png', 4))
        self.run = deque(self.load_textures('assets/textures/player/run-0{}.png', 6))
        self.jump = tuple(self.load_textures('assets/textures/player/jump-0{}.png', 4))
        self.fall = tuple(self.load_textures('assets/textures/player/fall-0{}.png', 2))

    def update(self, player: Player):
        if player.is_jumping:
            player.image = self.jump[2]
        elif player.velocity.x != 0:
            player.image = self.run[0]
            if self.frame % (FPS // len(self.run)) == 0:  # Evenly spread each animation frame over 1 second
                self.run.rotate(-1)
        elif player.velocity.x == 0:
            # TODO: Idle when colliding left or right
            player.image = self.idle[0]
            if self.frame % (FPS // len(self.idle)) == 0:
                self.idle.rotate(-1)

        # TODO: Not very efficient. Use events or store pre-flipped Surfaces?
        if player.orientation == Direction.LEFT:
            player.image = pygame.transform.flip(player.image, True, False)

        self.frame = (self.frame + 1) % FPS  # Increment frame count; roll over to 1 when frame == FPS
