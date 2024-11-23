import pytest
import random
from unittest.mock import Mock  # , patch

from utiloori.func import retry_with_exponential_backoff

# Adding initial_delay=0.01 & exponential_base=1 throughout is to make sire it's fast, as a unit test should be


def test_sync_retry_success():
    mock_counter = Mock(side_effect=[
        ConnectionError("First failure"),
        ConnectionError("Second failure"),
        "Success"
    ])

    # No, don't do this, because we want determinism for unit tests
    # @retry_with_exponential_backoff(exponential_base=1.1)
    # def flaky_sync_func():
    #     if random.random() < 0.7:
    #         raise ConnectionError("Simulated connection error")
    #     return "Success"

    @retry_with_exponential_backoff(initial_delay=0.01, exponential_base=1)
    def flaky_sync_func():
        return mock_counter()
    
    result = flaky_sync_func()
    assert result == "Success"
    assert mock_counter.call_count == 3


@pytest.mark.asyncio
async def test_async_retry_success():
    mock_counter = Mock(side_effect=[
        ConnectionError("First failure"),
        "Success"
    ])
    
    @retry_with_exponential_backoff(initial_delay=0.01, exponential_base=1)
    async def flaky_async_func():
        return mock_counter()
    
    result = await flaky_async_func()
    assert result == "Success"
    assert mock_counter.call_count == 2


def test_max_retries_exceeded():
    mock_counter = Mock(side_effect=ConnectionError("Always failing"))
    
    @retry_with_exponential_backoff(max_retries=2, initial_delay=0.01, exponential_base=1)
    def always_fail():
        return mock_counter()
    
    with pytest.raises(RuntimeError, match="Maximum retries"):
        always_fail()
    assert mock_counter.call_count == 3  # Initial try + 2 retries


def test_retry_on_return_value():
    mock_counter = Mock(side_effect=[None, False, "Success"], errors=(ValueError,))
    
    @retry_with_exponential_backoff(
        retry_if_retval=(None, False),
        errors=(ValueError,),
        initial_delay=0.01,
        exponential_base=1
    )
    def flaky_return_func():
        return mock_counter()
    
    result = flaky_return_func()
    assert result == "Success"
    assert mock_counter.call_count == 3


@pytest.mark.asyncio
async def test_custom_retry_params():
    mock_counter = Mock(side_effect=[
        ValueError("First failure"),
        ValueError("Second failure"),
        "Success"
    ])
    
    @retry_with_exponential_backoff(
        initial_delay=0.01,
        max_retries=5,
        exponential_base=1,
        errors=(ValueError,)
    )
    async def custom_retry_func():
        return mock_counter()
    
    result = await custom_retry_func()
    assert result == "Success"
    assert mock_counter.call_count == 3


def test_different_exceptions():
    mock_counter = Mock(side_effect=[
        ConnectionError("Retry this"),
        ValueError("Don't retry this")
    ])
    
    @retry_with_exponential_backoff(
        initial_delay=0.01,
        errors=(ConnectionError,)
    )
    def specific_error_func():
        return mock_counter()
    
    with pytest.raises(ValueError):
        specific_error_func()
    assert mock_counter.call_count == 2

