#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#--------------------------------
#
# Author            : Lasercata
# Last modification : 2025.04.02
# Version           : v1.0.0
#
#--------------------------------

'''File defining the user interface using argparse.'''

##-Imports
#---General
import argparse
from os.path import isfile, isdir, abspath

#---Project
# from src.MeiToGraph import MeiToGraph
# from src.utils import log, basename, write_file


##-Init
version = '0.1.0'


##-Ui parser
class ParserUi:
    '''Defines an argument parser'''

    def __init__(self):
        '''Initiate Parser'''

        #------Main parser
        #---Init
        examples = 'Examples :'
        examples += '\n\tconvert `file.mei`                       : ./main.py file.mei'
        examples += '\n\tconvert all mei files in the mei/ folder : ./main.py mei/*.mei'
        examples += '\n\tconvert all mei files in the sub path    : ./main.py **/*.mei'
        examples += '\n\tconvert all, overwrite, save in cypher/,'
        examples += '\n\t generate .cql, show progression         : ./main.py -nv -q load_all.cql -o cypher/ **/*.mei'

        self.parser = argparse.ArgumentParser(
            prog='Musypher',
            description='Compiles fuzzy queries to cypher queries',
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
            '-v', '--verbose',
            action='store_true',
            help='print logs when a file is converted'
        )

        self.parser.add_argument(
            '-n', '--no-confirmation',
            action='store_true',
            help='Do not ask for confirmation before overwriting a file'
        )

        self.parser.add_argument(
            '-o', '--output-folder',
            type=folder_arg,
            help='save all dumps in the given folder'
        )

        self.parser.add_argument(
            '-q', '--cql',
            help='If enabled, also create the .cql file (that is useful to load all the generated .cypher in the database)'
        )

        # self.parser.add_argument(
        #     '-U', '--URI',
        #     default='bolt://localhost:7687',
        #     help='the uri to the neo4j database'
        # )
        # self.parser.add_argument(
        #     '-u', '--user',
        #     default='neo4j',
        #     help='the username to access the database'
        # )
        # self.parser.add_argument(
        #     '-p', '--password',
        #     default='12345678',
        #     help='the password to access the database'
        # )

        self.parser.add_argument(
            'files',
            nargs='+',
            help='the MEI files to convert. For each file, it adds "_dump.cypher" to the basename of the file.'
        )

    def parse(self):
        '''Parse the args'''

        #---Get arguments
        args = self.parser.parse_args()

        dump_files = []

        for k, f in enumerate(args.files):
            if not isfile(f):
                log('warn', f'"{f}" is not a file !')

            else:
                dump_fn = make_dump_fn(f, args.output_folder)

                if args.verbose:
                    log('info', f'Converting file "{f}" to "{dump_fn}" ...')

                converter = MeiToGraph(f, args.verbose)
                res = converter.to_file(dump_fn, args.no_confirmation)

                if res:
                    log('info', f'File "{f}" has been converted to cypher in file "{dump_fn}" ! {round((k + 1) / len(args.files) * 100)}% done !')
                    dump_files.append(dump_fn)

                else:
                    log('info', f'Conversion for the file "{f}" has been canceled ! {round((k + 1) / len(args.files) * 100)}% done !')
        
        if args.cql != None:
            if len(dump_files) == 0:
                log('warn', f'Generation of {args.cql} canceled as no file was generated !')
                return

            self._make_cql_file(dump_files, args.cql, args.no_confirmation, args.verbose)


    class Version(argparse.Action):
        '''Class used to show version.'''

        def __call__(self, parser, namespace, values, option_string):

            print(f'Hash crack v{version}')
            parser.exit()

