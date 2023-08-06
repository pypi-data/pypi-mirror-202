from . import shell

def _get_alias(known_args):

    alias = shell.app_alias(known_args.alias)
    return alias


def print_alias(known_args):
    print(_get_alias(known_args))