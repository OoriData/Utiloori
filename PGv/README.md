# PostgreSQL/PGVector database using Docker and custom config

## Env variables
1. For security, we will load in secrets using 1password.
2. See the [setup instructions](https://github.com/OoriData/sysops/wiki/Developer-tips-%26-tricks#using-1password-environments) if you do not have 1password CLI. 
3. You can now prefix commands with `op run --env-file=op.env -- <your command>` and have the secrets loaded automatically.
NOTE: you can add the `--no-masking` flag before `--` to avoid 1password masking terminal.

## Locally
1. Clone the repository.
2. Configure needed env variables, `$PG_USER` and `$PG_HOST`, either using your own or `op.env`, detailed below.
3. From the root, run:
```sh
op run --env-file op.env -- docker compose -f PGv/compose.PGvector.yml up -d --build
```
(you can remove `--build` if you don't want to rebuild the image)
5. Now you have PGv database running on `localhost:5432` and an [adminer](https://www.adminer.org/) interface on `localhost:8080`

## On a remote/shared/production host

As above, except for the launch command, for which instead use:

```sh
op run --env-file PGv/op.env -- docker compose -f PGv/compose.PGv_remote.yml up -d --build
```

# Configuration
- All the options in `pg_configs/postgresql.conf`, by default `max_connections` to 200  and `shared_buffers` to 128mb
- Inside of `compose.PGvector.yml` or `compose.PGv_remote.yml`
  - `POSTGRES_USER`: The username used to connect to the database.
  - `POSTGRES_PASSWORD`: The password used to connect to the database.
  - `POSTGRES_DB`: The name of the database created.
  - Ports can be configured inside `compose.PGvector.yml`

# Database upgrades

From time to time [there will be a new tag for the pgvector image](https://hub.docker.com/r/pgvector/pgvector/tags). If this bumps PG by a major version, we might decide to delete or migrate the DB.

**Danger Zone**

To delete & rebuild the DB you can list the volumes

```sh
docker volume ls -q
```

**Make sure you're in the correct docker context**

The PG one will be in the form "[DBNAME]_db_data"

```sh
docker volume rm [VOLUME-ID]
```

You can slso use `docker compose rm -v` to remove any anonymous volumes attached to a container when you remove that container.

If you're trying to delete a volume on your local dev laptop, etc. using the Docker Desktop UI might be a safer bet

![Docker Desktop Volumes screen](<docker-desktop-volumes-screenshot.png>)
