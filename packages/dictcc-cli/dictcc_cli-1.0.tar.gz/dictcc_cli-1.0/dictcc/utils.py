from typing import Callable, Iterator, ParamSpec, TypeVar

T = TypeVar("T")
P = ParamSpec("P")


def listify(size: int | None = None) -> Callable[[Callable[P, Iterator[T]]], Callable[P, list[T]]]:
    def decorator(func: Callable[P, Iterator[T]]) -> Callable[P, list[T]]:
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> list[T]:
            results = list(func(*args, **kwargs))
            if size is not None and len(results) != size:
                raise ValueError(f"Iterator returned {len(results)} instead of {size} elements.")
            return results

        return wrapper

    return decorator
