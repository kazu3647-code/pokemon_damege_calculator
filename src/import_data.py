import time

from api import get_all_resources, get_item, get_move, get_pokemon
from database import (
    create_database,
    insert_abilities,
    insert_item,
    insert_move,
    insert_pokemon,
    insert_pokemon_moves,
    insert_types,
    pokemon_exists,
)


REQUEST_INTERVAL = 0.1


def wait():
    time.sleep(REQUEST_INTERVAL)


def get_id_from_url(url: str) -> int:
    return int(url.rstrip("/").split("/")[-1])


def import_pokemon():
    print("=== Importing Pokémon ===")

    pokemon_list = get_all_resources("pokemon")

    print(f"Found {len(pokemon_list)} Pokémon.")

    # 名前 → ID
    pokemon_ids = {
        pokemon["name"]: get_id_from_url(pokemon["url"])
        for pokemon in pokemon_list
    }
    for index, pokemon_data in enumerate(pokemon_list, start=1):
        pokemon_id = get_id_from_url(pokemon_data["url"])

        if pokemon_exists(pokemon_id):
            print(
                f"[{index}/{len(pokemon_list)}] "
                f"{pokemon_data['name']} - SKIP"
            )
            continue

        print(
            f"[{index}/{len(pokemon_list)}] "
            f"{pokemon_data['name']}"
        )

        pokemon = get_pokemon(pokemon_id)
        wait()

        base_pokemon_id = get_base_pokemon_id(
            pokemon["name"],
            pokemon_ids,
        )

        insert_pokemon(
            pokemon,
            base_pokemon_id=base_pokemon_id,
        )

        insert_types(pokemon)
        insert_abilities(pokemon)
        insert_pokemon_moves(pokemon)
    print("Pokémon import completed.")


def get_base_pokemon_id(
    pokemon_name: str,
    pokemon_ids: dict[str, int],
) -> int | None:

    if "-mega" not in pokemon_name:
        return None

    base_name = pokemon_name.split("-mega")[0]

    return pokemon_ids.get(base_name)


def import_moves():
    print("\n=== Importing Moves ===")

    move_list = get_all_resources("move")

    print(f"Found {len(move_list)} moves.")

    for index, move_data in enumerate(move_list, start=1):
        move_id = get_id_from_url(move_data["url"])

        print(
            f"[{index}/{len(move_list)}] "
            f"{move_data['name']}"
        )

        move = get_move(move_id)
        wait()

        insert_move(move)

    print("Move import completed.")


def import_items():
    print("\n=== Importing Items ===")

    item_list = get_all_resources("item")

    print(f"Found {len(item_list)} items.")

    for index, item_data in enumerate(item_list, start=1):
        item_id = get_id_from_url(item_data["url"])

        print(
            f"[{index}/{len(item_list)}] "
            f"{item_data['name']}"
        )

        item = get_item(item_id)
        wait()

        insert_item(item)

    print("Item import completed.")


def main():
    create_database()

    import_pokemon()
    import_moves()
    import_items()

    print("\n=== Import completed ===")


if __name__ == "__main__":
    main()
