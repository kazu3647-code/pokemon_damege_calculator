import sqlite3


DB_PATH = "data/pokemon.db"


with sqlite3.connect(DB_PATH) as conn:
    print("=== pokemon ===")
    for row in conn.execute("SELECT * FROM pokemon"):
        print(row)

    print("\n=== types ===")
    for row in conn.execute("SELECT * FROM types"):
        print(row)

    print("\n=== abilities ===")
    for row in conn.execute("SELECT * FROM abilities"):
        print(row)

    print("\n=== moves ===")
    for row in conn.execute("""
        SELECT id, name, type_id, category, power
        FROM moves
        LIMIT 20
    """):
        print(row)

    print("\n=== pokemon_moves ===")
    for row in conn.execute("""
        SELECT pokemon_id, move_id
        FROM pokemon_moves
        LIMIT 20
    """):
        print(row)
