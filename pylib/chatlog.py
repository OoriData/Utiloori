# SPDX-FileCopyrightText: 2023-present Oori Data <info@oori.dev>
# SPDX-License-Identifier: Apache-2.0
# utiloori.pprint_chatlog

from utiloori.ansi_color import ansi_color


def chatmsg_trim(msg):
    '''
    Trim a message from chatlog to only fields defined in HuggingFace Chat Template format
    https://huggingface.co/blog/chat-templates

    Picking HF because they at least seem committed to the idea of a standard format, and (sorta) documenting it
    '''
    # Makes a copy rather than mutilating in place
    new_msg = { k: v for k, v in msg.items() if k in ['content', 'role'] }
    return new_msg


def pformat(chatlog, prefix='💬🟢\n', suffix='💬🔴'):
    ''' Format chatlog for human/LLM readability '''
    chunks = [prefix]
    for message in chatlog:
        content = message['content']
        match message['role'].lower():
            case 'system':
                chunks.append(f'\n{ansi_color("SYSTEM", "black", "white")}: {content}\n')
            case 'user':
                chunks.append(f'\n{ansi_color("USER", "yellow")}: {content}\n')
            case 'assistant':
                chunks.append(f'\n{ansi_color("ASSISTANT", "green")}: {content}\n')
            case _:  # Deal with nonstandard ChatML role
                chunks.append(f'\n{ansi_color(message["role"], "white", "red")}: {content}\n')
    chunks.append(suffix)
    return ''.join(chunks)
