# -*- encoding: utf-8 -*-


class _GenConst(object):
    def __init__(self, name):
        self._name = name

    def __repr__(self):
        return u'<const: {}>'.format(self._name)


KEY_UP = _GenConst('↑')
KEY_DOWN = _GenConst('↓')
KEY_CTRL_C = _GenConst('Ctrl+C')
KEY_CTRL_N = _GenConst('Ctrl+N')
KEY_CTRL_P = _GenConst('Ctrl+P')

KEY_MAPPING = {'\x0e': KEY_CTRL_N,
               '\x03': KEY_CTRL_C,
               '\x10': KEY_CTRL_P}

ACTION_SELECT = _GenConst('select')
ACTION_ABORT = _GenConst('abort')
ACTION_PREVIOUS = _GenConst('previous')
ACTION_NEXT = _GenConst('next')


ARGUMENT_PLACEHOLDER = 'UNIFIX_ARGUMENT_PLACEHOLDER'

SHELL_LOGGER_SOCKET_ENV = 'SHELL_LOGGER_SOCKET'

DIFF_WITH_ALIAS = 0.5

SHELL_LOGGER_LIMIT = 5

LOG_DEBUG = False

no_colors = False

wait_slow_command = 15
slow_commands= ['lein', 'react-native', 'gradle', './gradlew', 'vagrant']
wait_command = 3

env = {'LC_ALL': 'C', 'LANG': 'C', 'GIT_TRACE': '1'}

FIX_COMMANDS_NUM = 3

USER_COMMAND_MARK = u'\u200B' * 10
