# SPDX-FileCopyrightText: 2023-present Oori Data <info@oori.dev>
# SPDX-License-Identifier: Apache-2.0
# utiloori.markdown

# import re2 as re
# from re import MULTILINE, DOTALL  # Why the 🤬 aren't these included in re2?
import re  # Use re until we figure out flags in re2
# mdx_comment_pat = re.compile(r'<!--.*?-->', re.DOTALL)
MDX_COMMENT_PAT = re.compile(r'\{/\*.*\*/\}', re.MULTILINE|re.DOTALL)


def clear_mdx_comments(text: str) -> str:
    '''
    Remove MDX-style Markdown comments from text
    '''
    return MDX_COMMENT_PAT.sub('', text)
