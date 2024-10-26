from typing import Any


class BaseCollector(object):
    """Базовый коллектор для определения версии."""

    def collect(self) -> None | str: ...

    def data(self) -> None | dict[str, Any]: ...
