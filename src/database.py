import sqlite3
from pathlib import Path


DB_PATH = Path("data/pokemon.db")


def pokemon_exists(pokemon_id: int) -> bool:
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute(
            "SELECT 1 FROM pokemon WHERE id = ?",
            (pokemon_id,),
        ).fetchone()

    return row is not None


def create_database():
    DB_PATH.parent.mkdir(exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS pokemon (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                base_pokemon_id INTEGER,

                hp INTEGER NOT NULL,
                attack INTEGER NOT NULL,
                defense INTEGER NOT NULL,
                special_attack INTEGER NOT NULL,
                special_defense INTEGER NOT NULL,
                speed INTEGER NOT NULL,

                FOREIGN KEY (base_pokemon_id)
                    REFERENCES pokemon(id)
            );

            CREATE TABLE IF NOT EXISTS types (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE
            );

            CREATE TABLE IF NOT EXISTS pokemon_types (
                pokemon_id INTEGER NOT NULL,
                type_id INTEGER NOT NULL,

                PRIMARY KEY (pokemon_id, type_id),

                FOREIGN KEY (pokemon_id)
                    REFERENCES pokemon(id),

                FOREIGN KEY (type_id)
                    REFERENCES types(id)
            );

            CREATE TABLE IF NOT EXISTS abilities (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE
            );

            CREATE TABLE IF NOT EXISTS pokemon_abilities (
                pokemon_id INTEGER NOT NULL,
                ability_id INTEGER NOT NULL,

                PRIMARY KEY (pokemon_id, ability_id),

                FOREIGN KEY (pokemon_id)
                    REFERENCES pokemon(id),

                FOREIGN KEY (ability_id)
                    REFERENCES abilities(id)
            );

            CREATE TABLE IF NOT EXISTS moves (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                type_id INTEGER NOT NULL,
                category TEXT NOT NULL,
                power INTEGER,

                FOREIGN KEY (type_id)
                    REFERENCES types(id)
            );

            CREATE TABLE IF NOT EXISTS pokemon_moves (
                pokemon_id INTEGER NOT NULL,
                move_id INTEGER NOT NULL,

                PRIMARY KEY (pokemon_id, move_id),

                FOREIGN KEY (pokemon_id)
                    REFERENCES pokemon(id),

                FOREIGN KEY (move_id)
                    REFERENCES moves(id)
            );
                           
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE
            );
        """)

        conn.commit()


def insert_pokemon(pokemon: dict, base_pokemon_id: int | None = None):
    stats = {
        stat["stat"]["name"]: stat["base_stat"]
        for stat in pokemon["stats"]
    }

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT OR REPLACE INTO pokemon (
                id,
                name,
                base_pokemon_id,
                hp,
                attack,
                defense,
                special_attack,
                special_defense,
                speed
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            pokemon["id"],
            pokemon["name"],
            base_pokemon_id,
            stats["hp"],
            stats["attack"],
            stats["defense"],
            stats["special-attack"],
            stats["special-defense"],
            stats["speed"],
        ))

        conn.commit()

def insert_types(pokemon: dict):
    with sqlite3.connect(DB_PATH) as conn:
        for type_data in pokemon["types"]:
            type_id = int(
                type_data["type"]["url"].rstrip("/").split("/")[-1]
            )

            type_name = type_data["type"]["name"]

            conn.execute("""
                INSERT OR IGNORE INTO types (
                    id,
                    name
                )
                VALUES (?, ?)
            """, (
                type_id,
                type_name,
            ))

            conn.execute("""
                INSERT OR IGNORE INTO pokemon_types (
                    pokemon_id,
                    type_id
                )
                VALUES (?, ?)
            """, (
                pokemon["id"],
                type_id,
            ))

        conn.commit()


def insert_abilities(pokemon: dict):
    with sqlite3.connect(DB_PATH) as conn:
        for ability_data in pokemon["abilities"]:
            ability_id = int(
                ability_data["ability"]["url"].rstrip("/").split("/")[-1]
            )

            ability_name = ability_data["ability"]["name"]

            conn.execute("""
                INSERT OR IGNORE INTO abilities (
                    id,
                    name
                )
                VALUES (?, ?)
            """, (
                ability_id,
                ability_name,
            ))

            conn.execute("""
                INSERT OR IGNORE INTO pokemon_abilities (
                    pokemon_id,
                    ability_id
                )
                VALUES (?, ?)
            """, (
                pokemon["id"],
                ability_id,
            ))

        conn.commit()


def insert_move(move: dict):
    type_id = int(
        move["type"]["url"].rstrip("/").split("/")[-1]
    )

    category = move["damage_class"]["name"]

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT OR REPLACE INTO moves (
                id,
                name,
                type_id,
                category,
                power
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            move["id"],
            move["name"],
            type_id,
            category,
            move["power"],
        ))

        conn.commit()


def insert_pokemon_moves(pokemon: dict):
    with sqlite3.connect(DB_PATH) as conn:
        for move_data in pokemon["moves"]:
            move_id = int(
                move_data["move"]["url"].rstrip("/").split("/")[-1]
            )

            conn.execute("""
                INSERT OR IGNORE INTO pokemon_moves (
                    pokemon_id,
                    move_id
                )
                VALUES (?, ?)
            """, (
                pokemon["id"],
                move_id,
            ))

        conn.commit()


def insert_item(item: dict):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT OR REPLACE INTO items (
                id,
                name
            )
            VALUES (?, ?)
        """, (
            item["id"],
            item["name"],
        ))

        conn.commit()
