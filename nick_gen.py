#!/usr/bin/env python3
"""Nickname generator"""

import argparse
import random
import os
import sys
import re

g_l33t = {'A': '4', 'B': '|3', 'C': '(', 'D': '|)', 'E': '3', 'F': '|=', 'G': '(-',
          'H': '|-|', 'I': '!', 'J': '_|', 'K': '|<', 'L': '1', 'M': '|v|', 'N': '~',
          'O': '0', 'P': '|*', 'Q': '0_', 'R': '|2', 'S': '5', 'T': '+', 'U': '|_|',
          'V': '|/', 'W': "'//", 'X': '><', 'Y': "'/", 'Z': '2'}


# ---------------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(description='Nickname generator',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-n',
                        '--num',
                        metavar='char_number',
                        help='Sum of all ASCII characters weight, min max will not count',
                        type=int,
                        default=None)

    parser.add_argument('-m',
                        '--min',
                        metavar='minimum',
                        help='Minimum length of nickname',
                        type=int,
                        default=1)

    parser.add_argument('-x',
                        '--max',
                        metavar='maximum',
                        help='Maximum length of nickname',
                        type=int,
                        default=30)

    parser.add_argument('-l',
                        '--l33t',
                        metavar='l33t',
                        help='Make characters 1337 in percent from 0.0 to 1.0',
                        type=float,
                        default=0.0)

    parser.add_argument('-s',
                        '--seed',
                        metavar='seed',
                        help='Random seed if needed',
                        type=int,
                        default=None)

    parser.add_argument('-f',
                        '--first',
                        metavar='first',
                        help='Specify the first character',
                        type=str,
                        default=None)

    parser.add_argument('-an',
                        '--adj_noun',
                        help='Make nickname using 1 adjective and 1 noun',
                        action='store_true')

    parser.add_argument('-vn',
                        '--verb_noun',
                        help='Make nickname using 1 verb and 1 noun',
                        action='store_true')

    parser.add_argument('-nn',
                        '--noun_noun',
                        help='Make nickname using 2 nouns',
                        action='store_true')

    args = parser.parse_args()

    # Check num
    if args.num and args.num < 97:
        parser.error(f'--num "{args.num}" must be > 96')

    # Check min and max values
    if args.min < 1:
        parser.error(f'--min "{args.min}" must be > 0')
    if args.max < args.min:
        parser.error(f'--max "{args.max}" must be >= --min "{args.min}"')

    # Check l33t %
    if not 0.0 <= args.l33t <= 1.0:
        parser.error(f'--l33t {args.l33t} must be between 0.0 and 1.0')

    return args


# ---------------------------------------------------------
def main() -> None:
    args = get_args()
    random.seed(args.seed)
    words_file = 'words.txt'
    adjs_file = 'adjectives.txt'
    verb_file = 'verbs.txt'
    noun_file = 'nouns.txt'
    words = set()

    if args.adj_noun:
        words = get_duos(adjs_file, noun_file, args)
    elif args.verb_noun:
        words = get_duos(verb_file, noun_file, args)
    elif args.noun_noun:
        words = get_duos(noun_file, noun_file, args)
    else:
        words = get_words(words_file, args.num, args)

    # Print 5 words in a row
    if words:
        for i, word in enumerate(words, start=1):
            word = word if not args.l33t else word2l33t(word)
            if i % 5:
                print(f'{word:<20}', end='  ')
            else:
                print(word)
                input()
    else:
        print('[!] Sorry, no words were found suitable for the parameters\n'
              'Try another parameters or expand .txt files with new words')


# ---------------------------------------------------------
def word2num(word: str) -> str:
    """Find weight(ASCII) of the word"""

    return str(sum(map(ord, re.sub('[^A-Za-z0-9]', '', word))))


# ---------------------------------------------------------
def word2l33t(word: str) -> str:
    """Translate word into 1337 based on a fixed %"""

    length = len(word)
    percent = round(length * get_args().l33t)
    new_word = list(word)

    for i in random.sample(range(length), percent):
        new_word[i] = g_l33t[new_word[i].upper()]

    return ''.join(new_word)


# ---------------------------------------------------------
def get_handle(file_name: str):
    """Get handle to read text or exit with error"""

    if os.path.isfile(file_name):
        return open(file_name, 'rt')
    else:
        sys.exit(f'[!] {file_name} is missing, be sure you downloaded it and put in the same place with nick_gen.py')


# ---------------------------------------------------------
def get_words(file_name: str, weight_sum: int, args) -> set:
    """Get words suitable for the parameters"""

    hf = get_handle(file_name)
    words = set()

    for line in hf:
        clean_word = line.rstrip().lower()
        if args.first:
            if not re.match(f'{args.first.lower()}', clean_word):
                continue
        if args.num:
            if word2num(clean_word) == str(weight_sum):
                words.add(clean_word)
        elif args.min <= len(clean_word) <= args.max:
            words.add(clean_word)

    hf.close()
    return words


# ---------------------------------------------------------
def get_duos(first, second, args) -> set:
    """Get noun + noun, adjective + noun or verb + noun words"""

    num1 = args.num
    num2 = args.num
    if args.num:
        num1 = int(args.num / 2)  # in case you want to set specific number
        num2 = args.num - num1

    words1 = get_words(first, num1, args)
    words2 = get_words(second, num2, args)

    if words1 and words2:
        return set(random.choice(tuple(words1)) + word for word in words2)


# ---------------------------------------------------------
if __name__ == '__main__':
    main()
