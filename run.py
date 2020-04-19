#!/usr/local/bin/python3
import os
import sys
from pathlib import Path

from clubsandwich.blt.nice_terminal import terminal
from clubsandwich.director import DirectorLoop

from logic.game_state import GameState
from utils import SCREEN_WIDTH, SCREEN_HEIGHT, BATTLE_WIDTH, BATTLE_HEIGHT, LEVEL_OFFSET, SPACESHIP_OFFSET_5x4, \
    FONT_OFFSET

GAME_ROOT = Path(os.path.abspath(sys.path[1]))
# GAME_ROOT = Path("/Users/eldarbogdanov/sandbox/aliens/")

from scenes import GameScene, CutScene

SCREEN_SIZE = "{}x{}".format(SCREEN_WIDTH, SCREEN_HEIGHT)
TILE_SIZE = "6x6"
FONT_SIZE = "12x18"
FONT = "{root}/assets/NotoMono-Regular.ttf".format(root=GAME_ROOT)
SPACESHIP_TILESET = "{root}/assets/spaceships.png".format(root=GAME_ROOT)
SF_TILESET = "{root}/assets/SF.png".format(root=GAME_ROOT)
NY_TILESET = "{root}/assets/NY.png".format(root=GAME_ROOT)
SCENE_DIMENSIONS = "{}x{}".format(BATTLE_WIDTH, BATTLE_HEIGHT)
SCENE_SIZE = "{}x{}".format(BATTLE_WIDTH * 6, BATTLE_HEIGHT * 6)


class GameLoop(DirectorLoop):
    def terminal_init(self):
        super().terminal_init()

        terminal.set("{}: {}, size={}, align=center, spacing={}".format(
            LEVEL_OFFSET, SF_TILESET, SCENE_SIZE, SCENE_DIMENSIONS
        ))

        terminal.set("{}: {}, size={}, align=center, spacing={}".format(
            LEVEL_OFFSET + 1, NY_TILESET, SCENE_SIZE, SCENE_DIMENSIONS
        ))

        terminal.set("{}: {}, size=60x48, align=center, spacing=10x8".format(
            SPACESHIP_OFFSET_5x4, SPACESHIP_TILESET
        ))

        terminal.set("""
    window.title=Keep it Ali...ens!!!;
    window.size={window_size};
    font: {font}, size={tile_size};
    """.format(window_size=SCREEN_SIZE, font=FONT, tile_size=TILE_SIZE))

        terminal.set("{}: {}, size={}, spacing=2x3".format(FONT_OFFSET, FONT, FONT_SIZE))

    def get_initial_scene(self):
        game_state = GameState()
        return CutScene(game_state)


if __name__ == '__main__':
    GameLoop().run()
