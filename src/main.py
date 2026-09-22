from api import get_move, get_pokemon, get_item
from database import (
    create_database,
    insert_abilities,
    insert_move,
    insert_pokemon,
    insert_pokemon_moves,
    insert_types,
    insert_item
)


def main():
    create_database()

    pokemon = get_pokemon("garchomp")

    print(f"Pokemon: {pokemon['name']}")
    print(f"Moves: {len(pokemon['moves'])}")

    insert_pokemon(pokemon)
    insert_types(pokemon)
    insert_abilities(pokemon)

    for move_data in pokemon["moves"]:
        move_id = int(
            move_data["move"]["url"].rstrip("/").split("/")[-1]
        )

        move = get_move(move_id)

        print(f"Importing move: {move['name']}")

        insert_move(move)

    insert_pokemon_moves(pokemon)

    print(f"Imported: {pokemon['name']}")

    item = get_item("life-orb")

    insert_item(item)

    print(f"Imported item: {item['name']}")


if __name__ == "__main__":
    main()
