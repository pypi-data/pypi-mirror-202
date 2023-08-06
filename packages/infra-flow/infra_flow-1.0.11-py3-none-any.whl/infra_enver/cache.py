import json
import redis
import typing as t
import time


def get_value(db: redis.Redis, key: str) -> t.Any:
    for _ in range(10):
        value = db.get(key)
        if value is not None:
            return json.loads(value.decode("utf-8"))
        time.sleep(1)

    raise KeyError(f"redis key <{key}> not exists")
