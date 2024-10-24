"""
This type stub file was generated by pyright.
"""

import uuid
from typing import Any, Iterable, Optional, ParamSpec, TypeVar

P = ParamSpec('P')
T = TypeVar('T')
def consume(iterator: Iterable[Any], n: Optional[int] = ...) -> None:
    "Advance the iterator n-steps ahead. If n is none, consume entirely."
    ...

def pass_generator_as_copy(*xs: Iterable[str]): # -> Callable[..., Callable[P, T]]:
    ...

class UuidGenerator:
    def __init__(self, seed: Optional[int] = ...) -> None:
        ...
    
    def reset(self): # -> Self:
        ...
    
    def next(self, n: Optional[int] = ...): # -> UUID | Generator[UUID, None, None]:
        ...
    
    def __iter__(self): # -> Generator[UUID | Generator[UUID, None, None], Any, NoReturn]:
        ...
    
    @pass_generator_as_copy('xs')
    def map(self, xs: Iterable[T], offset: Optional[int] = ...) -> Iterable[uuid.UUID]:
        ...
    
    @pass_generator_as_copy('xs')
    def zipWith(self, xs: Iterable[T], offset: Optional[int] = ...) -> Iterable[tuple[uuid.UUID, T]]:
        ...
    


