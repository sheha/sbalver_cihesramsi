#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
SECOND PROBLEM

Braces Balancing check based on stacking.

@author: Ismar Sehic, <https://github.com/sheha>

June, 2017

"""

import re

in_text = 'Python {is an easy to [learn]}, (powerful programming language. It)' \
          'has efficient high­level [(data structures) and a simple but' \
          'effective approach to object­oriented programming]. Python’s elegant' \
          'syntax and dynamic typing, together with its {interpreted nature,' \
          'make it an ideal language (for) scripting and rapid} application' \
          'development in many areas on most platforms.'


def balance_checker(extract):
    """
    Determines braces balance using stacking mechanism to preserve opening braces when encountered,
    popping the last one out to compare against current closing brace.If they are a pair, loop forward.
    Stack is empty in the end, if they're balanced.    
    """

    balanced_set = {('(', ')'), ('[', ']'), ('{', '}')}
    stack = []

    for ch in extract:

        if ch == '[' or ch == '{' or ch == '(':
            stack.append(ch)

        else:
            if len(stack) == 0:
                return False
            last_open = stack.pop()
            if (last_open, ch) not in balanced_set:
                return False

    return len(stack) == 0


def main():
    """
    Extracting all three sort of braces from our known string for less overhead,
    and running them through balance_checker
    """
    extracted_braces = re.sub(r'[^(){}[\]]', '', in_text)

    print 'Braces are balanced' if balance_checker(extracted_braces) else 'Braces are not balanced'


if __name__ == '__main__':
    main()
