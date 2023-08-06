import json
import redis
import typing as t


def get_value(db: redis.Redis, key: str) -> t.Any:
    value = db.get(key)
    if value is not None:
        return json.loads(value.decode("utf-8"))

    raise KeyError(f"redis key <{key}> not exists")
