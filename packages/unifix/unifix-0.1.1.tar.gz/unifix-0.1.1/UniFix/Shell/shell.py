import os
from .utils import memoize
from .const import ARGUMENT_PLACEHOLDER
from pathlib import Path
from collections import namedtuple


ShellConfiguration = namedtuple('ShellConfiguration', (
    'content', 'path', 'reload', 'can_configure_automatically'))

class Bash():
        
    def app_alias(self, alias_name):
        # It is VERY important to have the variables declared WITHIN the function
        return '''
            function {name} () {{
                UF_PYTHONIOENCODING=$PYTHONIOENCODING;
                export UF_SHELL=bash;
                export UF_ALIAS={name};
                export UF_SHELL_ALIASES=$(alias);
                export UF_HISTORY=$(fc -ln -10);
                export PYTHONIOENCODING=utf-8;
                UF_CMD=$(
                    unifix {argument_placeholder} "$@"
                ) && eval "$UF_CMD";
                unset UF_HISTORY;
                export PYTHONIOENCODING=$UF_PYTHONIOENCODING;
                {alter_history}
            }}
        '''.format(
            name=alias_name,
            argument_placeholder=ARGUMENT_PLACEHOLDER,
            alter_history=('history -s $UF_CMD;'))
    
    def _parse_alias(self, alias):
        name, value = alias.replace('alias ', '', 1).split('=', 1)
        if value[0] == value[-1] == '"' or value[0] == value[-1] == "'":
            value = value[1:-1]
        return name, value

    @memoize
    def get_aliases(self):
        raw_aliases = os.environ.get('UF_SHELL_ALIASES', '').split('\n')
        return dict(self._parse_alias(alias)
                    for alias in raw_aliases if alias and '=' in alias)
    
    def _expand_aliases(self, command_script):
        aliases = self.get_aliases()
        binary = command_script.split(' ')[0]
        if binary in aliases:
            return command_script.replace(binary, aliases[binary], 1)
        else:
            return command_script
        
    def from_shell(self, command_script):
        """Prepares command before running in app."""
        return self._expand_aliases(command_script)
    
    def _create_shell_configuration(self, content, path, reload):
        return ShellConfiguration(
            content=content,
            path=path,
            reload=reload,
            can_configure_automatically=Path(path).expanduser().exists())
    
    def how_to_configure(self):
        if os.path.join(os.path.expanduser('~'), '.bashrc'):
            config = '~/.bashrc'
        elif os.path.join(os.path.expanduser('~'), '.bash_profile'):
            config = '~/.bash_profile'
        else:
            config = 'bash config'

        return self._create_shell_configuration(
            content=u'eval "$(thefuck --alias)"',
            path=config,
            reload=u'source {}'.format(config))