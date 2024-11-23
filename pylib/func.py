# SPDX-FileCopyrightText: 2023-present Oori Data <info@oori.dev>
# SPDX-License-Identifier: Apache-2.0
# utiloori.func

import asyncio
import random
from functools import wraps
from typing import Callable, Any, Optional, Tuple, Union, Type


def retry_with_exponential_backoff(
    *decorator_args,
    initial_delay: float = 1,
    exponential_base: float = 2,
    jitter: bool = True,
    max_retries: int = 10,
    max_delay: Optional[float] = None,
    errors: Tuple[Type[Exception], ...] = (ConnectionError, TimeoutError),
    retry_if_retval: Optional[Union[Callable[[Any], bool], Tuple[Any, ...]]] = None,
    logger: Optional[Callable[[Exception], None]] = None
):
    '''
    Decorates a function with exponential backoff retry mechanism.

    Supports both synchronous and asynchronous functions. Retries the function 
    call with increasing delays between attempts, with optional jitter to prevent 
    [thundering herd problem](https://en.wikipedia.org/wiki/Thundering_herd_problem).

    Args:
        func (Callable): The function to be retried.
        initial_delay (float, optional): Initial delay between retries. Defaults to 1 second.
        exponential_base (float, optional): Base for exponential backoff. Defaults to 2.
        jitter (bool, optional): Add randomness to delay to prevent synchronization. Defaults to True.
        max_retries (int, optional): Maximum number of retry attempts. Defaults to 10.
        max_delay (float, optional): Maximum delay between retries. Defaults to None.
        errors (Tuple[Type[Exception], ...], optional): Exceptions that trigger a retry. 
            Defaults to (ConnectionError, TimeoutError).
        retry_if_retval (Union[Callable[[Any], bool], Tuple[Any, ...]], optional): 
            Condition to retry based on return value. Can be a predicate function 
            or a tuple of values to retry.
        logger (Callable[[Exception], None], optional): Optional logging function 
            for retry-related errors.

    Returns:
        The result of the function call after successful execution or raising 
        a RuntimeError if max retries are exceeded.

    Raises:
        RuntimeError: If maximum number of retries is exceeded.

# Sync function example
@retry_with_exponential_backoff
def sync_fetch():
    # sync code here

# Async function example
@retry_with_exponential_backoff
async def async_fetch():
    # async code here

# Passing custom parameters
result = sync_fetch(initial_delay=2, max_retries=5)

# Or with async function
result = await async_fetch(initial_delay=2, max_retries=5)
    '''
    # Allow decorator to be used with or without arguments
    if len(decorator_args) == 1 and callable(decorator_args[0]):
        func = decorator_args[0]
        return _retry_wrapper(
            func, 
            initial_delay, 
            exponential_base, 
            jitter, 
            max_retries, 
            max_delay, 
            errors, 
            retry_if_retval, 
            logger
        )
    
    def decorator(func):
        return _retry_wrapper(
            func, 
            initial_delay, 
            exponential_base, 
            jitter, 
            max_retries, 
            max_delay, 
            errors, 
            retry_if_retval, 
            logger
        )
    
    return decorator

def _retry_wrapper(
    func: Callable,
    initial_delay: float,
    exponential_base: float,
    jitter: bool,
    max_retries: int,
    max_delay: Optional[float],
    errors: Tuple[Type[Exception], ...],
    retry_if_retval: Optional[Union[Callable[[Any], bool], Tuple[Any, ...]]],
    logger: Optional[Callable[[Exception], None]]
):
    @wraps(func)
    def wrapper(*args, **kwargs):
        async def async_wrapper():
            num_retries = 0
            delay = initial_delay

            while True:
                try:
                    # Check if the function is async
                    if asyncio.iscoroutinefunction(func):
                        retval = await func(*args, **kwargs)
                    else:
                        retval = func(*args, **kwargs)
                    
                    # More flexible return value checking
                    if retry_if_retval:
                        should_retry = (
                            (callable(retry_if_retval) and retry_if_retval(retval)) or
                            (isinstance(retry_if_retval, tuple) and retval in retry_if_retval)
                        )
                        if should_retry:
                            raise ValueError(f'Unwanted return value {retval}')
                    
                    return retval

                except errors as e:
                    if logger:
                        logger(e)

                    num_retries += 1
                    if num_retries > max_retries:
                        raise RuntimeError(f'Maximum retries ({max_retries}) exceeded.')

                    # Add max_delay constraint
                    delay *= exponential_base * (1 + jitter * random.random())
                    if max_delay:
                        delay = min(delay, max_delay)

                    await asyncio.sleep(delay)

        # Return a coroutine if the function is async, otherwise run the sync version
        if asyncio.iscoroutinefunction(func):
            return async_wrapper()
        else:
            return asyncio.run(async_wrapper())

    return wrapper
