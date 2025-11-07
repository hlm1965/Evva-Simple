"""
Example usage of the Evva-Simple library
"""

import logging
from evva_simple import EvvaClient, EvvaAPIError

# Enable logging to see what's happening
logging.basicConfig(level=logging.INFO)


def main():
    # Initialize the client with your API key
    api_key = "your-api-key-here"
    client = EvvaClient(api_key=api_key)

    try:
        # List all locks
        print("Fetching locks...")
        locks = client.list_locks(limit=10)
        print(f"Found {len(locks)} locks")
        for lock in locks:
            print(f"  - {lock.get('name', 'Unnamed')}: {lock.get('id')}")

        # List all persons
        print("\nFetching persons...")
        persons = client.list_persons(limit=10)
        print(f"Found {len(persons)} persons")
        for person in persons:
            print(
                f"  - {person.get('firstName')} {person.get('lastName')}: {person.get('id')}"
            )

        # Create a new person (commented out to avoid accidental creation)
        # print("\nCreating a new person...")
        # new_person = client.create_person(
        #     first_name="John",
        #     last_name="Doe",
        #     email="john.doe@example.com",
        #     phone="+1234567890"
        # )
        # print(f"Created person with ID: {new_person.get('id')}")

        # List access media
        print("\nFetching access media...")
        media = client.list_media(limit=10)
        print(f"Found {len(media)} access media")
        for medium in media:
            print(f"  - {medium.get('type')}: {medium.get('id')}")

        # Create an authorization (example - adjust IDs as needed)
        # print("\nCreating an authorization...")
        # authorization = client.create_authorization(
        #     medium_id="medium-id-here",
        #     lock_id="lock-id-here",
        #     valid_from="2025-11-07T08:00:00Z",
        #     valid_to="2025-11-07T22:00:00Z"
        # )
        # print(f"Created authorization with ID: {authorization.get('id')}")

    except EvvaAPIError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
