# SPDX-FileCopyrightText: 2023-present Oori Data <info@oori.dev>
# SPDX-License-Identifier: Apache-2.0
# utiloori.pprint_chatlog

from utiloori.ansi_color import ansi_color

def pprint_chatlog(chatlog):
    ''' Format ChatML style chatlog for human readability '''
    formatted_chatlog = ansi_color('  START OF CHATLOG  '.center(60, '┄'), 'purple')

    for message in chatlog:
        match message['role'].lower():
            case 'system':
                formatted_chatlog += f'\n{ansi_color("SYSTEM", "black", "white")}: {message["content"]}\n'
            case 'user':
                formatted_chatlog += f'\n{ansi_color("USER", "yellow")}: {message["content"]}\n'
            case 'assistant':
                formatted_chatlog += f'\n{ansi_color("ASSISTANT", "green")}: {message["content"]}\n'
            case _:  # Default case when nonstandard ChatML role is used (shouldn't happen)
                formatted_chatlog += f'\n{ansi_color(message["role"], "white", "red")}: {message["content"]}\n'

    formatted_chatlog += ansi_color('  END OF CHATLOG  '.center(60, '┄'), 'purple')
    
    return formatted_chatlog