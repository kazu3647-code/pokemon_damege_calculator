import time

import httpx


BASE_URL = "https://pokeapi.co/api/v2"

TIMEOUT = 30.0
MAX_RETRIES = 2


def get_resource(resource: str, resource_id: int | str) -> dict:
    url = f"{BASE_URL}/{resource}/{resource_id}"

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = httpx.get(
                url,
                timeout=TIMEOUT,
            )
            response.raise_for_status()

            return response.json()

        except httpx.RequestError as e:
            print(
                f"Request failed "
                f"({attempt}/{MAX_RETRIES}): {e}"
            )

            if attempt == MAX_RETRIES:
                raise

            time.sleep(attempt)


def get_pokemon(name_or_id: str | int) -> dict:
    return get_resource("pokemon", name_or_id)


def get_move(name_or_id: str | int) -> dict:
    return get_resource("move", name_or_id)


def get_item(name_or_id: str | int) -> dict:
    return get_resource("item", name_or_id)


def get_all_resources(resource: str) -> list[dict]:
    results = []
    offset = 0
    limit = 100

    while True:
        response = httpx.get(
            f"{BASE_URL}/{resource}",
            params={
                "limit": limit,
                "offset": offset,
            },
            timeout=TIMEOUT,
        )
        response.raise_for_status()

        data = response.json()

        results.extend(data["results"])

        if data["next"] is None:
            break

        offset += limit

    return results