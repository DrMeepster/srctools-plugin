import sys, argparse

from typing import List

from srctools import Property
from srctools.game import Game

from pathlib import Path

GAMECONFIG = "GameConfig.txt"

def find_gameconfig(game: Game) -> Property:
    path = game.bin_folder() / ".." / GAMECONFIG

    print(f"Found game config at {path.resolve()}")

    with open(path) as f:
        return Property.parse(f)

FGD = "srctools_fgdfix.fgd"

HEADER = """// This FGD is automatically generated.
// Any changes will be overwritten.
"""

def write_fgd(game: Game, fgds: List[str]) -> None:
    path = game.bin_folder() / ".." / FGD

    print(f"Writing to {path.resolve()}")

    with open(path, "w") as f:
        f.write(HEADER)
        f.writelines(f'@include "{fgd}"\n' for fgd in fgds)

    if game.bin_folder() / ".." / game.fgd_loc != path: #TODO: doesnt check right in p2 because of dlc paths
        print("Note: 'srctools_fgdfix.fgd' not set as FGD in your gameinfo")

def main(argv: List[str]) -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--chaos",
        action="store_true",
    )

    parser.add_argument(
        "--set-fgd",
        action="store_true",
    )

    parser.add_argument(
        "--config",
    )

    parser.add_argument(
        "game",
    )

    result = parser.parse_args(argv)

    game = Game(result.game)

    if result.chaos:
        raise RuntimeError("P2CE/Chaos Engine support not added yet")
    else:
        gc = find_gameconfig(game)

    configs = gc.find_key("Configs").find_key("Games")

    if len(configs) == 0:
        raise ValueError("No game configurations in GameConfig.txt!")
    elif len(configs) == 1:
        config_name = list(configs)[0].name
    elif result.config:
        config_name = result.config
    else:
        raise ValueError(f"Multiple game configurations: {[prop.real_name for prop in configs]}, Use --config to specify")

    print(f"Using config '{config_name}'")

    config = configs.find_key(config_name)

    fgds = [str(p.value) for p in config.find_key("Hammer") if p.name.startswith("gamedata")]

    fgds.sort() # fgds are loaded by hammer in alphabetical order, we want to copy that

    print("Found FGDs:")
    for fgd in fgds:
        print(f" * {fgd}")

    write_fgd(game, fgds)

    print("Done!")

if __name__ == '__main__':
    main(sys.argv[1:])