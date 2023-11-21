'''
pytest test

or

pytest test/test_ansi_color.py
'''
from utiloori.ansi_color import ansi_color

def test_text_color():
    assert ansi_color('black text', 'black')   == '\033[30mblack text\033[0m'
    assert ansi_color('red text', 'red')       == '\033[31mred text\033[0m'
    assert ansi_color('green text', 'green')   == '\033[32mgreen text\033[0m'
    assert ansi_color('yellow text', 'yellow') == '\033[33myellow text\033[0m'
    assert ansi_color('blue text', 'blue')     == '\033[34mblue text\033[0m'
    assert ansi_color('purple text', 'purple') == '\033[35mpurple text\033[0m'
    assert ansi_color('cyan text', 'cyan')     == '\033[36mcyan text\033[0m'
    assert ansi_color('white text', 'white')   == '\033[37mwhite text\033[0m'


def test_background_color():
    assert ansi_color('black background', 'red', 'black')   == '\033[31m\033[40mblack background\033[0m'
    assert ansi_color('red background', 'red', 'red')       == '\033[31m\033[41mred background\033[0m'
    assert ansi_color('green background', 'red', 'green')   == '\033[31m\033[42mgreen background\033[0m'
    assert ansi_color('yellow background', 'red', 'yellow') == '\033[31m\033[43myellow background\033[0m'
    assert ansi_color('blue background', 'red', 'blue')     == '\033[31m\033[44mblue background\033[0m'
    assert ansi_color('purple background', 'red', 'purple') == '\033[31m\033[45mpurple background\033[0m'
    assert ansi_color('cyan background', 'red', 'cyan')     == '\033[31m\033[46mcyan background\033[0m'
    assert ansi_color('white background', 'red', 'white')   == '\033[31m\033[47mwhite background\033[0m'
