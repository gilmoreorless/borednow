#!/usr/bin/env python

import os
import json
import argparse
import random

dirname = os.path.expanduser('~/.borednow')
path_tasks = dirname + '/tasks.json'
path_state = dirname + '/state.json'
tasks_cache = []
state_cache = {}
max_skips = 5


def show_help(msg='', code=1):
    print 'YOU DID IT WRONG'
    if (msg):
        print msg
    exit(code)


def ensure_files():
    # Mkdir if it doesn't exist
    if not os.path.isdir(dirname):
        os.makedirs(dirname)
    if not os.path.isfile(path_tasks):
        f = open(path_tasks, 'w')
        f.write('[]')
        f.close()
    if not os.path.isfile(path_state):
        f = open(path_state, 'w')
        f.write('{}')
        f.close()


def get_state():
    global state_cache
    ensure_files()
    if len(state_cache) == 0:
        f = open(path_state, 'r')
        raw_json = f.read()
        f.close()
        state_cache = json.loads(raw_json)
    return state_cache


def get_tasks():
    global tasks_cache
    ensure_files()
    if len(tasks_cache) == 0:
        f = open(path_tasks, 'r')
        raw_json = f.read()
        f.close()
        tasks_cache = json.loads(raw_json)
    return tasks_cache


def get_random_task():
    tasks = filter(filter_active, get_tasks())
    return random.choice(tasks)


def get_current_task():
    state = get_state()
    return state.get('current_task')


def set_current_task(task):
    state = get_state()
    state['current_task'] = task
    save_state(state)


def save_state(state):
    f = open(path_state, 'w')
    json_str = json.dumps(state, indent=4)
    f.write(json_str)
    f.close()


def write_tasks(tasks):
    f = open(path_tasks, 'w')
    json_str = json.dumps(tasks, indent=4)
    f.write(json_str)
    f.close()


def add_task(task_str):
    tasks = get_tasks()
    id = len(tasks)
    task = {'id': id, 'text': task_str, 'done': False}
    tasks.append(task)
    write_tasks(tasks)


def update_task(task):
    tasks = get_tasks()
    id = task['id']
    for i in range(0, len(tasks)):
        if tasks[i]['id'] == id:
            tasks[i] = task
            break
    write_tasks(tasks)


def print_task(prefix, task):
    print '{0}: (#{1}) {2}'.format(prefix, task['id'], task['text'])


def filter_active(x):
    return not x['done']


parser = argparse.ArgumentParser(description='Bored Now!')
parser.add_argument('-a', '--add')
parser.add_argument('-d', '--done', action='store_true')
parser.add_argument('-s', '--skip', action='store_true')
args = parser.parse_args()

if args.add:
    add_task(args.add)
    exit(0)

current = get_current_task()
was_skipped = False
if current:
    if args.done:
        current['done'] = True
        update_task(current)
        set_current_task(None)
        state = get_state()
        state['skips'] = 0
        save_state(state)
        print_task('TASK MARKED AS DONE', current)
    elif args.skip:
        state = get_state()
        skips = state.get('skips', 0)
        if skips == max_skips:
            print '!!! No more skips allowed - you have to do this one !!!'
            print_task('DO IT', current)
            exit(1)
        was_skipped = True
        state['skips'] = skips + 1
        save_state(state)
        print_task('TASK SKIPPED', current)
    else:
        print_task('CURRENT TASK', current)
    if not was_skipped:
        exit(0)

if not was_skipped:
    if args.done:
        print '!!! No current task to mark as done !!!'
        exit(1)

    if args.skip:
        print '!!! No current task to skip !!!'
        exit(1)

tasks = filter(filter_active, get_tasks())
if len(tasks) == 0:
    print '!!! No unfinished tasks available !!!'
    exit(1)

task = get_random_task()
if not task:
    print 'ERROR: Could not get a new task'
    exit(2)

set_current_task(task)
print_task('NEW TASK', task)
