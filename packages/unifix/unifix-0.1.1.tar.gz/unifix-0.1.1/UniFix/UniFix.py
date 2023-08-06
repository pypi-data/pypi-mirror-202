'''
Fix the command using appropriate prompt
'''

import sys
import os
from .Shell.utils import get_alias, get_all_executables
from .Shell import const
from .Shell import shell
from .Fix.chat import FixAgent
from .Uni import matcher
from .System import message
from .errors import EmptyCommand
from .Output import get_output, logs
from .Shell.arg_parse import Parser
from .Shell.alias import print_alias
from .User.ui import select_command



sys.path.append(".")

''' Format:
"Command line to be fixed: 
```bash
sudo echo 'hello' > /etc/a.txt
```
Error message:
bash: /etc/a.txt: Permission denied

Extracted semantics from manpage:
The command is execute a command as another user. The default target user is root. The nested command is display a line of text. with option or argument "hello". The command involves redeirection. The redirected output is: "/etc/a.txt" . 
"
'''


def _get_raw_command(known_args):
    if known_args.command or not os.environ.get('UF_HISTORY'):
        return known_args.command
    else:
        history = os.environ['UF_HISTORY'].split('\n')[::-1]
        # print(history)
        # alias = get_alias()
        # executables = get_all_executables()
        for command in history:
            # diff = SequenceMatcher(a=alias, b=command).ratio()
            # if diff < const.DIFF_WITH_ALIAS or command in executables:
            if command != 'unifix':
                return [command]
    return []


def format_raw_script(raw_script):
    """Creates single script from a list of script parts.

    :type raw_script: [basestring]
    :rtype: basestring

    """
    script = ' '.join(raw_script)

    return script.lstrip()

def from_raw_script(raw_script):
    """Creates instance of `Command` from a list of script parts.

    :type raw_script: [basestring]
    :rtype: Command
    :raises: EmptyCommand

    """
    script = format_raw_script(raw_script)
    if not script:
        raise EmptyCommand

    expanded = shell.from_shell(script)
    output = get_output(script, expanded)
    return expanded, output

def extract_semantic(command):
    '''
    try to extract semantics from the wrong command line
    '''
    try:
        uni = matcher.Uni(command)
        uni.parse_vis()   
        return "".join(uni.description)
    except:
        return None

def fix_command_line(agent, command, error, semantic):
    '''
    try to fix the command
    '''
    # print("fix")
    if not agent:
        print("Do not have GPT Agent")
        return None
    agent.reset()
    question = "Command line to be fixed:\n"+\
                "```bash\n"                  +\
                 command                     +\
                "\n```"
    if error:
        question += "\n\nCommand Output:\n"              +\
                     error                        
    if semantic:
        question += "\n\nExtracted semantics from manpage:\n" +\
                    semantic
    if True or "file" in error or "directory" in error:
        cwd = os.getcwd()
        # print(cwd)
        question += "\n\nAdditional message:" +\
                    message.get_sub_dirs(cwd) +"\n"+\
                    message.get_sub_files(cwd) +"\n"+\
                    message.get_branches()
    agent.think_fix(question)
    return agent.code

NO_CODE_PROMPT = "Notice that you should give me a fixed command line or a command line with the same intent."

MORE_CODE_PROMPT = "Can you give me another fixed command line or a command line with the same intent."

def no_code_fix_again(agent):
    '''
    There's no code in the previous answer, ask again
    '''
    # print("again")
    agent.think_fix(NO_CODE_PROMPT)
    return agent.code

def get_more_fix_command(agent):
    agent.think_fix(MORE_CODE_PROMPT)
    return agent.code



def get_corrected_commands(fix_agent, command, output):
    num = 1
    corrected_commands = []
    code = fix_command_line(fix_agent, command, output, extract_semantic(command))
    while not code:
        code = no_code_fix_again(fix_agent)
    corrected_commands.append(code)
    while num < const.FIX_COMMANDS_NUM:
        code = get_more_fix_command(fix_agent)
        while not code:
            code = no_code_fix_again(fix_agent)
        corrected_commands.append(code)
        num +=1
    return corrected_commands

def run_fix_command(command):
    logs.debug(u'PYTHONIOENCODING: {}'.format(
            os.environ.get('PYTHONIOENCODING', '!!not-set!!')))

    sys.stdout.write(command)

def fix_command_main(fix_agent, known_args):
    """Fixes previous command. Used when `thefuck` called without arguments."""
    with logs.debug_time('Total'):
        raw_command = _get_raw_command(known_args)

        try:
            command, output = from_raw_script(raw_command)
        except EmptyCommand:
            logs.debug('Empty command, nothing to do')
            return

        corrected_commands = get_corrected_commands(fix_agent, command, output)

        if known_args.output: # output the fixed command directly
            for command in corrected_commands:
                print(command)
                
        else:
            selected_command = select_command(corrected_commands)

            if selected_command:
                run_fix_command(selected_command)
            else:
                sys.exit(1)
        
        

global_agent = FixAgent()

def main():
    parser = Parser()
    known_args = parser.parse(sys.argv)

    if known_args.help:
        parser.print_help()
    elif known_args.alias:
        print_alias(known_args)
    # It's important to check if an alias is being requested before checking if
    # `TF_HISTORY` is in `os.environ`, otherwise it might mess with subshells.
    # Check https://github.com/nvbn/thefuck/issues/921 for reference
    elif known_args.command or 'UF_HISTORY' in os.environ:
        fix_command_main(global_agent, known_args)
    else:
        parser.print_usage()

if __name__ == '__main__':
    main()
