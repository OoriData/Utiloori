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

T = TypeVar('T')

async def batch_fetch_cursor(
    conn,
    query: str,
    batch_size: int = 100
) -> AsyncIterator[list[Any]]:
    """
    Fetch results from PostgreSQL in batches using a named cursor.
    
    Args:
        conn: asyncpg connection
        query: SQL query to execute
        batch_size: Number of records to fetch per batch
        
    Yields:
        Lists of records, with each list containing up to batch_size records

    # Example usage:
    ```
    async def process_results(conn):
        query = "SELECT * FROM your_table"
        
        async for batch in batch_fetch_cursor(conn, query, batch_size=100):
            for record in batch:
                yield record  # Process each individual record
    ```
    """
    # Generate a unique cursor name
    cursor_name = f"batch_cursor_{uuid.uuid4()}"
    
    # Declare the cursor
    declare_query = f"DECLARE {cursor_name} CURSOR FOR {query}"
    
    try:
        async with conn.transaction(readonly=True):
            # Declare the cursor
            await conn.execute(declare_query)
            
            while True:
                # Fetch a batch of results
                fetch_query = f"FETCH FORWARD {batch_size} FROM {cursor_name}"
                batch = await conn.fetch(fetch_query)
                
                if not batch:
                    break
                    
                yield batch
                
    finally:
        # Clean up the cursor
        try:
            await conn.execute(f"CLOSE {cursor_name}")
        except Exception:
            # Handle case where connection is already closed
            pass


# Batched fetch from PG using prepared statement
async def batch_fetch_prepared(
    conn,
    query: str,
    params: tuple = None,
    batch_size: int = 100
) -> AsyncIterator[list[Any]]:
    """
    Fetch results from PostgreSQL in batches using a prepared statement.
    
    Args:
        conn: asyncpg connection
        query: SQL query to execute
        params: Query parameters (optional)
        batch_size: Number of records to fetch per batch
        
    Yields:
        Lists of records, with each list containing up to batch_size records

    # Example usage:
    ```
    async def process_results(conn):
        query = "SELECT * FROM your_table"
        
        async for batch in batch_fetch_prepared(conn, query, batch_size=100):
            for record in batch:
                yield record  # Process each individual record
    ```
    """
    # Workaround for issue encountered with Supabase; needed explicit prepared statements with forced unique names
    stmt_name = f"__asyncpg_{uuid.uuid4()}__"
    
    try:
        async with conn.transaction(readonly=True):
            # Prepare the statement
            stmt = await conn.prepare(query, name=stmt_name)
            
            # Create cursor from prepared statement
            cursor = await stmt.cursor(*params if params else ())
            
            while True:
                # Fetch batch_size records
                batch = await cursor.fetch(batch_size)
                if not batch:
                    break
                    
                yield batch
                
    finally:
        # Cursor is automatically closed when the transaction ends
        pass
