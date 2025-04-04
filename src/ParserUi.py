#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#--------------------------------
#
# Author            : Lasercata
# Last modification : 2025.04.04
# Version           : v1.0.0
#
#--------------------------------

'''File defining the user interface using argparse.'''

##-Imports
#---General
import argparse
from os.path import isfile, isdir, abspath

#---Project
from src.multithreading import launch_multithreads
from src.hash_crack import algorithms_available


##-Init
version = '1.0.0'

alphabets = {
    '[0-9]': '0123456789',
    '[a-z]': 'abcdefghijklmnopqrstuvwxyz',
    '[A-Z]': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
    '[a-z0-9]': 'abcdefghijklmnopqrstuvwxyz0123456789',
    '[a-zA-Z]': 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
    '[a-zA-Z0-9]': 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
}

##-Types
def hash_algo(h: str) -> str:
    '''
    Raises an argument parser type error if 'h' is not a hash function name.

    - h : the hash function name to test.
    '''

    if h not in algorithms_available:
        raise argparse.ArgumentTypeError(f'"{h}" is not available as a hash')

    return h

def positive_int(n: int) -> int:
    '''If n <= 0, raises an argument type error.'''

    try:
        n = int(n)
    except ValueError:
        raise argparse.ArgumentTypeError(f'the number of threads should be a number ("{type(n)}" found) !')

    if n <= 0:
        raise argparse.ArgumentTypeError(f'the number of threads should be positive ({n} found) !')
    
    return n

##-Ui parser
class ParserUi:
    '''Defines an argument parser'''

    def __init__(self):
        '''Initiate Parser'''

        #------Main parser
        #---Init
        examples = 'Examples :'
        examples += '\n\t./main.py [hash]'
        examples += '\n\t./main.py -a 0123456789 [hash]'
        examples += '\n\t./main.py -a 0123456789 -A sha256 [hash]'
        examples += '\n\t./main.py -t 12 [hash]'

        self.parser = argparse.ArgumentParser(
            prog='HashCracker',
            description='Multithreaded hash cracker',
            epilog=examples,
            formatter_class=argparse.RawDescriptionHelpFormatter
        )

        #---Add arguments
        self.parser.add_argument(
            '-V', '--version',
            help='show version and exit',
            nargs=0,
            action=self.Version
        )
        self.parser.add_argument(
            '-s', '--silent',
            action='store_true',
            help='only print the password and nothing else'
        )

        self.parser.add_argument(
            '-A', '--algorithm',
            default='md5',
            type=hash_algo,
            help='the hash algorithm. Defaults to "md5".'
        )
        self.parser.add_argument(
            '-a', '--alphabet',
            default='[a-z]',
            help='the alphabet to use. Can be [0-9], [a-z], [a-z0-9], [a-zA-Z], [a-zA-Z0-9], or directly the raw alphabet'
        )

        self.parser.add_argument(
            '-t', '--nb-threads',
            type=positive_int,
            help='Specify the number of threads to use. If not set, it gets the number of thread available on the current machine'
        )
        self.parser.add_argument(
            '-l', '--limit',
            type=int,
            help='If used, limit the length of words to LIMIT'
        )

        self.parser.add_argument(
            'hash',
            help='the hash to crack'
        )

    def parse(self):
        '''Parse the args'''

        #---Get arguments
        args = self.parser.parse_args()

        alf = args.alphabet
        if alf in alphabets:
            alf = alphabets[alf]

        launch_multithreads(args.hash, alf, args.algorithm, args.limit, verbose=(not args.silent), nb_threads=args.nb_threads)


    class Version(argparse.Action):
        '''Class used to show version.'''

        def __call__(self, parser, namespace, values, option_string):

            print(f'Hash crack v{version}')
            parser.exit()

