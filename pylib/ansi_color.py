# SPDX-FileCopyrightText: 2023-present Oori Data <info@oori.dev>
# SPDX-License-Identifier: Apache-2.0
# utiloori.ansi_color

def ansi_color(text: str, font_color: str = 'white', bg_color: str | None = None) -> str:
    '''
    Wraps text in ANSI color codes (and terminators) for printing colored text to console

    ANSI colors: black, red, green, yellow, blue, purple, cyan, white

    usage:
        ansi_color('green text', 'green')
        ansi_color('red text on a blue background', 'red', 'blue')
    '''
    font_color = font_color.lower()
    bg_color = bg_color.lower() if bg_color else None

    font_color_codes = {
        'black': '30',
        'red': '31',
        'green': '32',
        'yellow': '33',
        'blue': '34',
        'purple': '35',
        'cyan': '36',
        'white': '37',
    }
    bg_color_codes = {
        'black': '40',
        'red': '41',
        'green': '42',
        'yellow': '43',
        'blue': '44',
        'purple': '45',
        'cyan': '46',
        'white': '47',
    }

    if bg_color:
        return (
            f'\033[{font_color_codes[font_color]}m'  # Set font color
            f'\033[{bg_color_codes[bg_color]}m'      # Set background color
            f'{text}'                                # insert text
            '\033[0m'                                # Reset font and background colors
        )
    else:
        return (
            f'\033[{font_color_codes[font_color]}m'  # Set font color
            f'{text}'                                # insert text
            '\033[0m'                                # Reset font and background colors
        )
