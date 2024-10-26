from typing import Any

from package_api.locks.base import BaseLock


class PoetryLock(BaseLock):
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return super().__call__(*args, **kwds)
