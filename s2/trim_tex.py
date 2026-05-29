#!/usr/bin/env python3
import re
import sys

MIN_LEN = 100
HARD_LEN = 140
MIN_TAIL = 10

def find_cut(line, start):
    for i in range(start, len(line)):
        c = line[i]
        if c in '.,;:)]}':
            cut = i + 1
            tail = line[cut:].lstrip()
            if len(tail) >= MIN_TAIL:
                return cut
        if c == '$' and i > start:
            cut = i
            tail = line[cut:].lstrip()
            if len(tail) >= MIN_TAIL:
                return cut
    for i in range(HARD_LEN, len(line)):
        if line[i] == ' ':
            tail = line[i+1:]
            if len(tail.lstrip()) >= MIN_TAIL:
                return i + 1
    return -1

def wrap_line(line, min_len=MIN_LEN, hard_len=HARD_LEN):
    if len(line.rstrip()) <= min_len:
        return [line.rstrip()]

    stripped = line.lstrip()
    if stripped.startswith('%') or stripped.startswith('\\begin') or stripped.startswith('\\end'):
        return [line.rstrip()]

    indent = len(line) - len(stripped)
    prefix = ' ' * indent

    result = []
    current = line.rstrip()

    while len(current) > min_len:
        cut = find_cut(current, min_len)
        if cut == -1:
            break
        result.append(current[:cut].rstrip())
        current = prefix + current[cut:].lstrip()

    result.append(current)
    return result

def process_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    out = []
    for line in lines:
        wrapped = wrap_line(line.rstrip('\n'))
        out.extend(l + '\n' for l in wrapped)

    with open(path, 'w', encoding='utf-8') as f:
        f.writelines(out)

if __name__ == '__main__':
    for path in sys.argv[1:]:
        process_file(path)
