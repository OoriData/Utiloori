import time
import random

def retry_exponential_backoff(
    func,
    initial_delay: float = 1,
    exponential_base: float = 2,
    jitter: bool = True,
    max_retries: int = 10,
    errors: tuple = None,
    retry_if_retval = None,
    log_errors = None
):
    '''
    Retry function call with exponential backoff
    '''

    def wrapper(*args, **kwargs):
        # Initialize variables
        num_retries = 0
        delay = initial_delay

        # Loop until a successful response or max_retries is hit or an exception is raised
        while True:
            try:
                retval = func(*args, **kwargs)
                if retval in retry_if_retval:
                    err = ValueError(f'Unwanted return value {retval}')
                else:
                    return retval

            # Retry on specific errors
            except errors as e:
                err = e

            # Raise exceptions for any errors not specified
            except Exception as e:
                raise e

            if log_errors:
                log_errors(err)

            num_retries += 1

            if num_retries > max_retries:
                # Max retries has been reached
                raise RuntimeError(f'Maximum number of retries ({max_retries}) exceeded.')

            # Backoff: Increment delay
            delay *= exponential_base * (1 + jitter * random.random())

            # Sleep for the delay
            time.sleep(delay)

    return wrapper
