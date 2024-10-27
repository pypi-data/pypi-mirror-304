import pygame as pg

from game.config import Config, DIR_ASSET
from game.maingame import MainGame


def main():
    config = Config(DIR_ASSET / "config.toml")
    game = MainGame(config=config)
    game.play()
    pg.quit()


if __name__ == "__main__":
    main()
