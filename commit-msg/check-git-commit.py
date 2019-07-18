#!/usr/bin/env python

import sys
import os
import re

from subprocess import call

if "EDITOR" in os.environ.keys():
    editor = os.environ["EDITOR"]
else:
    editor = "/usr/bin/nano"

#Regex patterns
regex1 = r"^\w+"
regex2 = r"^(feat|fix|docs|style|refactor|test|chore)"

def check_format_rules(lineno, line):
    real_lineno = lineno + 1
    if lineno == 0:
        if len(line) > 50:
            return "E%d: First line is the HEADER.\n " \
                " - HEADER is a single line of max. 50 characters that contains a \n" \
                "  succinct description of the change. It contains a type, an optional \n" \
                "  scope and a subject\n" \
                "  + <type> describes the kind of change that this commit is providing. \n" \
                "    Allowed types are:\n" \
                "        * feat      - (feature)\n" \
                "        * fix       - (bug fix)\n" \
                "        * docs      - (documentation)\n" \
                "        * style     - (formatting, missing semi colons,...)\n" \
                "        * refactor  - (refactor)\n" \
                "        * test      - (when adding missing tests)\n" \
                "        * chore     - (maintain)\n" \
                "  + <scope> can be anything specifying place of the commit change\n" \
                "  + <subject> is a very short description of the change, in the \n" \
                "    following format:\n" \
                "        * imperative, present tense: “change” not “changed” / “changes”\n" \
                "        * no capitalized first letter\n" \
                "        * no dot (.) at the end" % (real_lineno,)
    if lineno == 1:
        if line:
            return "E%d: Second line should be a blank line" % (real_lineno,real_lineno)
    if lineno == 2:
        if line.startswith('#') or not len(line) > 0:
            return "E%d: Third line should be BODY.\n" \
                "   The BODY should include the motivation for the change and contrast this\n" \
                "   with previous behavior, and must be phrased in imperative present tense" % (real_lineno,)
    if lineno == 3:
        if line:
            return "E%d: Line no %d should be a blank line" % (real_lineno,real_lineno)
    if lineno == 4:
        if line.startswith('#') or not len(line) > 0:
            return "E%d: Last line is FOOTER, it should contain references.\n" \
                "  The FOOTER should contain any information about Breaking Changes and is" 
                "  also the place to reference GitHub issues that this commit closes" % (real_lineno,)
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
