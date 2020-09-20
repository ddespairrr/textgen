from random import uniform
import argparse
import json


parser = argparse.ArgumentParser(description='Input path to a model')
parser.add_argument('path', type=str, help='Path to a model')
parser.add_argument('num_of_strings', type=int, help='Number of strings to generate')
args = parser.parse_args()


def rrand(seq):
    _sum, _freq = 0, 0
    for item, freq in seq:
        _sum += freq
    rnd = uniform(0, _sum)
    for token, freq in seq:
        _freq += freq
        if rnd < _freq:
            return token


def generate_sentence(model):
    sent = ''
    t0 = '#'
    t1 = '#'
    while True:
        t1 = rrand(model[t0])
        while t1 in '--.!?,:;' and t0 in '--.!?,:;' or t1 in '--.!?,:;' and t0 == '#':
            t1 = rrand(model[t0])
        if t1 == '#':
            break
        if t0 in '--.!?,:;' or t0 == '#':
            sent += t1
        else:
            if t1 in '--.!?,:;':
                sent += t1 + ' '
            else:
                sent += ' ' + t1
        t0 = t1
    return sent.capitalize()


if __name__ == '__main__':
    with open(args.path, "r", encoding="utf-8") as f:
        content = f.read()
        model = json.loads(content)
    with open("output.txt", 'w', encoding='utf-8') as f:
        for i in range(args.num_of_strings):
            f.write((generate_sentence(model)) + '\n')
