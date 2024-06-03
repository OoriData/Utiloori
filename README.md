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
- [Spin up a PostgreSQL vector database using Docker with a custom config](PGv/README.md)

## Print ansi colors in terminal
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

### Usage
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
