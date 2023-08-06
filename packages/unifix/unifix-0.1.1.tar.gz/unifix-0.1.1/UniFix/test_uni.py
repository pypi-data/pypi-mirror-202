from Uni import matcher
import sys
import re
sys.path.append(".")
test_commands = [
                 ":(){ :;};:", #-------------------------------------0 (function)
                 "echo \"hello\"| xargs -r0n1", #--------------------1 (-concated flag)
                 "echo \"hello\"", #---------------------------------2
                 "echo \"hello\" > /etc/a.txt",#---------------------3 Redirection
                 "cat < a.txt",#-------------------------------------4
                 "ls >> a.txt",#-------------------------------------5
                 "cat a.txt 2>&1", #---------------------------------6 some problem to solve 2&>1需要特殊处理吗
                 "ls -C *.jpg",#-------------------------------------7
                 "python -q", #--------------------------------------8 python的Manpage描述并不涉及Python..特殊处理？(类似的还有tar等)
                 "git log", #----------------------------------------9 (multicommand)
                 "for user in $(cut -f1 -d: /etc/passwd); do crontab -u $user -l 2>/dev/null; done", #---10(compound, substitution)
                 "javac Pair.java", #--------------------------------11
                 "ls -R *.jpg", #------------------------------------12
                 "true && { echo success; } || { echo failed; }",#---13 (operator and/or/group)
                 "file=$(echo `basename \"$file\"`)", #--------------14 (assignment/commandsubstitution)
                 "echo $user", #-------------------------------------15 (parameter: test and decide not to deal with parameter specially)
                 "cd ~", #-------------------------------------------16 (cd does not have manpage)
                 ":(){ echo $1;};: \"hello\"", #---------------------17 (function with arguments)
                 "ls | less", #--------------------------------------18 (pip) [less- the oppsite of more...]
                 "echo \"hello\"; echo $1; ls", #--------------------19 (list)
                 'echo \"hello\"; { echo $1; }', #-------------------20 (list and group)
                 "! ls nonexistingpath && echo \"yes, nonexistingpath doesn't exist\"", #-----------21 (negation)
                 "cut -d ' ' -f 1 /var/log/apache2/access_logs | uniq -c | sort -n", #--------------22
                 "sudo echo 'hello'", #-------------------------------------------------------------23 (command - command)
                 "sudo git branch", #---------------------------------------------------------------24 (command - multicommand)
                 "sudo git branch -f",#------------------------------------------------------25 (command - multicommand, flag)
                 "sudo ls -R", #-------------------------------------------------------------26 (command - command, flag)
                 "cat volcanoes.txt | wc", #-------------------------------------------------27
                 "sudo echo 'hello' > /etc/a.txt"
                 ] 

test_command =  test_commands[28]
uni_test = matcher.Uni(test_command)
uni_test.parse_vis()
print("".join(uni_test.description))
#print("\x1B[4m" + "max-args" + "\x1B[0m")

