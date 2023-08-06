'''
 extract code block and maybe polish it
'''
import re



def extract_code_block(text):
    '''
    extract code block
    '''
    code_regex = r"```bash([\s\S]*?)```"
    code_matches = re.findall(code_regex, text)

    if code_matches:
        code = code_matches[0].strip()
        code_line = code.split("\n")
        return " && ".join(code_line)
    return None