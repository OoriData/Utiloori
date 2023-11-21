# Utiloori - oori's miscellaneous python toolkit

## terminal ansi colors
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
