import json
from pathlib import Path
from typing import Any
from datetime import datetime


def json_encode_hook(obj: Any):
    if isinstance(obj, datetime):
        return {
            'type': 'datetime',
            'value': obj.replace(microsecond=0).astimezone().isoformat()
        }

    return obj


def json_decode_hook(obj: dict):
    if 'type' not in obj:
        return obj

    if obj['type'] == 'datetime':
        return datetime.fromisoformat(obj['value'])

    raise TypeError(f'Unknown state type {obj["type"]}.')


class StateFile:
    _data: dict = {}
    filename: Path

    def __init__(self, filename: Path):
        self.filename = filename

        if not filename.exists():
            self.save()
        else:
            self.load()

    def load(self):
        with self.filename.open('r', encoding='utf-8') as fp:
            self._data = json.load(fp, object_hook=json_decode_hook)

    def save(self):
        with self.filename.open('w', encoding='utf-8') as fp:
            json.dump(self._data, fp, default=json_encode_hook, ensure_ascii=False, indent=4)

    def get(self, key: str, default=None, raise_error=False) -> Any:
        if key not in self._data:
            if raise_error:
                raise KeyError(f'State "{key}" not defined.')

            return default

        return self._data[key]

    def set(self, key: str, value: Any):
        self._data[key] = value
