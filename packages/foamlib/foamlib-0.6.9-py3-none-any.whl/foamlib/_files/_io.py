import gzip
import sys
from copy import deepcopy
from pathlib import Path
from types import TracebackType
from typing import (
    TYPE_CHECKING,
    Optional,
    Tuple,
    Type,
    Union,
)

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

from ._parsing import Parsed

if TYPE_CHECKING:
    import os


class FoamFileIO:
    def __init__(self, path: Union["os.PathLike[str]", str]) -> None:
        self.path = Path(path).absolute()

        self.__contents: Optional[bytes] = None
        self.__parsed: Optional[Parsed] = None
        self.__defer_io = 0
        self.__dirty = False

    def __enter__(self) -> Self:
        if self.__defer_io == 0:
            self._read(missing_ok=True)
        self.__defer_io += 1
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        self.__defer_io -= 1
        if self.__defer_io == 0 and self.__dirty:
            assert self.__contents is not None
            self._write(self.__contents)

    def _read(self, *, missing_ok: bool = False) -> Tuple[bytes, Parsed]:
        if not self.__defer_io:
            try:
                contents = self.path.read_bytes()
            except FileNotFoundError:
                contents = None
            else:
                assert isinstance(contents, bytes)
                if self.path.suffix == ".gz":
                    contents = gzip.decompress(contents)

            if contents != self.__contents:
                self.__contents = contents
                self.__parsed = None

        if self.__contents is None:
            if missing_ok:
                return b"", Parsed(b"")
            raise FileNotFoundError(self.path)

        if self.__parsed is None:
            parsed = Parsed(self.__contents)
            self.__parsed = parsed

        return self.__contents, deepcopy(self.__parsed)

    def _write(self, contents: bytes) -> None:
        self.__contents = contents
        self.__parsed = None
        if not self.__defer_io:
            if self.path.suffix == ".gz":
                contents = gzip.compress(contents)

            self.path.write_bytes(contents)
            self.__dirty = False
        else:
            self.__dirty = True

    def __repr__(self) -> str:
        return f"{type(self).__qualname__}('{self.path}')"
