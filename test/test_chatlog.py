'''
pytest test

or

pytest test/test_pprint_chatlog.py
'''

from utiloori.chatlog import pformat
from utiloori.ansi_color import ansi_color

CONSOLE_WIDTH = 60


def test_pformat():
    chatlog = [
        {'role': 'system', 'content': 'System message 1'},
        {'role': 'user', 'content': 'User message 1'},
        {'role': 'assistant', 'content': 'Assistant message 1'},
        {'role': 'system', 'content': 'System message 2'},
        {'role': 'user', 'content': 'User message 2'},
        {'role': 'assistant', 'content': 'Assistant message 2'},
        {'role': 'nonstandard', 'content': 'Nonstandard message'}
    ]
    expected_output = (
        '\033[35m' + '  START OF CHATLOG  '.center(CONSOLE_WIDTH, '┄') + '\033[0m' +
        '\n\033[30m\033[47mSYSTEM\033[0m: System message 1\n' +
        '\n\033[33mUSER\033[0m: User message 1\n' +
        '\n\033[32mASSISTANT\033[0m: Assistant message 1\n' +
        '\n\033[30m\033[47mSYSTEM\033[0m: System message 2\n' +
        '\n\033[33mUSER\033[0m: User message 2\n' +
        '\n\033[32mASSISTANT\033[0m: Assistant message 2\n' +
        '\n\033[37m\033[41mnonstandard\033[0m: Nonstandard message\n' +
        '\033[35m' + '  END OF CHATLOG  '.center(60, '┄') + '\033[0m'
    )
    result = pformat(
        chatlog,
        prefix=ansi_color('  START OF CHATLOG  '.center(CONSOLE_WIDTH, '┄'), 'purple'),
        suffix=ansi_color('  END OF CHATLOG  '.center(CONSOLE_WIDTH, '┄'), 'purple')
        )
    assert result == expected_output
