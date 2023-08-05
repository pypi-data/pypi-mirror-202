import concurrent.futures
import warnings
from functools import reduce
from typing import Any, Callable, List


def pmap(funcs: List[Callable], max_workers: int = 2) -> List[Any]:
    """Simple parallel map construction, using a thread pool executor.

    Feed it an array of functions, and it will execute them in parallel, returning
    the results in the same order as the input functions"""
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(func): i for i, func in enumerate(funcs)}
        results = []
        for future, i in futures.items():
            try:
                result = future.result()
            except Exception as e:
                warnings.warn(f"Function {i} raised an exception: {e}")
                result = None
            results.append((i, result))
        results.sort()
        return [result for i, result in results]


def pipe(inp: Any, *fns: Callable[..., Any]) -> Any:
    """
    Applies a series of functions to an input value, with the output of each function
    being passed as the input to the next function in the series. Returns the final
    output value after all functions have been applied.

    :param inp: The initial input value
    :param fns: A variable-length list of functions to apply to the input value

    :return: The final output value after all functions have been applied
    """
    return reduce(lambda cum, fn: fn(cum), fns, inp)
