# Utiloori - oori's miscellaneous python toolkit

<table><tr>
  <td><a href="https://oori.dev/"><img src="https://www.oori.dev/assets/branding/oori_Logo_FullColor.png" width="64" /></a></td>
  <td>Utiloori is primarily developed by the crew at <a href="https://oori.dev/">Oori Data</a>. We offer software engineering services around LLM applications.</td>
</tr></table>

[![PyPI - Version](https://img.shields.io/pypi/v/utiloori.svg)](https://pypi.org/project/utiloori)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/utiloori.svg)](https://pypi.org/project/utiloori)

## print ansi colors in terminal
`from utiloori.ansi_color import ansi_color` 
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
print string with green text:
```python
green_string = ansi_color('foo', 'green')
print(green_string)
```

print string with red text on a blue background:
```python
red_on_blue_string = ansi_color('bar', 'red', 'blue')
print(red_on_blue_string)
```
