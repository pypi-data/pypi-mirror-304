from typing import Dict, Any
from .base_code_block import BaseCodeBlock


class DataStorage(BaseCodeBlock):
    """
    Extends BaseCodeBlock. This class manages data storage operations.
    """
    # A dictionary used for storing data items.
    store: Dict[str, Any]

    def __init__(self):
        """Initialize the datastore with an empty dictionary."""
        self.store = {}

    def create(self, key: str, value: Any):
        """Create a new item in the datastore."""
        if key in self.store:
            raise ValueError("Key already exists.")
        self.store[key] = value

    def retrieve(self, key: str):
        """Retrieve an item from the datastore."""
        return self.store.get(key, None)

    def update(self, key: str, value: Any):
        """Update an existing item in the datastore."""
        if key not in self.store:
            raise ValueError("Key does not exist.")
        self.store[key] = value

    def delete(self, key: str):
        """Delete an item from the datastore."""
        if key in self.store:
            del self.store[key]

    def list_all(self):
        """List all items in the datastore."""
        return self.store
