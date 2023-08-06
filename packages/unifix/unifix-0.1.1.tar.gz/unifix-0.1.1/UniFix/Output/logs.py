import sys
import colorama
from ..Shell import const
from contextlib import contextmanager
from datetime import datetime

def color(color_):
    """Utility for ability to disabling colored output."""
    if const.no_colors:
        return ''
    else:
        return color_

def debug(msg):
    if const.LOG_DEBUG:
        sys.stderr.write(u'{blue}{bold}DEBUG:{reset} {msg}\n'.format(
            msg=msg,
            reset=color(colorama.Style.RESET_ALL),
            blue=color(colorama.Fore.BLUE),
            bold=color(colorama.Style.BRIGHT)))

def warn(title):
    sys.stderr.write(u'{warn}[WARN] {title}{reset}\n'.format(
        warn=color(colorama.Back.RED + colorama.Fore.WHITE
                   + colorama.Style.BRIGHT),
        reset=color(colorama.Style.RESET_ALL),
        title=title))
    
@contextmanager
def debug_time(msg):
    started = datetime.now()
    try:
        yield
    finally:
        debug(u'{} took: {}'.format(msg, datetime.now() - started))


def failed(msg):
    sys.stderr.write(u'{red}{msg}{reset}\n'.format(
        msg=msg,
        red=color(colorama.Fore.RED),
        reset=color(colorama.Style.RESET_ALL)))


def show_corrected_command(corrected_command):
    sys.stderr.write(u'{prefix}{bold}{script}{reset}\n'.format(
        prefix=const.USER_COMMAND_MARK,
        script=corrected_command,
        bold=color(colorama.Style.BRIGHT),
        reset=color(colorama.Style.RESET_ALL)))


def confirm_text(corrected_command):
    sys.stderr.write(
        (u'{prefix}{clear}{bold}{script}{reset} '
         u'[{green}enter{reset}/{blue}↑{reset}/{blue}↓{reset}'
         u'/{red}ctrl+c{reset}]').format(
            prefix=const.USER_COMMAND_MARK,
            script=corrected_command,
            clear='\033[1K\r',
            bold=color(colorama.Style.BRIGHT),
            green=color(colorama.Fore.GREEN),
            red=color(colorama.Fore.RED),
            reset=color(colorama.Style.RESET_ALL),
            blue=color(colorama.Fore.BLUE)))