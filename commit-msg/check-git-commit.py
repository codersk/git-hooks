#!/usr/bin/env python

import sys
import os
import re

from subprocess import call

if "EDITOR" in os.environ.keys():
    editor = os.environ["EDITOR"]
else:
    editor = "/usr/bin/nano"

message_file = sys.argv[1]
error_header = '# GIT COMMIT MESSAGE FORMAT ERRORS:'

#Regex patterns
regex1 = r"^\w+"
regex2 = r"^(feat|fix|docs|style|refactor|test|chore)"

def check_format_rules(lineno, line):
    real_lineno = lineno + 1
    if lineno == 0:
        words = line.split(' ')
        r1 = re.search(regex1, line, re.IGNORECASE | re.DOTALL | re.UNICODE)
        r2 = bool(re.search(regex2, r1.group()))
        r3 = bool(re.search(regex2, words[0]))
        col_index = line.find(":")
        header_length = len(line)
        header_error = ""
        header_format = "\n  HEADER SYNTAX:\n" \
        "  <type>:(refs <scope>) <subject>\n"
        header_type_error = "  Allowed types are:\n" \
            "    * feat      - (feature)\n" \
            "    * fix       - (bug fix)\n" \
            "    * docs      - (documentation)\n" \
            "    * style     - (formatting, missing semi colons,...)\n" \
            "    * refactor  - (refactor)\n" \
            "    * test      - (when adding missing tests)\n" \
            "    * chore     - (maintain)"
        if not r2:
            return "E%d: First word must be a valid <type>\n%s%s" % (real_lineno, header_format, header_type_error)
        else:
            if r2 == r3:
                if col_index > -1:
                    s1 = line.find("(")
                    s2 = line.find(")")
                    ss = line.split(':')[1]
                    scope = ss[ss.find("(")+1:ss.find(")")]
                    if col_index < 10:
                        if s1 == -1:
                            header_error +="  Opening Parenthesis '(' is missing\n"
                        if not s1 == col_index+1:
                            header_error += "  <scope> is missing \n"
                        else:
                            if s1 > col_index+1:
                                header_error +="  <scope> is missplaced \n"
                            else:
                                if s2 == -1:
                                    header_error +="  Closing Parenthesis ')' is missing\n"
                        if s1+1 == s2 or scope == ' ':
                            header_error +="  <scope> is empty \n"
                        if s2 > -1 and (not (len(line)-1) == (s2+len(line.split(")",1)[1]))):
                            header_error +="  <subject> is missing\n "

                        if len(header_error)>0:
                            return "E%d: %s%s\n" % (real_lineno, header_error, header_format)
                    else:
                        return "E%d: <scope> is missplaced \n%s " % (real_lineno, header_format)
                else:
                    return "E%d: ':' is missing\n%s " % (real_lineno, header_format)
                if len(line) > 50:
                    return "E%d: First line should be less than 50 characters " \
                            "in length." % (real_lineno,)
    if lineno == 1:
        if line:
            return "E%d: Second line should be a blank line" % (real_lineno,)
    if lineno == 2:
        if line.startswith('#') or not len(line) > 0:
            return "E%d: Third line should be BODY.\n" \
                "   The BODY should include the motivation for the change and contrast this\n" \
                "   with previous behavior, and must be phrased in imperative present tense" % (real_lineno,)
    # if lineno == 3:
    #     if line:
    #         return "E%d: Line no %d should be a blank line" % (real_lineno,real_lineno)
    # if lineno == 4:
    #     if line.startswith('#') or not len(line) > 0:
    #         return "E%d: Last line should contain references.\n" % (real_lineno,)
    if not line.startswith('#'):
        if len(line) > 72:
            return "E%d: No line should be over 72 characters long." % (real_lineno,)
    return False

def read_commit_message():
    commit_msg = list()
    errors = list()
    empty_lines = 0
    with open(message_file) as commit_fd:
        for lineno, line in enumerate(commit_fd):
            stripped_line = line.strip()
            if stripped_line == error_header:
                break
            if not stripped_line:
                empty_lines +=1
            if not empty_lines < 3:
                errors.append("\n  %d blank lines\n" % (empty_lines) )
                break
            commit_msg.append(line)
            e = check_format_rules(lineno, stripped_line)
            if e:
                errors.append(e)
        return [commit_msg, errors]

# Print commit erros on console and write them in commit message file
while True:
    res = read_commit_message()
    commit_msg = res[0]
    errors = res[1]
    if errors:
        print("-----------------------------------------------------------------------")
        print("--------------------------- :COMMIT ERRORS: ---------------------------")
        print("-----------------------------------------------------------------------")
        with open(message_file, 'w') as commit_fd:
            for line in commit_msg:
                commit_fd.write(line)
            commit_fd.write('%s\n' % (error_header,))
            for error in errors:
                print(error),
                for eline in error.split('\n'):
                    commit_fd.write('#    %s\n' % (eline,))

        re_edit = input('-----------------------------------------------------------------------\n' \
                'Invalid git commit message format. Would you like to re-edit it?' \
                '\n-----------------------------------------------------------------------\n' \
                '(If you answer no, your commit will fail) [Y/n] : ')
        if re_edit in ('N', 'n', 'NO', 'no', 'No', 'nO'):
            sys.exit(1)
        if re_edit in ('Y', 'y', 'Yes', 'YEs', 'YES', 'YEs', 'yeS', 'yEs'):
            call('%s %s' % (editor, message_file), shell=True)
        continue
    break
