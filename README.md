<h1>Utiloori - oori's miscellaneous toolkit</h1>

<table><tr>
  <td><a href="https://oori.dev/"><img src="https://www.oori.dev/assets/branding/oori_Logo_FullColor.png" width="64" /></a></td>
  <td>Utiloori is primarily developed by the crew at <a href="https://oori.dev/">Oori Data</a>. We offer software engineering services around LLM applications.</td>
</tr></table>

[![PyPI - Version](https://img.shields.io/pypi/v/utiloori.svg)](https://pypi.org/project/utiloori)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/utiloori.svg)](https://pypi.org/project/utiloori)

Table of contents:
- [print ansi colors in terminal](#print-ansi-colors-in-terminal)
  - [colors](#colors)
  - [usage](#usage)
- [Spin up a PostgreSQL vector database using Docker with a custom config](#spin-up-a-postgresql-vector-database-using-docker-with-a-custom-config)
  - [Locally](#locally)
  - [On a remote host](#on-a-remote-host)

## print ansi colors in terminal
Wraps text in ANSI color codes (and terminators) for printing colored text to console.

Some terminals, notably VSCode's, try to be clever about not displaying unreadable text; they might override the font color you specify if you specify a background color that is too similar to the font color. For example, if you specify a black font color on a red background, VSCode will override the font color to white.

### colors
the following "standard" ansi colors are supported:
- black
- red
- green
- yellow
- blue
- purple
- cyan
- white

### usage
`from utiloori.ansi_color import ansi_color`

print string with green font:
```python
green_string = ansi_color('lorem', 'green')
print(green_string)
```

print string with purple background (with default, white font):
```python
purple_bg_string = ansi_color('ipsum', bg_color='purple')
print(purple_bg_string)
```

print string with red font on a blue background:
```python
red_on_blue_string = ansi_color('dolor', 'red', 'blue')
print(red_on_blue_string)
```

## Spin up a PostgreSQL vector database using Docker with a custom config
### Locally
1. Clone the repository.
2. From the root, run:
```sh
docker compose -f compose.PGvector.yml up -d --build
```
(you can remove `--build` if you don't want to rebuild the image)
3. Now you have PGv database running on `localhost:5432` and an [adminer](https://www.adminer.org/) interface on `localhost:8080`

### On a remote host
1. Clone the repository on your local machine.
2. Copy `pg_configs/postgresql.conf` to `/etc/postgresql.conf` (or another absolute path) on the remote host.
   - If you choose another absolute path, make sure to modify `compose.PGv_remote.yml` as follows:
  ```yml
    volumes:
      # This is in the remote itself, not in the repo. See pg_configs for references
      - <custom_path_here>:/etc/postgresql.conf
  ```
3. Set up a [remote docker context](https://docs.docker.com/engine/context/working-with-contexts/) and switch to it.
```sh
docker context create <context_name> --docker host=ssh://<user>@<remote_host_ip>

docker context use <context_name>
```
1. Run:
```sh
docker compose up -f compose.PGv_remote.yml
```
1. Now you have PGv database running on `<remote_host_ip>:5432` and an [adminer](https://www.adminer.org/) interface on `<remote_host_ip>:8080`

__Configurable__:
- All the options in `pg_configs/postgresql.conf`, by default `max_connections` to 200  and `shared_buffers` to 128mb
- Inside of `compose.PGvector.yml` or `compose.PGv_remote.yml`
  - `POSTGRES_USER`: The username used to connect to the database.
  - `POSTGRES_PASSWORD`: The password used to connect to the database.
  - `POSTGRES_DB`: The name of the database created.
  - Ports can be configured inside `compose.PGvector.yml`
