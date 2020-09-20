import argparse
import re
from collections import defaultdict
import json


parser = argparse.ArgumentParser(description='Input path to a text')
parser.add_argument('path', type=str, help='Path to a text')
args = parser.parse_args()

r_alphabet = re.compile(u'[а-яА-Я0-9-]+|[.,:;?!]+')

path = 'TEXT.txt'

def gen_lines():
    data = open(args.path, "r", encoding="utf-8")
    for line in data:
        yield line.lower()


def gen_tokens(lines):
    for line in lines:
        for token in r_alphabet.findall(line):
            yield token


def get_bigramms(tokens):
    t0 = '#'
    for t1 in tokens:
        yield t0, t1
        if t1 in '.?!':
            yield t1, '#'
            t0, t1 = '#', '#'
        else:
            t0 = t1


def get_model():
    lines = gen_lines()
    tokens = gen_tokens(lines)
    bigramms = get_bigramms(tokens)

    bb, un = defaultdict(lambda: 0.0), defaultdict(lambda: 0.0)
    for t0, t1 in bigramms:
        un[t0] += 1
        bb[t0, t1] += 1

    model = {}
    for (t0, t1), freq in iter(bb.items()):
        if t0 in model:
            model[t0].append((t1, freq / un[t0]))
        else:
            model[t0] = [(t1, freq / un[t0])]
    with open("model.json", "w") as f:
        f.write(json.dumps(model))


if __name__ == '__main__':
    get_model()



