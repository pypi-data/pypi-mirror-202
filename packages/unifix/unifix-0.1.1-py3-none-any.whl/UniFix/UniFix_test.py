'''
Fix the command using appropriate prompt
This is a test program for experiment
The input is a file of Command/Error
The test inputs is in the test_file
Use make tests to see the tests
'''
import sys
import re
import argparse
from .Fix.chat import FixAgent
from .Uni import matcher


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
    print("fix")
    if not agent:
        print("Do not have GPT Agent")
        return None
    agent.reset()
    question = "Command line to be fixed:\n"+\
                "```bash\n"                  +\
                 command                     +\
                "\n```"
    if error:
        question += "\n\nError message:\n"              +\
                     error                        
    if semantic:
        question += "\n\nExtracted semantics from manpage:\n" +\
                    semantic
    agent.think_fix(question)
    return agent.code

NO_CODE_PROMPT = "Notice that you should give me a fixed command or a command line with the same intent."

def no_code_fix_again(agent):
    '''
    There's no code in the previous answer, ask again
    '''
    print("again")
    agent.think_fix(NO_CODE_PROMPT)
    return agent.code

Long_error_demo = \
    """On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   Makefile
        modified:   UniFix.py

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        test

no changes added to commit (use "git add" and/or "git commit -a")"""

def parse_from_test(text):
    '''
    parse code and error from test text
    format: (one line)
    Command: ...
    Error: ...
    '''
    command = re.search(r"(?<=^Command:\s).+", text, re.MULTILINE)
    if command:
        command = command.group(0).strip()
    error = re.search(r"(?<=^Error:\s).+", text, re.MULTILINE)
    if error:
        error = error.group(0).strip()
    return command, error


def main():
    '''
    main function
    '''
    parser = argparse.ArgumentParser(
        prog="unifix",
        description="Fix bash command line",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("testfile", nargs=argparse.REMAINDER, help="")
    args = parser.parse_args()
    if not args.testfile:
        print(
            "Missing test file name",
        )
        sys.exit(1)
    
    fix_agent = FixAgent()
    for file in args.testfile:
        test_file = open(file, encoding = "utf-8")
        command, error = parse_from_test(test_file.read())
        test_file.close()
        code = fix_command_line(fix_agent, command, error, extract_semantic(command))
        while not code:
            code = no_code_fix_again(fix_agent)
        print("-----------------------------------------------------------------------")
        print("original: "+ command)
        print("fixed   : " + code.strip())
        print("-----------------------------------------------------------------------")


if __name__ == "__main__":
    main()
    


