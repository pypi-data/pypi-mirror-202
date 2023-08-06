'''
 chat with GPT
'''
import os
import sys
import openai
import json
import re
from subprocess_tee import run
from glom import glom
from . import system
from . import extract_code



if "OPENAI_API_KEY" not in os.environ:
    print("ERROR: OPENAI_API_KEY environment variable not found.")
    sys.exit(1)

openai.api_key = os.environ["OPENAI_API_KEY"]

FIX_COMMAND_PROMPT = """
Now your job is to fix bash command lines. You are going to be given a command line and some possible error messages. 
Some system and semantic messages may also be given.
The command line may be wrong in that it causes error or it did not run expectedly.
Your job is to come up with correct bash command lines.
You may need to correct some typos if the command is not found. For example, 'cs' may be a typo of 'cd', 'mdir' may be a typo of 'mkdir'.
You may need to add something to let the command line run successfully, e.g. fix 'cd nonexist' by 'mkdir nonexist && cd nonexist'.
You may need to take into consideration some additional message such as files or directories in the system. 
For example, 'cd Hit' may be a typo of 'cd  hit' if 'hit' is a directory in the system.
So you should consider whether to correct the typo of a file/directory or create a new one.
Do not use anything but bash command. The format of your answer should be a line of command, so you can combine multiple commands by '&&' to give a command line.
Pay attention that you must provide one suggested substitute command line with the same intent no matter whether the error message is given.
Use the following format.
Give the command line directly without explaination and answer as fast as possible please.


<Example>
Q: 
"Command line to be fixed: 
```bash
sudo echo 'hello' > /etc/a.txt
```

Command Output:
bash: /etc/a.txt: Permission denied

Extracted semantics from manpage:
The command is execute a command as another user. The default target user is root. The nested command is display a line of text. with option or argument "hello". The command involves redeirection. The redirected output is: "/etc/a.txt" . 
"

The error happens because that you don't have the access permission to the file '/etc/a.txt', the fixed command is:
```bash
sudo sh -c 'echo "hello" > /etc/a.txt'
```

"""

def extract_head_tail(text):
    '''
    extract head and tail of text (200 words)
    '''
    if len(text) <= 200:
        return text
    else:
        head = text[:100]
        tail = text[-100:]
        return head + "..." + tail


class FixAgent():
    '''
    agent to fix the command line
    '''
    PRESET_MESSAGES = [
        {"role": "system", "content": FIX_COMMAND_PROMPT},
        {"role": "system", "content": "The operating environment for bash is as follows:"+system.info()},
    ]

    def __init__(self, temperature=0.1):
        self.temperature = temperature
        self.messages = self.PRESET_MESSAGES
        self.display_comment = ""
        self.question = []
        self.names = []
        self.code = ""

    def add_user_message(self, message):
        '''
        add user message
        '''
        self.messages.append({"role": "user", "content": message})

    def add_system_message(self, message):
        '''
        message about system
        '''
        self.messages.append({"role": "system", "content": message})

    def add_assistant_message(self, message):
        '''
        assistant message - the chat happened so far
        '''
        self.messages.append({"role": "assistant", "content": message})

    def report_result(self, result):
        '''
        add result of the fixed command line (add latter) (TODO)
        '''
        self.add_system_message(f"""
        returncode : {result.returncode}
        stdout :
        {extract_head_tail(result.stdout)}
        stderr : 
        {extract_head_tail(result.stderr)}
        """)

    def chat(self):
        '''
        chat with gpt
        '''
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages,
            temperature=self.temperature,
        )
        message = glom(response, "choices.0.message.content", default=None)
        self.add_assistant_message(message)
        return message

    def think_fix(self, question):
        '''
        fix the command
        '''
        self.question.append(question)
        self.add_user_message(question)
        message = self.chat()
        self.code = extract_code.extract_code_block(message)
        return message

    def reset(self):
        '''
        reset for a new fix
        '''
        self.messages = self.PRESET_MESSAGES
