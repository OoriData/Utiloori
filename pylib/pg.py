# SPDX-FileCopyrightText: 2023-present Oori Data <info@oori.dev>
# SPDX-License-Identifier: Apache-2.0
# utiloori.pg
'''
Tools for PostgreSQL
'''
from typing import AsyncIterator, TypeVar, Any
# from itertools import islice
import uuid
# import asyncio


from typing import AsyncIterator, TypeVar, Any, Optional
import uuid
import asyncio
from asyncpg.exceptions import ConnectionDoesNotExistError, InterfaceError

T = TypeVar('T')

class ConnectionLostError(Exception):
    """Raised when the connection is lost and we need to retry from last known position"""
    pass

async def resilient_prepared_fetch(
    pool,
    query: str,
    params: tuple = None,
    batch_size: int = 100,
    max_retries: int = 3,
    retry_delay: float = 1.0,
    position: int = 0
) -> AsyncIterator[tuple[list[Any], int]]:
    """
    Fetch results from PostgreSQL in batches using prepared statements with retry logic.
    
    Args:
        pool: asyncpg connection pool
        query: SQL query to execute
        params: Query parameters (optional)
        batch_size: Number of records to fetch per batch
        max_retries: Maximum number of retry attempts per batch
        retry_delay: Delay between retries in seconds
        position: Starting position for OFFSET
    """
    current_position = position
    retries = 0
    
    # Add OFFSET/LIMIT to the original query
    paginated_query = f"""
        {query}
        OFFSET $1 LIMIT $2
    """
    
    while True:
        try:
            async with pool.acquire() as conn:
                # Create a unique statement name for this batch
                stmt_name = f"__asyncpg_{uuid.uuid4()}__"
                
                async with conn.transaction(readonly=True):
                    # Prepare the statement
                    prepared_stmt = await conn.prepare(
                        paginated_query,
                        name=stmt_name
                    )
                    
                    # Execute with current position and batch size
                    query_params = (params or ()) + (current_position, batch_size)
                    batch = await prepared_stmt.fetch(*query_params)
                    
                    if not batch:
                        break
                    
                    current_position += len(batch)
                    yield batch, current_position
                    retries = 0  # Reset retry counter on successful fetch
                    
        except (ConnectionDoesNotExistError, InterfaceError) as e:
            retries += 1
            if retries > max_retries:
                raise ConnectionLostError(
                    f"Failed to maintain connection after {max_retries} retries. "
                    f"Last successful position: {current_position}"
                ) from e
                
            await asyncio.sleep(retry_delay)
            continue

async def process_results_prepared(
    pool,
    query: str,
    params: tuple = None,
    batch_size: int = 100,
    checkpoint_callback = None
):
    """
    Process results using prepared statements with checkpointing support.
    
    Args:
        pool: asyncpg connection pool
        query: SQL query to execute
        params: Query parameters (optional)
        batch_size: Number of records to fetch per batch
        checkpoint_callback: Optional async callback function(position) to save progress
    """
    try:
        async for batch, position in resilient_prepared_fetch(
            pool,
            query,
            params,
            batch_size
        ):
            for record in batch:
                yield record
                
            if checkpoint_callback:
                await checkpoint_callback(position)
                
    except ConnectionLostError as e:
        # Here you could log the error and/or save the position for later resumption
        raise


# T = TypeVar('T')

# async def batch_fetch_cursor(
#     conn,
#     query: str,
#     batch_size: int = 100
# ) -> AsyncIterator[list[Any]]:
#     """
#     Fetch results from PostgreSQL in batches using a named cursor.
    
#     Args:
#         conn: asyncpg connection
#         query: SQL query to execute
#         batch_size: Number of records to fetch per batch
        
#     Yields:
#         Lists of records, with each list containing up to batch_size records

#     # Example usage:
#     ```
#     async def process_results(conn):
#         query = "SELECT * FROM your_table"
        
#         async for batch in batch_fetch_cursor(conn, query, batch_size=100):
#             for record in batch:
#                 yield record  # Process each individual record
#     ```
#     """
#     # Generate a unique cursor name
#     cursor_name = f"batch_cursor_{uuid.uuid4()}"
    
#     # Declare the cursor
#     declare_query = f"DECLARE {cursor_name} CURSOR FOR {query}"
    
#     try:
#         async with conn.transaction(readonly=True):
#             # Declare the cursor
#             await conn.execute(declare_query)
            
#             while True:
#                 # Fetch a batch of results
#                 fetch_query = f"FETCH FORWARD {batch_size} FROM {cursor_name}"
#                 batch = await conn.fetch(fetch_query)
                
#                 if not batch:
#                     break
                    
#                 yield batch
                
#     finally:
#         # Clean up the cursor
#         try:
#             await conn.execute(f"CLOSE {cursor_name}")
#         except Exception:
#             # Handle case where connection is already closed
#             pass


# # Batched fetch from PG using prepared statement
# async def batch_fetch_prepared(
#     conn,
#     query: str,
#     params: tuple = None,
#     batch_size: int = 100
# ) -> AsyncIterator[list[Any]]:
#     """
#     Fetch results from PostgreSQL in batches using a prepared statement.
    
#     Args:
#         conn: asyncpg connection
#         query: SQL query to execute
#         params: Query parameters (optional)
#         batch_size: Number of records to fetch per batch
        
#     Yields:
#         Lists of records, with each list containing up to batch_size records

#     # Example usage:
#     ```
#     async def process_results(conn):
#         query = "SELECT * FROM your_table"
        
#         async for batch in batch_fetch_prepared(conn, query, batch_size=100):
#             for record in batch:
#                 yield record  # Process each individual record
#     ```
#     """
#     # Workaround for issue encountered with Supabase; needed explicit prepared statements with forced unique names
#     stmt_name = f"__asyncpg_{uuid.uuid4()}__"
    
#     try:
#         async with conn.transaction(readonly=True):
#             # Prepare the statement
#             stmt = await conn.prepare(query, name=stmt_name)
            
#             # Create cursor from prepared statement
#             cursor = await stmt.cursor(*params if params else ())
            
#             while True:
#                 # Fetch batch_size records
#                 batch = await cursor.fetch(batch_size)
#                 if not batch:
#                     break
                    
#                 yield batch
                
#     finally:
#         # Cursor is automatically closed when the transaction ends
#         pass
