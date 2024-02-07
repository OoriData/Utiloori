<h1>Utiloori - oori's miscellaneous toolkit</h1>

<table><tr>
  <td><a href="https://oori.dev/"><img src="https://www.oori.dev/assets/branding/oori_Logo_FullColor.png" width="64" /></a></td>
  <td>Utiloori is primarily developed by the crew at <a href="https://oori.dev/">Oori Data</a>. We offer software engineering services around LLM applications.</td>
</tr></table>

[![PyPI - Version](https://img.shields.io/pypi/v/utiloori.svg)](https://pypi.org/project/utiloori)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/utiloori.svg)](https://pypi.org/project/utiloori)

__Table of contents:__
- [print ansi colors in terminal](#print-ansi-colors-in-terminal)
  - [colors](#colors)
  - [usage](#usage)
- [Spin up a PostgreSQL vector database using Docker with a custom config](#spin-up-a-postgresql-vector-database-using-docker-with-a-custom-config)
  - [Env variables](#env-variables)
  - [Locally](#locally)
  - [On a remote host](#on-a-remote-host)
- [Spin up a Dozzle docker log viewer on sofola with remote\_hosts](#spin-up-a-dozzle-docker-log-viewer-on-sofola-with-remote_hosts)

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
### Env variables
1. For security, we will load in secrets using 1password.
2. See the [setup instructions](https://github.com/OoriData/sysops/wiki/Developer-tips-%26-tricks#using-1password-environments) if you do not have 1password CLI. 
3. You can now prefix commands with `op run --env-file=op.env -- <your command>` and have the secrets loaded automatically.
NOTE: you can add the `--no-masking` flag before `--` to avoid 1password masking terminal.

### Locally
1. Clone the repository.
2. Configure needed env variables, `$PG_USER` and `$PG_HOST`, either using your own or `op.env`, detailed below.
3. From the root, run:
```sh
op run --env-file op.env -- docker compose -f PGv/compose.PGvector.yml up -d --build
```
(you can remove `--build` if you don't want to rebuild the image)
5. Now you have PGv database running on `localhost:5432` and an [adminer](https://www.adminer.org/) interface on `localhost:8080`

__Configurable__:
- All the options in `pg_configs/postgresql.conf`, by default `max_connections` to 200  and `shared_buffers` to 128mb
- Inside of `compose.PGvector.yml` or `compose.PGv_remote.yml`
  - `POSTGRES_USER`: The username used to connect to the database.
  - `POSTGRES_PASSWORD`: The password used to connect to the database.
  - `POSTGRES_DB`: The name of the database created.
  - Ports can be configured inside `compose.PGvector.yml`
