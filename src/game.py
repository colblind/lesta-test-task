from random import randint
from typing import List, Tuple, TYPE_CHECKING

from board import Board
from combat import Combat
from constants import Sprite
from core import GameAPI
from obstacles import Cliff, Island
from obstacles.base import Obstacle
from player import Player

from radars import CrossLineRadar, WeakRadar
from ships.base import Ship
from ships import Battleship, Cruiser, Destroyer


if TYPE_CHECKING:
    from core import Image, Marker
    from game_object import GameObject


class Game(object):
    board: Board

    players: List[Player]
    current_player_index: int

    _markers: dict[Ship, "Marker"]
    _images: dict["GameObject", "Image"]

    _game_over: bool

    def __init__(self):
        self.board = Board()
        self.players = []
        self.current_player_index = 0
        self._markers = {}
        self._images = {}
        self._game_over = False

    def start(self, api: GameAPI) -> None:
        self.players = self._create_players()
        self._place_ships()
        self._create_islands()
        self._update_ui(api)

        api.addMessage('Игра началась. {} ходят'.format(self.get_current_player().name))

    def click(self, api: GameAPI, x: int, y: int) -> None:
        if self._game_over:
            return

        current_player = self.get_current_player()
        selected_ship = current_player.get_selected_ship()
        clicked_object = self.board.get_object(x, y)

        if selected_ship:
            initial_pos = '{}{}'.format(chr(65 + selected_ship.position[0]), selected_ship.position[1] + 1)
            final_pos = '{}{}'.format(chr(65 + x), y + 1)

            if (x, y) == selected_ship.position:
                self._unselect_ship(api)
            elif self._move_ship(selected_ship, x, y):
                self._attack_and_change_turn(api)
                api.addMessage('{} ходят {}->{}'.format(current_player.name, initial_pos, final_pos))
            return

        if isinstance(clicked_object, Ship) and clicked_object in self.get_current_player().get_ships():
            self._select_ship(clicked_object, api)

    def _create_players(self) -> List[Player]:
        red_ships = self._create_ships(Sprite.RED_TEAM)
        green_ships = self._create_ships(Sprite.GREEN_TEAM)

        return [
            Player("Красные", red_ships),
            Player("Зеленые", green_ships)
        ]

    def _create_ships(self, team_sprites: Tuple[str]) -> List[Ship]:
        return [
            Destroyer(team_sprites[0], radar=WeakRadar(self.board)),
            Cruiser(team_sprites[1], radar=CrossLineRadar(self.board)),
            Battleship(team_sprites[2], radar=CrossLineRadar(self.board)),
        ]

    def _place_ships(self) -> None:
        initial_positions = [
            [(6, 1), (6, 3), (6, 5)],
            [(0, 1), (0, 3), (0, 5)]
        ]

        for i, player in enumerate(self.players):
            for j, ship in enumerate(player.get_ships()):
                x, y = initial_positions[i][j]

                ship.set_position(x, y)
                self.board.place_object(x, y, ship)

    def _create_islands(self) -> None:
        island_count = randint(5, 15)
        island_sprites = [Sprite.ISLAND, Sprite.CLIFF]
        available_positions = self.board.get_empty_positions()

        for _ in range(island_count):
            if not available_positions:
                break

            position_index = randint(0, len(available_positions) - 1)
            x, y = available_positions.pop(position_index)

            if self.board.is_cell_empty(x, y):
                sprite = island_sprites[randint(0, 1)]
                island = Cliff(sprite) if sprite == Sprite.CLIFF else Island(sprite)
                island.set_position(x, y)
                self.board.place_object(x, y, island)

    def _move_ship(self, ship: Ship, x: int, y: int) -> bool:
        dist = ((x - ship.position[0]) ** 2 + (y - ship.position[1]) ** 2) ** 0.5

        if dist > ship.speed:
            return False

        if not self.board.is_cell_empty(x, y):
            return False

        self.board.clear_cell(ship.position[0], ship.position[1])
        ship.set_position(x, y)
        self.board.place_object(x, y, ship)
        return True

    def _unselect_ship(self, api: GameAPI) -> None:
        self.get_current_player().set_selected_ship(None)
        self._update_ui(api)

    def _select_ship(self, ship: Ship, api: GameAPI) -> None:
        current_player = self.get_current_player()
        current_player.set_selected_ship(ship)

        self._update_ui(api)

        api.addMessage('{} выбирают {}'.format(current_player.name, ship))

    def _attack_and_change_turn(self, api: GameAPI):
        combat = Combat

        enemy_ships = self._get_enemy_ships()

        current_player = self.get_current_player()

        for ship in enemy_ships:
            combat.attack(ship, current_player.get_ships())

        self._remove_dead_ships(api)
        self._check_for_winner(api)
        self._next_player(api)
        self._update_ui(api)

    def _get_enemy_ships(self) -> List[Ship]:
        enemy_index = (self.current_player_index + 1) % len(self.players)
        enemy_ships = self.players[enemy_index].get_ships()

        return enemy_ships

    def _remove_dead_ships(self, api: GameAPI) -> None:
        for player in self.players:
            ships_to_remove = []
            for ship in player.get_ships():
                if not ship.is_alive():
                    ships_to_remove.append(ship)

            for ship in ships_to_remove:
                self.board.clear_cell(ship.position[0], ship.position[1])

                player.remove_ship(ship)

                api.addMessage('{} уничтожен!'.format(ship))

    def _check_for_winner(self, api: GameAPI) -> None:
        for player in self.players:
            if not player.get_ships():
                winner = self.players[(self.players.index(player) + 1) % 2]

                self._game_over = True

                api.addMessage('{} побеждают!'.format(winner.name))

                return

    def _next_player(self, api: GameAPI) -> None:
        if self._game_over:
            return

        self.get_current_player().set_selected_ship(None)
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

        api.addMessage('{} ходят'.format(self.get_current_player().name))

    def get_current_player(self) -> Player:
        return self.players[self.current_player_index]

    def _update_ui(self, api: GameAPI) -> None:
        objects_on_board = set()
        for row in self.board.get_grid():
            for obj in row:
                if obj:
                    objects_on_board.add(obj)

        markers_to_remove = [marker for obj, marker in self._markers.items() if obj not in objects_on_board]
        images_to_remove = [image for obj, image in self._images.items() if obj not in objects_on_board]

        for marker in markers_to_remove:
            marker.remove()
            del self._markers[next(obj for obj, m in self._markers.items() if m == marker)]

        for image in images_to_remove:
            image.remove()
            del self._images[next(obj for obj, m in self._images.items() if m == image)]

        for y, row in enumerate(self.board.get_grid()):
            for x, obj in enumerate(row):
                if obj:
                    if isinstance(obj, Ship):
                        if obj in self._markers:
                            marker = self._markers[obj]
                            marker.moveTo(x, y)
                            marker.setHealth(obj.health / obj.max_health)
                            if obj == self.get_current_player().get_selected_ship():
                                marker.setSelected(True)
                            else:
                                marker.setSelected(False)
                        else:
                            marker = api.addMarker(obj.sprite_path, x, y)
                            marker.setHealth(obj.health / obj.max_health)
                            if obj == self.get_current_player().get_selected_ship():
                                marker.setSelected(True)
                            self._markers[obj] = marker
                    elif isinstance(obj, Obstacle):
                        if obj in self._images:
                            image = self._images[obj]
                            image.setPosition(x, y)
                        else:
                            image = api.addImage(obj.sprite_path, x, y)
                            self._images[obj] = image
