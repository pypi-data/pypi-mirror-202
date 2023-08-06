import sys
from argparse import ArgumentParser
from .utils import get_alias
from .const import ARGUMENT_PLACEHOLDER


class Parser(object):
    """Argument parser that can handle arguments with our special
    placeholder.

    """

    def __init__(self):
        self._parser = ArgumentParser(prog='unifix', add_help=False, description="Understand and Fix bash command line")
        self._add_arguments()

    def _add_arguments(self):
        """Adds arguments to parser."""
        self._parser.add_argument(
            '-h', '--help',
            action='store_true',
            help='show this help message and exit')

        self._parser.add_argument(
            '-a', '--alias',
            nargs='?',
            const=get_alias(),
            help='[custom-alias-name] prints alias for current shell')
        
        self._parser.add_argument(
            'command',
            nargs='*',
            help='command that should be fixed')
        
        self._parser.add_argument(
            '-o', '--output',
            action='store_true',
            help= 'show the fixed commands directly without the process of select and run'
        )

    
    def _prepare_arguments(self, argv):
        """Prepares arguments by:

        - removing placeholder and moving arguments after it to beginning,
          we need this to distinguish arguments from `command` with ours;

        - adding `--` before `command`, so our parse would ignore arguments
          of `command`.

        """
        if ARGUMENT_PLACEHOLDER in argv:
            index = argv.index(ARGUMENT_PLACEHOLDER)
            return argv[index + 1:] + ['--'] + argv[:index]
        elif argv and not argv[0].startswith('-') and argv[0] != '--':
            return ['--'] + argv
        else:
            return argv

    def parse(self, argv):
        arguments = self._prepare_arguments(argv[1:])
        return self._parser.parse_args(arguments)
    
    def print_usage(self):
        self._parser.print_usage(sys.stderr)

    def print_help(self):
        self._parser.print_help(sys.stderr)
