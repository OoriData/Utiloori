# SPDX-FileCopyrightText: 2023-present Oori Data <info@oori.dev>
# SPDX-License-Identifier: Apache-2.0
# utiloori.plaintext


def truncate_text_middle(text, max_start=50, max_end=50):
    '''
    Show beginning and end of text with ellipsis in middle if too long

    >>> from utiloori.plaintext import truncate_text_middle
    >>> print(truncate_text_middle('Hello world!', max_start=4, max_end=2))
    ... Hell…d!
    '''
    if len(text) <= max_start + max_end + 3:
        return text
    return f'{text[:max_start]}…{text[-max_end:]}'
