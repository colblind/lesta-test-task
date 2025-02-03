from abc import ABC, abstractmethod


class GameObject(ABC):
    sprite_path: str

    def __init__(self, sprite_path: str):
        self.sprite_path = sprite_path

    @abstractmethod
    def __str__(self):
        pass
