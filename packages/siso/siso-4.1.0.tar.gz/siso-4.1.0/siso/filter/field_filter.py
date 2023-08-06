from typing import Iterator, Set

from .. import api
from ..api import B, F, S, T, Z
from .passthrough import PassthroughAll


class FieldFilter(PassthroughAll[B, F, S, T, Z]):
    """Filter that removes fields that don't match the set of allowed names."""

    allowed_names: Set[str]

    def __init__(self, source: api.Source[B, F, S, T, Z], allowed_names: Set[str]):
        super().__init__(source)
        self.allowed_names = allowed_names

    def fields(self, basis: B) -> Iterator[F]:
        for field in self.source.fields(basis):
            if field.name.casefold() in self.allowed_names:
                yield field
