#!/usr/bin/python
# -*- coding: utf-8 -*-

import ipdb


def main(file1, file2):
    match_sort_output(readfile(file1), readfile(file2))


def readfile(f):
    """
    Reads the file lines in a set of tuples, with type conversion for common id.
    """
    types = str, int

    with open(f) as infile:
        result = set()

        for line in infile:
            result.add(tuple(t(e) for t, e in zip(types, line.rstrip().split())))

    return result


def match_sort_output(content1, content2):
    """ 
    Simply prints out the result of nested helper _matcher(), 
    that way we get a memory optimization and perf gain when _matcher does it's thing
    and returns matched result set,
    instead of keeping everything in this functions scope
    """

    def _matcher():
        """
        Matches file contents by turning tuple sets into dictionaries: 
            d1 = {4321: ['John'], 1234: ['Adam']}
            d2 = {4321: ['Anderson', 4321], 1234: ['Smith', 1234]}
            
        then does a set union by key, returning matched list of lists which is converted back to 
        set of tuples for performance when sorting or whatever we want to do with the matches later...
        
            result = [('Adam', 'Smith', 1234), ('John', 'Anderson', 4321)]
                
        :return: set of match tuples sorted by the id
        """
        d1, d2 = {}, {}
        for item in content1:
            d1.setdefault(item[1], []).append(item[0])
        print d1
        for item in content2:
            d2.setdefault(item[1], []).extend(item)
        print d2

        result = [d1.get(key, []) + d2.get(key, []) for key in d1.viewkeys() | d2]

        result = set(tuple(item) for item in result if len(item) > 1)

        return sorted(result, key=lambda x: x[-1])

    ipdb.set_trace()
    print _matcher()


def input_validation():
    """
    Validates the files existence, 
    sets the default path of both files to be in the same folder as the script itself,
    so if no files provided, points the script to the defaults.
        
    :return: argparse parser object
    """
    import os
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

    parser = ArgumentParser(description=__doc__, formatter_class=ArgumentDefaultsHelpFormatter)

    parser.add_argument("-in1", "--infile1", dest="file1", type=lambda x: _file_exists(parser, x), nargs="?",
                        const="file1.txt", default="file1.txt", required=False,
                        help="line layout --> <first name> <ID number>", metavar="FILE")

    parser.add_argument("-in2", "--infile2", dest="file2", type=lambda x: _file_exists(parser, x), default="file2.txt",
                        required=False, help="line layout --> <last name> <ID number>", metavar="FILE")

    def _file_exists(pars, arg):
        arg = os.path.abspath(arg)
        return arg if os.path.exists(arg) else pars.error("The file %s does not exist!" % arg)

    return parser


if __name__ == "__main__":
    args = input_validation().parse_args()
    main(args.file1, args.file2)
