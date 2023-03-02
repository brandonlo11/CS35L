import argparse
import random
import sys

parser = argparse.ArgumentParser(description='Generate random permutations of input lines')
parser.add_argument('input', nargs='*', help='input file (defaults to standard input), or list of arguments given the echo case')
parser.add_argument('-e', '--echo', action='store_true', help='treat each ARG as an input line')
parser.add_argument('-i', '--input-range', help='treat each number LO through HI as an input line')
parser.add_argument('-n', '--head-count', type=int, help='output at most COUNT lines')
parser.add_argument('-r', '--repeat', action='store_true', help='output lines can be repeated')
#parser.add_argument('--help', action='help', help='show this help message and exit')

args = parser.parse_args()

# if args.help:
    #print('')
    
lines = []
if args.input_range:
    low, high = map(int, args.input_range.split('-'))
    lines = [str(x) + '\n' for x in range(low, high + 1)]
elif args.echo:
    for index in range(len(args.input)):
        lines.append(args.input[index]+'\n')
elif len(args.input) == 0 or '-' == args.input[0]:
    lines = sys.stdin.readlines()
else:
    try:
        f = open(args.input[0], 'r')
        lines = f.readlines()
        f.close()
    except Exception as e:
        parser.error ('Not a valid file')

#if not args.repeat:
#    lines = list(set(lines))
    
if args.head_count and args.repeat:
    for index in range(args.head_count):
        sys.stdout.write(random.choice(lines))
elif not args.head_count and not args.repeat:
    for line in random.sample(lines, len(lines)):
        sys.stdout.write(line)
else:
    while True:
        sys.stdout.write(random.choice(lines))
