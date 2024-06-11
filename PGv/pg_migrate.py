import json
import asyncio

import asyncpg

# from ogbujipt.embedding.pgvector_message import CREATE_MESSAGE_TABLE
CREATE_MESSAGE_TABLE = '''
-- Create a table to hold individual messages (e.g. from a chatlog) and their metadata
CREATE TABLE IF NOT EXISTS {table_name} (
    ts TIMESTAMP WITH TIME ZONE,              -- timestamp of the message
    history_key UUID,                         -- uunique identifier for contextual message history
    role TEXT,                                -- role of the message (meta ID such as 'system' or user,
                                              -- or an ID associated with the sender)
    content TEXT NOT NULL,                    -- text content of the message
    embedding VECTOR({embed_dimension}),      -- embedding vectors (array dimension)
    metadata JSON                             -- additional metadata of the message
);
'''
from oorichat.sql_templates import (IF_EXISTS, CREATE_SESSION_TABLE, CREATE_GUILD_TABLE, ESTABLISH_HISTORY_KEY,
                                    QUERY_HISTORY_KEY, LOOKUP_CHANNEL_ID, UPDATE_GUILD_INFO, GET_GUILD_INFO,
                                    INIT_GUILD_INFO, CLEAR_SESSION, CHECK_TABLE_EXISTS)
# from oorichat.persistence_pg import DB_PREFIX, DB_VERSION
DB_PREFIX = 'buddies'
DB_VERSION = '0_8_0'


SOURCE_DB_HOST = 'sofola'
SOURCE_DB_PORT = int('5432')
SOURCE_DB_NAME = 'PGv'
SOURCE_DB_USER = 'oori'
SOURCE_DB_PASSWORD = 'password'

SOURCE_GUILD_TABLE = 'oorichat_v0_7_5_guild'
SOURCE_SESSION_TABLE = 'oorichat_v0_7_5_session'

DEST_DB_HOST = 'localhost'
DEST_DB_PORT = int('5432')
DEST_DB_NAME = 'PGv'
DEST_DB_USER = 'oori'
DEST_DB_PASSWORD = 'passowrd'


async def async_main():
    source_db = await asyncpg.connect(
        host=SOURCE_DB_HOST,
        port=SOURCE_DB_PORT,
        database=SOURCE_DB_NAME,
        user=SOURCE_DB_USER,
        password=SOURCE_DB_PASSWORD
    )

    dest_db = await asyncpg.connect(
        host=DEST_DB_HOST,
        port=DEST_DB_PORT,
        database=DEST_DB_NAME,
        user=DEST_DB_USER,
        password=DEST_DB_PASSWORD
    )

    source_guild_data = await source_db.fetch(f'SELECT * FROM {SOURCE_GUILD_TABLE}')

    await dest_db.execute(CREATE_MESSAGE_TABLE.format(table_name=f'{DB_PREFIX}_{DB_VERSION}_chatlog', embed_dimension=768))
    await dest_db.execute(CREATE_GUILD_TABLE.format(db_prefix=DB_PREFIX, db_version=DB_VERSION))
    await dest_db.execute(CREATE_SESSION_TABLE.format(db_prefix=DB_PREFIX, db_version=DB_VERSION))

    for guild in source_guild_data:
        print(f'inserting guild {guild["guild_id"]} into destination "{DB_PREFIX}_{DB_VERSION}_guild" table')
        await dest_db.execute(
            INIT_GUILD_INFO.format(db_prefix=DB_PREFIX, db_version=DB_VERSION),
            guild['guild_id'],
            guild['bot_id'],
            guild['metadata']
        )

    await source_db.close()
    await dest_db.close()

if __name__ == "__main__":
    asyncio.run(async_main())
