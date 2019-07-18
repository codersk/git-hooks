#!/usr/bin/env python

import sys

from subprocess import call

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
            
        return [commit_msg, errors]

# Print commit erros on console and write them in commit message file
while True:
    res = read_commit_message()
    commit_msg = res[0]
    errors = res[1]
    print("Commt Message: %s" % (commit_msg));
    print("Errors: %s" % (errors));
