from obstacles.base import Obstacle


class Island(Obstacle):
    def __init__(self, sprite_path: str):
        super().__init__(sprite_path)

    def __str__(self):
        return 'остров'
