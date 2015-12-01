#!/usr/bin/python

import os
import re
import sys

# https://github.com/bizcor/system-command
sys.path.append(os.environ['HOME'] + '/Dropbox/sys/python/lib/mylib')
from system_command import system_command

# the string to search for in the Author field of each commit
USER = os.environ.get('GIT_VDIFF_USER')
if USER is None:
    USER = os.environ.get('USER')

# this regex will be applied to lines like this:
#    :000000 100644 0000000... e9e6cc9... A      README.md
FILE_STATS_LINE_REGEX = re.compile(
    '^:([0-7]{6})\s+([0-7]{6})\s+([\da-f]+)[.]+'
    '\s+([\da-f]+)[.]+\s+([A-Z])\s+(.*)'
)

VIMRC_FILE = "{}/.my-vimdiffrc".format(os.environ['HOME'])


def always_include():
    ''' check the environment for a whitespace delimited list of sha's.  this
        will represent a list of commits always to process, despite the author.
    '''
    env_include = os.environ.get('ALWAYS_INCLUDE')
    if env_include is None:
        return None
    include = env_include.split()
    return include


def parse_commits():
    '''
    parse the output of the git whatchanged command.  return an array of dicts.
    '''
    command_state \
        = system_command(
              ['git', 'whatchanged', '--no-color'], return_state=True)
    output = command_state['stdout'].split('\n')

    count = 0
    commits = []
    buf = {'files': {}}

    for line in output:
        count += 1
        if len(line) == 0 or line[0] in [' ', '     ']:
            continue
        if re.search('^commit ', line):
            sha = re.sub('^commit ', '', line)
            if count != 1:
                commits.append(buf)
                buf = {'files': {}}
            buf['sha'] = sha
        elif re.search('^:[0-7]{6} ', line):
            match = re.match(FILE_STATS_LINE_REGEX, line)
            previous_mode = match.group(1)
            current_mode = match.group(2)
            previous_sha = match.group(3)
            current_sha = match.group(4)
            change_type = match.group(5)
            path = match.group(6)
            buf['files'][path] = {
                'previous_mode': previous_mode,
                'current_mode': current_mode,
                'previous_sha': previous_sha,
                'current_sha': current_sha,
                'change_type': change_type,
            }
        elif re.search('^Date: ', line):
            buf['date'] = re.sub('^Date:   ', '', line)
        elif re.search('^Author: ', line):
            buf['author'] = line
            buf['author'] = re.sub('^Author: ', '', line)
        elif re.search('^Merge: ', line):
            buf['merge'] = re.sub('^Merge: ', '', line)
    commits.append(buf)
    return commits


def previous_commit(commits, sha):
    '''
    given a list of commits and a sha, return the sha representing the commit
    one before the commit represented by the given sha.
    '''
    next_one_is_it = False
    for c in commits:
        if next_one_is_it:
            return c['sha']
        if c['sha'] == sha:
            next_one_is_it = True


def main():
    ALWAYS_INCLUDE = always_include()
    print "USER => '{}'".format(USER)

    debug = os.environ.get('GIT_VDIFF_DEBUG')

    if len(sys.argv) > 1:
        working_directory = sys.argv[1]
        os.chdir(working_directory)

    commits = parse_commits()

    count = 0
    for commit in reversed(commits):
        sha = commit['sha']
        author = commit['author']

        disqualify_based_on_user = False
        if USER is not None:
            if USER not in author:
                disqualify_based_on_user = True

        include_unconditionally = False
        if ALWAYS_INCLUDE is not None:
            if sha in ALWAYS_INCLUDE:
                include_unconditionally = True

        if disqualify_based_on_user:
            if not include_unconditionally:
                continue

        date = commit['date']
        files = commit['files']
        for path in files:
            count += 1

            previous_mode = files[path]['previous_mode']
            current_mode = files[path]['current_mode']
            previous_file_sha = files[path]['previous_sha']
            current_file_sha = files[path]['current_sha']
            change_type = files[path]['change_type']
            short_sha = sha[:7]
            a = '<( echo {}... {}:a/{} [{}] {} "#{}" ; git show {} )'.format(
                short_sha, previous_file_sha, path, change_type, date, count,
                previous_file_sha)
            b = '<( echo {}... {}:b/{} [{}] {} "#{}" ; git show {} )'.format(
                short_sha, current_file_sha, path, change_type, date, count,
                current_file_sha)

        if debug is None:
            print "vimdiff -u {} {} {}".format(VIMRC_FILE, a, b)

        else:
            print
            print "commit {}".format(sha)
            print "Author: {}".format(author)
            print "Date:   {}".format(date)
            for path in files:
                previous_mode = files[path]['previous_mode']
                current_mode = files[path]['current_mode']
                previous_sha = files[path]['previous_sha']
                current_sha = files[path]['current_sha']
                change_type = files[path]['change_type']
                print ":{} {} {}... {}... {}  {}".format(previous_mode,
                                                         current_mode,
                                                         previous_sha,
                                                         current_sha,
                                                         change_type,
                                                         path)

if __name__ == '__main__':
    sys.exit(main())
