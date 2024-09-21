import json
from typing import Any
from pathlib import Path
from dataclasses import field, dataclass


ENCODING = "utf-8"


@dataclass
class BaseDAO:
    """Base DAO class that provides common methods for data access."""
    file_name: Path = field(default_factory=lambda: Path(__file__).parent / "aggregated_data.json")
    _data: dict[str, Any] = field(default_factory=dict, init=False)
    model_name: str = field(init=False)
    other_model_names: list[str] = field(default_factory=list, init=False)

    @property
    def data(self) -> dict[str, Any]:
        """Get the data for this model."""
        if not self._data:
            self.load_data()
        return self._data.get(self.model_name, {})

    def load_data(self) -> None:
        """Load data from the file."""
        try:
            with open(self.file_name, encoding=ENCODING) as f:
                self._data = json.load(f)
        except FileNotFoundError:
            self._data = {}

    def _save_data(self) -> None:
        """Save the updated model data to the file."""
        try:
            with open(self.file_name, encoding=ENCODING) as f:
                all_data = json.load(f)
        except FileNotFoundError:
            all_data = {}

        for model in self.other_model_names:
            if model not in all_data:
                all_data[model] = {}

        all_data[self.model_name] = self._data[self.model_name]

        with open(self.file_name, "w", encoding=ENCODING) as f:
            json.dump(all_data, f, indent=2)

    def insert(self, data: dict[str, Any] | list[dict[str, Any]]) -> None:
        """Insert a new item or items into the data."""
        self.load_data()  # Ensure we have the latest data

        if self.model_name not in self._data:
            self._data[self.model_name] = {}

        existing_keys = set(map(int, self._data[self.model_name].keys()))
        if isinstance(data, list):
            for item in data:
                new_id = str(max(existing_keys, default=0) + 1)
                self._data[self.model_name][new_id] = item
                existing_keys.add(int(new_id))
        else:
            new_id = str(max(existing_keys, default=0) + 1)
            self._data[self.model_name][new_id] = data

        self._save_data()

    def get_all(self) -> list[dict[str, Any]]:
        """Get all items from the data."""
        return list(self._data[self.model_name].values())

    def get_by_id(self, hashmap_key: str) -> dict[str, Any] | None:
        """Get an item by id."""
        item = self._data[self.model_name].get(hashmap_key)

        if item is None:
            for value in self._data[self.model_name].values():
                if str(value.get("id")) == hashmap_key:
                    return value

        return item

    def filter_items(self, **kwargs) -> list[dict[str, Any]]:
        """Filter items by the given criteria."""
        return [{"id": key, **item} for key, item in self.data.items()
                if all(item.get(k) == v for k, v in kwargs.items())]

    def update(self, hashmap_key: str, **kwargs) -> dict[str, Any] | None:
        """Update an item by hashmap_key."""
        if hashmap_key in self._data[self.model_name]:
            self._data[self.model_name][hashmap_key].update(kwargs)
            self._save_data()
            return self._data[self.model_name][hashmap_key]
        return None

    def delete(self, hashmap_key: str) -> bool:
        """Delete an item by hashmap_key."""
        if hashmap_key in self._data[self.model_name]:
            del self._data[self.model_name][hashmap_key]
            self._save_data()
            return True
        return False
