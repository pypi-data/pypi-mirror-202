PIPELINES = ""

OPSEMICOLON = ""  # sequentially executed

OPBACKGROUND = "Executes the command in the background."

OPAND = " && " # better with chatgpt

OPOR = " || "

OPERATORS = {';': OPSEMICOLON, '&': OPBACKGROUND, '&&': OPAND, '||': OPOR}

REDIRECTION = "The command involves redeirection. "

REDIRECTING_INPUT = "The redirected input is: "

REDIRECTING_OUTPUT = "The redirected output is: "

APPENDING_REDIRECTED_OUTPUT = "The appending redirected output is: "

REDIRECTING_OUTPUT_ERROR = "Redirect standard output and standard error to: "

APPENDING_OUTPUT_ERROR = "Append standard output and standard error to: "

HERE_DOCUMENTS = "Read input from the current source until a line containing only the delimiter : "

REDIRECTION_KIND = {'<': REDIRECTING_INPUT,
                    '>': REDIRECTING_OUTPUT,
                    '>>': APPENDING_REDIRECTED_OUTPUT,
                    '&>': REDIRECTING_OUTPUT_ERROR,
                    '>&': REDIRECTING_OUTPUT_ERROR,
                    '&>>': APPENDING_OUTPUT_ERROR,
                    '<<': HERE_DOCUMENTS,
                    '<<<': HERE_DOCUMENTS}

ASSIGNMENT = ""

_group_start = "Execute the following commands in a group: "

_group_end = "End the commands group."

_subshell_start = "Execute the command in the subshell: "

_subshell_end = "End the subshell command."

_negate = "the logical negation of: "

'''
_if = ""

_for = ""

_whileuntil = ""

_select = ""
'''

RESERVEDWORDS = {
    '!': _negate,
    '{': _group_start,
    '}': _group_end,
    '(': _subshell_start,
    ')': _subshell_end,
    ';': OPSEMICOLON,
}

'''
def _addwords(key, text, *words):
    for word in words:
        COMPOUNDRESERVEDWORDS.setdefault(key, {})[word] = text
'''

COMPOUNDRESERVEDWORDS = {
    "if": "if the condition is true: ",
    "then": ", then do the command: ",
    "elif": ", else if",
    "else": " else",
    "fi": " ,then endif.",
    "for": "for",
    "in": " in the list: ",
    "do": " do the command: ",
    "done": " then end the loop.",
    "while": "while the condition is true: ",
    "until": "until the condition is false: ",
    "select": "select"
}
'''
_addwords('if', _if, 'if', 'then', 'elif', 'else', 'fi', ';')
_addwords('for', _for, 'for', 'in', 'do', 'done', ';')
_addwords('while', _whileuntil, 'while', 'do', 'done', ';')
_addwords('until', _whileuntil, 'until', 'do', 'done')
_addwords('select', _select, 'select', 'in', 'do', 'done')
'''

_function = "Creat a function named "

_functioncall = 'call shell function %r'
_functionarg = 'argument for shell function %r'

parameters = {
    '*': 'star',
    '@': 'at',
    '#': 'pound',
    '?': 'question',
    '-': 'hyphen',
    '$': 'dollar',
    '!': 'exclamation',
    '0': 'zero',
    '_': 'underscore',
}
