import logging

import argparse
import functools
import os
import re
import subprocess
import sys

from . import option

print_err = functools.partial(print, file=sys.stderr)
logger = logging.getLogger(__name__)

# A backport from subprocess to cover differences between 2/3.4 and 3.5
# This allows the same args to be passed into CPE regardless of version.
# This can be replaced with an import at 2.7 EOL
# See: https://github.com/carlbordum/manly/issues/27


class CalledProcessError(subprocess.CalledProcessError):
    def __init__(self, returncode, cmd, output=None, stderr=None):
        self.returncode = returncode
        self.cmd = cmd
        self.output = output
        self.stderr = stderr


'''
flag_dict = {}


def parse_flags(raw_flags):
    """Return a list of flags.

    Concatenated flags will be split into individual flags
    (eg. '-la' -> '-l', '-a'), but the concatenated flag will also be
    returned, as some command use single dash names (e.g `clang` has
    flags like "-nostdinc") and some even mix both.
    """
    logger.info("Start parse flags")
    flag_dict.clear()
    flags = set()
    preflag = None
    for flag in raw_flags:
        logger.info("Parse %s", flag)
        # Filter out non-flags
        # flags that forget with '-' or '--'? (需要特殊处理，可以直接忽略)
        if not flag.startswith("-"):
            if preflag == None:
                logger.info("Discard flag %s", flag)
                continue  # discard
            else:
                flag_dict[preflag] = flag  # para(目前仅支持一个参数)
                preflag = None
        flags.add(flag)
        preflag = flag
        # Split and sperately add potential single-letter flags
        if not flag.startswith("--"):
            flags.update("-" + char for char in flag[1:])
            preflag = "-"+flag[-1]

    return list(flags)
'''
'''
def parse_manpage(page, flags):
    """Return a list of blocks that match *flags* in *page*."""
    current_section = []
    output = []

    for line in page.splitlines():
        if line:
            current_section.append(line)
            continue

        section = "\n".join(current_section)
        section_top = section.strip().split("\n")[:2]
        section_tail = section.strip().split("\n")[1:]
        # 不换行 第一句
        section_content = " ".join(section_tail).split(".")[0]+"."
        first_line = section_top[0].split(",")

        segments = [seg.strip() for seg in first_line]
        try:
            segments.append(section_top[1].strip())
        except IndexError:
            pass

        for flag in flags:
            for segment in segments:
                if segment.startswith(flag):
                    if "=" in segment and "=" in flag:
                        para_name = segment.split(
                            '=')[1].lstrip('<').rstrip('>')
                        para = flag.split('=')[1]
                        output.append(
                            re.sub(r" [<]%s[>] " % para_name, para,
                                   section_content.rstrip())
                        )
                    elif " " in segment and flag_dict.get("flag", None) is not None:
                        para_name = segment.split(' ')[1]
                        para = flag_dict.get("flag", None)
                        output.append(
                            re.sub(r" [<]%s[>] " % para_name, para,
                                   section_content.rstrip())
                        )
                    else:
                        output.append(
                            section_content.rstrip()
                        )
                    break

        current_section = []
    return output
'''


def _parsetext(page):
    current_section = []
    paragraphs = []
    idx = 0
    program_description = ""
    for line in page.splitlines():
        if line.startswith("OPTION"):#启发式地去掉
            continue
        if line:
            current_section.append(line.strip())
            continue

        section = '\n'.join(current_section).strip()
        #print(section)
        #print("-----------------------")
        if section.startswith('NAME') and program_description == "":
           # print(section)
            program_description = ''.join(current_section[1:])
           # print(program_description)
        if section.startswith("-"):  # 启发式的
            paragraphs.append(option.paragraph(idx, section, section, True))
        else:
            paragraphs.append(option.paragraph(idx, section, section, False))
        idx += 1
        current_section = []
    return paragraphs, program_description


class Manpage:
    def __init__(self, command, nestedcommand=False):
        self.command = command
        self.manpage = None
        self.paragraphs = None
        self.nestedcommand = nestedcommand
        # nested command : sudo, xargs

    @property
    def options(self):
        return [p for p in self.paragraphs if isinstance(p, option.option)]

    def find_option(self, flag):
        for option in self.options:
            for o in option.opts:
                if o == flag:
                    return option
        return None

    def getmanpage(self, nested=False):
        # we set MANWIDTH, so we don't rely on the users terminal width
        # try `export MANWIDTH=80` -- makes manuals more readable imo :)
        man_env = {}
        man_env.update(os.environ)
        man_env["MANWIDTH"] = "80"
        try:
            process = subprocess.Popen(
                ["man", "--"] + ['-'.join(self.command.split(" "))],
                env=man_env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            out, err = (s.decode("utf-8") for s in process.communicate())
            # emulate subprocess.run of py3.5, for easier changing in the future
            if process.returncode:
                raise CalledProcessError(
                    process.returncode, ["man", "--", self.command], out, err
                )
        except OSError as e:
            logger.info("Could not execute 'man'")
            print_err("Could not execute 'man'")
            print_err(e)
            sys.exit(127)
        except CalledProcessError as e:
            logger.info(
                "Could not find the program %s in manpage", self.command)
            return ""

        self.manpage = out
    # flags = parse_flags(flags)
    # output = parse_manpage(manpage, flags)
       # print(out)
        self.paragraphs, title = _parsetext(self.manpage)
        if title == "":
            logger.info("Special format of manpage to describe the program%s, may need specialize."%self.command)
        title_des = " "
        if len(title.split(" — ")) < 2: # sudo 用的是这个
           if len(title.split(" - ")) >=2:
               title_des = ''.join(title.split(" - ")[1:]).strip()
           else:
               logger.info("Fail to extract description of program %s", self.command)
        else:
            title_des = ''.join(title.split(" — ")[1:]).strip() 

        if nested:
            return "The nested command is " + title_des + ". "

        return "The command is " + title_des + ". "

    def process_manpage(self):
        option.extract(self)
