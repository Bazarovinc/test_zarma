import json
from typing import Final

from httpx import Client

URL: Final[str] = "https://jsonplaceholder.typicode.com/posts"


class HTTPException(Exception):
    def __init__(self, status_code: int, content: str | bytes):
        message = f"Ответ не получен. Status code: {status_code}, msg: {content}"
        super().__init__(message)


def get_json() -> bytes:
    with Client() as http_client:
        response = http_client.get(URL)
        if response.status_code == 200:
            return response.content
        else:
            raise HTTPException(response.status_code, response.content)


def save_json_to_file(data: bytes) -> None:
    with open("response.json", "w") as file:
        json.dump(json.loads(data.decode("utf-8")), file, indent=4)


def main():
    save_json_to_file(get_json())


if __name__ == "__main__":
    main()
