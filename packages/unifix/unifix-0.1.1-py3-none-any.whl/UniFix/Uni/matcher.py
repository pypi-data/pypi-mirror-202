import logging
import functools
import sys

from . import maninfo, helpconstants, errors
import bashlex.ast
import bashlex.parser


print_err = functools.partial(print, file=sys.stderr)
logger = logging.getLogger(__name__)


class Uni(bashlex.ast.nodevisitor):
    '''
    parse a command line and return sentences to describe it.
    '''

    def __init__(self, command: str):
        self.command = command
        self.description = []
        self._prevoption = self._currentoption = None
        # keep a stack of the currently visited compound command (if/for..)
        # to provide context when matching reserved words, since for example
        # the keyword 'done' can appear in a for, while..
        self.compoundstack = []

        # a set of functions defined in the current input, we will try to match
        # commands against them so if one refers to defined function, it won't
        # show up as unknown or be taken from the db
        self.functions = set()
        self.listnum = 1 # pip的指令计数
        self.manpagestack = [] # manpage的stack
        self.opt_des = False # 是否前面无法解析的参数已经描述了"with option or argument"
        self.seqnumstack = [] # list的指令计数
        self.groups = 0 # 目前所在的嵌套group层
       # self._currentoption = None

       #-----------关于sudo,xargs-------用于处理nested command中的Multicommand---------------------
        self.nested = False
        self.prenode = None
       #------------------------------------------------------------------------------------------
    '''
    def visitnode(self, n):
        pass
    '''

    def findmanpage(self, prog):
       # prog = prog.decode('latin1')
        logger.info('looking up %r', prog)
        manpage = maninfo.Manpage(prog)
        s = manpage.getmanpage(self.nested)
        if s != "":
            # self.description += s
            manpage.process_manpage()
        else:
            raise errors.ProgramDoesNotExist
        return manpage, s

    def find_option(self, opt):
        # print("find ",opt)
        manpage = self.manpagestack.pop()
        currentoption = manpage.find_option(opt)
        if currentoption == None:
            currentoption = manpage.find_option("-"+opt)
        self._currentoption = currentoption
        self.manpagestack.append(manpage)
        # print(opt_para)
        return self._currentoption

    def visitnodeend(self, n):

        if n.kind == 'command':
            if self.description[-1][-2:] != ". " and self.description[-1][-1] != '.':
                self.description[-1]+= ". "
            #print(self.description)
            self.endcommand()
        elif n.kind in ('if', 'for', 'while', 'until'):
            kind = self.compoundstack.pop()
            assert kind == n.kind
        elif n.kind == 'list' and not self.groups:
            self.seqnumstack.pop()

    def visitoperator(self, n, op):
        helptext = helpconstants.OPERATORS[op]
        if op == ';' and not self.groups:
            self.seqnumstack[-1] += 1
            helptext = str(self.seqnumstack[-1]) + ". "
        self.description.append(helptext)

    def visitlist(self, n, parts):  # 按顺序执行（无需处理？）--方便gpt可给信息
        if not self.groups:
            self.description.append("The following commands are executed sequencially: 1. ")
            self.seqnumstack.append(1)

    def visitpipe(self, n, pipe):
        self.listnum += 1
        self.description.append(str(self.listnum)+". ")

    def visitpipeline(self, n, parts):
        idxpipenode = bashlex.ast.findfirstkind(parts, 'pipe')
        if idxpipenode != -1: # 因为negation也被当作pipeline了
            self.description.append("The following commands are piped together: 1. ")
        # for part in parts:
          #  self.visit(part)

    def visitcompound(self, n, list, redirects):
        pass

    def visitif(self, node, parts):
        self.compoundstack.append('if')

    def visitfor(self, node, parts):
        self.compoundstack.append('for')

    def visitwhile(self, node, parts):
        self.compoundstack.append('while')

    def visituntil(self, node, parts):
        self.compoundstack.append('until')

    def startcommand(self, n, parts):
        idxwordnode = bashlex.ast.findfirstkind(parts, 'word')
        assert idxwordnode != -1
        wordnode = parts[idxwordnode]
        if wordnode.parts:
            self.manpagestack.append(None)
            logger.info('node %r has parts (it was expanded), no point in looking'
                        ' up a manpage for it', wordnode)
            return False
        try:
            mp, sp = self.findmanpage(wordnode.word)
            # print(wordnode.word, sp)
            # we consume this node here, pop it from parts so we
            # don't visit it again as an argument
            parts.pop(idxwordnode)
        except errors.ProgramDoesNotExist:

            # add a group for this command, we'll mark it as unknown
            # when visitword is called
            self.description.append(wordnode.word + "(a possible command, but cannot find explaination, may be mistyped or needs installing) ")
            parts.pop(idxwordnode) # 在visitword时不重复访问
            self.manpagestack.append(None)
            return False

        manpage = mp
        str_mp = sp
        idxnextwordnode = bashlex.ast.findfirstkind(parts, 'word')

        # check the next word for a possible multicommand if:
        # - the matched manpage says so
        # - we have another word node
        # - the word node has no expansions in it
        if idxnextwordnode != -1 and not parts[idxnextwordnode].parts:
            nextwordnode = parts[idxnextwordnode]
            try:
                multi = '%s %s' % (wordnode.word, nextwordnode.word)
                # print(multi)
                logger.info(
                    '%r is a multicommand, trying to get another token and look up %r', manpage, multi)
                manpage, str_mp = self.findmanpage(multi)
                # print(str_mp)
                # we consume this node here, pop it from parts so we
                # don't visit it again as an argument
                parts.pop(idxnextwordnode)
               # endpos = nextwordnode.pos[1]
            except errors.ProgramDoesNotExist:
                logger.info('no manpage %r for multicommand %r',
                            multi, manpage)

        # create a new matchgroup for the current command
        self.manpagestack.append(manpage)
        self.description.append(str_mp)

        #------------不优雅的特殊处理------------------
        if manpage.command == 'sudo' or manpage.command == 'xargs':
            self.nested = True
        if manpage.command == 'sudo':
            self.description.append("The default target user is root. ")
        elif manpage.command == 'python':
            self.description[-1] = self.description[-1][:-2]
            self.description.append(", python. ")
        #---------------------------------------------
        return True

    def endcommand(self):
        '''
        if self.compoundstack: #没有解析manpage
            return
        '''
        if self.manpagestack: 
            logger.info("Ending of a command in a compound.")
            self.manpagestack.pop()
        else:
            logger.info("False manpagestack, probably forget to append somewhere.")
        self.opt_des = False
        self.nested = False # 一定是开始了一个新的command，之前的Nested无效

    def visitcommand(self, n, parts):
        #assert parts

        # look for the first WordNode, which might not be at parts[0]
        idxwordnode = bashlex.ast.findfirstkind(parts, 'word')
        if idxwordnode == -1:
            self.manpagestack.append(None)
            logger.info(
                'no words found in command (probably contains only redirects)')
            return

        wordnode = parts[idxwordnode]

        if self.compoundstack:
            self.manpagestack.append(None)
            logger.info('inside a compund, giving up on %r', wordnode.word)
            self.description.append(" " + wordnode.word)
            parts.pop(idxwordnode)
            return

        # check if this refers to a previously defined function
        if wordnode.word in self.functions:
            logger.info('word %r is a function, not trying to match it or its '
                        'arguments', wordnode)
            self.manpagestack.append(None)
            # first, add a matchresult for the function call
            self.description.append("Call the predefined function \"" + wordnode.word + "\". ")

            # this is a bit nasty: if we were to visit the command like we
            # normally do it would try to match it against a manpage. but
            # we don't have one here, we just want to take all the words and
            # consider them part of the function call
            first_para = False
            for part in parts:
                # maybe it's a redirect...
                if part.kind != 'word':
                    self.visit(part)
                else:
                    # this is an argument to the function
                    if part is not wordnode:
                        if not first_para:
                            self.description.append("The arguments of the function are: " + part.word)

                        # do not visit any expansions in there
                        # for ppart in part.parts:
                        #    self.visit(ppart)

            # we're done with this commandnode, don't visit its children
            return False

        self.startcommand(n, parts)

    def visitfunction(self, n, name, body, parts):
        self.functions.add(name.word)
        def _iscompoundopenclosecurly(compound):
            first, last = compound.list[0], compound.list[-1]
            if (first.kind == 'reservedword' and last.kind == 'reservedword' and
                    first.word == '{' and last.word == '}'):
                return True

        # if the compound command we have there is { }, let's include the
        # {} as part of the function declaration. normally it would be
        # treated as a group command, but that seems less informative in this
        # context
        if _iscompoundopenclosecurly(body):
            # create a matchresult until after the first {
            self.description.append(helpconstants._function + \
                "\"" + name.word + "\", and it does { ")

            # visit anything in between the { }
            for part in body.list[1:-1]:
                self.visit(part)
            self.description.append( "}. ")
        else:
            beforebody = bashlex.ast.findfirstkind(parts, 'compound') - 1
            assert beforebody > 0
            beforebody = parts[beforebody]

            # create a matchresult ending at the node before body
            self.description.append(helpconstants._function + \
               "\"" + name.word + "\", and it does { ")

            # visit anything in between the { }
            self.visit(body)
            self.description.append("}. ")
      
        return False

    def visitword(self, n, word):
        def attemptfuzzy(chars):
            m = []
            if chars[0] == '-':
                tokens = [chars[0:2]] + list(chars[2:])
                considerarg = True
            else:
                tokens = list(chars)
                considerarg = False

            pos = n.pos[0]
            prevoption = None
            for i, t in enumerate(tokens):
                op = t if t[0] == '-' else '-' + t
                opt_para = self.find_option(op)
                if opt_para:
                    self.opt_des = False
                    if considerarg and not m and opt_para.expectsargname:
                        logger.info(
                            'option %r expected an arg, taking the rest too', opt_para)
                        # reset the current option if we already took an argument,
                        # this prevents the next word node to also consider itself
                        # as an argument
                        self._currentoption = None
                        # print("%r"%opt_para)
                        if chars[2:] != "":
                            return [opt_para.text+" The \"" + opt_para.expectsargname + "\" is '" + chars[2:] + "'. "]
                        else:
                            return [opt_para.text+" The \"" + opt_para.expectsargname + "\" is unknown."]

                    mr = opt_para.text
                    m.append(mr)
                # if the previous option expected an argument and we couldn't
                # match the current token, take the rest as its argument, this
                # covers a series of short options where the last one has an argument
                # with no space between it, such as 'xargs -r0n1'
                elif considerarg and prevoption and prevoption.expectsargname:
                    pmr = m[-1]
                    mr = pmr + " The \"" + prevoption.expectsargname +"\" is '" + \
                        ''.join(tokens)[i+1:] + "'."
                    m[-1] = mr
                    # reset the current option if we already took an argument,
                    # this prevents the next word node to also consider itself
                    # as an argument
                    self._currentoption = None
                    break
                else:
                    if self.opt_des:
                        m.append(", \"" + t + "\"")
                    else:
                        m.append("with option or argument \"" + t + "\"")
                        self.opt_des = True
                   # self._currentoption = None
                pos += len(t)
                prevoption = opt_para
            return m

        def _visitword(node, word):
            if self.compoundstack:
                logger.info('inside a compund, giving up on %r', word)
                self.description.append(" " + word)
                return
            manpage = None
            try:
                manpage = self.manpagestack.pop()
            except:
                logger.info("pop from empty manpagestack when visiting word %s."%word)
            # append回去
            self.manpagestack.append(manpage)
            if manpage is None:
                logger.info('inside an unknown command, giving up on %r', word)
                if self.opt_des:
                    self.description.append(", \"" + word + "\"")
                else:
                    self.description.append("with option or argument \"" + word + "\"")
                    self.opt_des = True
                return

            logger.info('trying to match token: %r', word)

            self._prevoption = self._currentoption
            # print(self._prevoption, word, self._prevoption.expectsarg if self._prevoption else "no")
            if word.startswith('--'):
                word = word.split('=', 1)[0]
                # print("split")
            opt_para = self.find_option(word)
          #  print(word)
          #  print("%r"%option)
            if opt_para:
            # ----------------------sudo,xargs特殊处理------------------
                if manpage.command != 'sudo' and manpage.command != 'xargs':
                    self.nested = False
                    self.prenode = None
            #-----------------------------------------------------------    
                self.opt_des = False
                logger.info('found an exact match for %r: %r', word, opt_para)
                mr = opt_para.text
                self.description.append(mr)

                # check if we splitted the word just above, if we did then reset
                # the current option so the next word doesn't consider itself
                # an argument
                if word != node.word:
                    self._currentoption = None
                    self.description.append(" The \"" + opt_para.expectsargname + "\" is '" + node.word[len(word) +1:] + "'. ")
            else:
                word = node.word

                # check if we're inside a nested command and this word marks the end
                '''
                if isinstance(self.groupstack[-1][-1], list) and word in self.groupstack[-1][-1]:
                    logger.info('token %r ends current nested command', word)
                    self.endcommand()
                    mr = matchresult(
                        node.pos[0], node.pos[1], self.matches[-1].text, None)
                    self.matches.append(mr)
                '''
                if word != '-' and word.startswith('-') and not word.startswith('--'):
                    logger.debug('looks like a short option')
                    # ----------------------sudo,xargs特殊处理------------------
                    if manpage.command != 'sudo' and manpage.command != 'xargs':
                        self.nested = False
                        self.prenode = None
                    #-----------------------------------------------------------
                    if len(word) > 2:
                        logger.info("trying to split it up")
                        for txt in attemptfuzzy(word):
                            self.description.append(txt)
                    else:
                        if self.opt_des:
                            self.description.append(", \"" + word + "\"")
                        else:
                            self.description.append("with option or argument \"" + word + "\"")
                            self.opt_des = True
                elif self._prevoption and self._prevoption.expectsargname:
                    # print("here")
                    # ----------------------sudo,xargs特殊处理------------------
                    if manpage.command != 'sudo' and manpage.command != 'xargs':
                        self.nested = False
                        self.prenode = None
                    #-----------------------------------------------------------

                    self.nested = False
                    logger.info("previous option possibly expected an arg, and we can't"
                                " find an option to match the current token, assuming it's an arg")
                    '''
                    ea = self._prevoption.expectsarg
                    
                    possibleargs = ea if isinstance(ea, list) else []
                    take = True
                    if possibleargs and word not in possibleargs:
                        take = False
                        logger.info('token %r not in list of possible args %r for %r',
                                    word, possibleargs, self._prevoption)
                    if take:
                        
                        if self._prevoption.nestedcommand:
                            logger.info(
                                'option %r can nest commands', self._prevoption)
                            if self.startcommand(None, [node]):
                                self._currentoption = None
                                return
                        self.description += "The nested command is \"" + word + "\""
                        
                        logger.info("Haven't dealt with nested command.")
                '''
                    self.description.append(" The \"" + self._prevoption.expectsargname + "\" is '" + word + "'. ")
                else:
                    # --------------不优雅的特殊处理：可以开启一个新command的命令------------
                    if self.nested:
                        if self.prenode:
                            if self.startcommand(None, [self.prenode, n]):
                                self.prenode = None
                                self.manpagestack.pop(-2)
                                if self.description[-2] != self.description[-1]: #multicommand
                                    self.description.pop(-2)
                                    self._currentoption = None
                                    self.nested = False
                                    return
                                self.description.pop(-2)
                        else:
                            if self.startcommand(None, [n]):
                                self._currentoption = None
                                self.prenode = n
                            return
                    # ---------------------------------------------------------------------
                    if self.opt_des:
                        self.description.append(", \"" + word + "\"")
                    else:
                        self.description.append("with option or argument \"" + word + "\"")
                        self.opt_des = True
        _visitword(n, word)

    def visitassignment(self, n, word):
        assign_objs = word.split("=")
        assign_objs.reverse()
        pre_obj = assign_objs[0]
        for obj in assign_objs[1:]:
            self.description.append("Assign the value of " + pre_obj + " to " + obj + ". ")
        return False

    def visitreservedword(self, n, word):
        # first try the compound reserved words
        helptext = ""
        if self.compoundstack:
            # currentcompound = self.compoundstack[-1]
            helptext = helpconstants.COMPOUNDRESERVEDWORDS.get(word)

        # try these if we don't have anything specific
        if helptext == "" or helptext is None:
            if word == '{': # 在group中不需要特殊处理List
                self.groups += 1
            elif word == '}':
                self.groups -= 1
            helptext = helpconstants.RESERVEDWORDS[word]

        self.description.append(helptext)

    def visitparameter(self, n, value):
        return
    '''
        if self.compoundstack:
            return
        try:
            int(value)
            kind = 'digits-' + value + " "
        except ValueError:
            kind = helpconstants.parameters.get(value, value)
        self.description += "parameter:" + kind
    '''

    def visittilde(self, n, value):  # 不特殊处理
        return False

    def visitredirect(self, n, input, type, output, heredoc):
        if self.description[-1][-2:] == ". ":
            helpredirect = helpconstants.REDIRECTION
        elif self.description[-1][-1:] == ".":
            helpredirect = " " + helpconstants.REDIRECTION
        else:
            helpredirect = ". " + helpconstants.REDIRECTION
    
        helptext = [helpredirect]

        if type == '>&' and isinstance(output, int):
            type = type[:-1]
        
        if type in helpconstants.REDIRECTION_KIND:
            helptext.append(helpconstants.REDIRECTION_KIND[type])
        self.description.append(''.join(helptext))
        if isinstance(output, bashlex.ast.node):
            self.description.append("\""+output.word+"\" ")
        else:
            try:
                int(output)
                self.description.append("file descriptor " + str(output))
            except:
                self.description += str(output)
        if input:
            try:
                int(input)
                self.description.append(". The redirected input is file descriptor " + str(input) + ". ")
            except:
                self.description.append(". The redirected input is " + str(input) + ". ") #或许可以特殊处理Input（数字类型？）
            ''' 不处理嵌套
            for part in output.parts:
                self.visit(part)
            '''

        return False

    def visitheredoc(self, n, value):
        pass

    def visitprocesssubstitution(self, n, command): #不嵌套处理
        return False

    def visitcommandsubstitution(self, n, command):
        return False

    def parse_vis(self):
        logger.info('Parse and Understand %s', self.command)
        try:
            self.ast = bashlex.parser.parsesingle(
                self.command, expansionlimit=1)  # 目前不支持嵌套command
        except:
            logger.info("Sorry, the hierarchy format of your command line is too confused to be parsed.")
            sys.exit(127)
        if self.ast:
            self.visit(self.ast)
        else:
            logger.warn('No AST generated for %s', self.command)
            print_err('No AST generated for %s', self.command)
            sys.exit(127)
