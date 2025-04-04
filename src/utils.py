#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#--------------------------------
#
# Author            : Lasercata
# Last modification : 2025.04.03
# Version           : v1.0.0
#
#--------------------------------

'''File defining misc functions'''

##-Functions
def boxed_print(s: str):
    '''
    Prints `s` in a box, e.g:

        +------+
        | test |
        +------+
    '''

    print('+' + '-'*(len(s) + 2) + '+')
    print(f'| {s} |')
    print('+' + '-'*(len(s) + 2) + '+')
