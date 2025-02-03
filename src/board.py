from constants import GRID_SIZE
from typing import List, Tuple


class Board:
    def __init__(self):
        self._grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    def place_object(self, x: int, y: int, obj: object) -> None:
        self._grid[y][x] = obj

    def get_object(self, x: int, y: int) -> object:
        return self._grid[y][x]

    def is_cell_empty(self, x: int, y: int) -> bool:
        return self._grid[y][x] is None

    def get_neighbors(self, x: int, y: int) -> List[Tuple[int, int]]:
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                    neighbors.append((nx, ny))
        return neighbors

    def get_all_positions(self) -> List[Tuple[int, int]]:
        positions = []
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                positions.append((x, y))
        return positions

    def get_grid(self) -> List[List[object]]:
        return self._grid

    def clear_cell(self, x: int, y: int) -> None:
        self._grid[y][x] = None
