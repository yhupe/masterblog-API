import json
import os


def load_json_posts(file_path: str) -> list[dict]:
    """Function to load blogposts from the storage. """

    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist. Will return an empty list instead.")
        return []

    try:
        with open(file_path, "r") as fileobj:
            blogposts = json.load(fileobj)

        if not isinstance(blogposts, list):
            print(f"Error: File '{file_path}' does not contain valid json list. Will return empty list instead.")
            return []

        return blogposts

    except json.JSONDecodeError:
        print(f"Error: file '{file_path}' contains invalid JSON. Will return empty list instead")
        return []
    except Exception as e:
        print(f"Unexpected error while loading file '{file_path}': {e}")
        return []


def find_post_by_id(post_id: int, blogposts: list[dict]) -> dict:

    post = next((post for post in blogposts if post.get("id") == post_id), None)
    return post


def save_json_posts(file_path: str, thing_to_save: list[dict]):
    """Function to load blogposts from the storage.
    Returns nothing. """

    try:
        with open(file_path, "w") as fileobj:
            json.dump(thing_to_save, fileobj, indent=4)

    except Exception as e:
        print(f"Error during saving file '{file_path}': {e}")
