#!/usr/bin/env python

import os
import json
import argparse
import datetime

dirname = os.path.expanduser('~/.borednow')
path_yak = dirname + '/yak.json'


def show_help(msg='', code=1):
    print 'YOU DID IT WRONG'
    if (msg):
        print msg
    exit(code)


def ensure_files():
    # Mkdir if it doesn't exist
    if not os.path.isdir(dirname):
        os.makedirs(dirname)
    if not os.path.isfile(path_yak):
        f = open(path_yak, 'w')
        f.write('[]')
        f.close()


def get_yak_stack():
    ensure_files()
    f = open(path_yak, 'r')
    raw_json = f.read()
    f.close()
    stack = json.loads(raw_json)
    return stack


def save_yak_stack(stack):
    f = open(path_yak, 'w')
    json_str = json.dumps(stack, indent=4)
    f.write(json_str)
    f.close()


def add_yak_frame(stack, message):
    frame = {'text': message, 'timestamp': str(datetime.datetime.now())}
    stack.append(frame)
    save_yak_stack(stack)
    return frame


def pop_yak_frame(stack):
    if (len(stack)):
        stack.pop()
        save_yak_stack(stack)


def print_yak_frame_count(stack):
    count = len(stack)
    if (count):
        print 'You are currently %i yak %s deep' % (count, 'frame' if (count == 1) else 'frames')
    else:
        print 'No yaks to shave right now!'


def print_yak_stack(stack):
    spaces = -2
    for frame in stack:
        print '%s%s%s' % (' ' * spaces if (spaces > 0) else '', u'\u2937 ' if (spaces >= 0) else '', frame['text'])
        spaces += 3


def print_yaks(stack):
    print_yak_frame_count(stack)
    print_yak_stack(stack)


parser = argparse.ArgumentParser(description='Yak Stack!')
parser.add_argument('message', nargs='?', default='')
parser.add_argument('-l', '--list', action='store_true')
parser.add_argument('-p', '--pop', action='store_true')
args = parser.parse_args()

stack = get_yak_stack()

if args.message:
    add_yak_frame(stack, args.message)
elif args.pop:
    pop_yak_frame(stack)
# elif args.list:
#     print_yak_stack(stack)

print_yaks(stack)
