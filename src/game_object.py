from abc import ABC, abstractmethod


class GameObject(ABC):
    @abstractmethod
    def __str__(self):
        pass
