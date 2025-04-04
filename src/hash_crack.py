#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#--------------------------------
#
# Author            : Lasercata
# Last modification : 2025.04.02
# Version           : v1.0.0
#
#--------------------------------

'''File defining the brute force operations'''

##-Imports
from hashlib import *

##-Word generator
class BruteForceGen:
    '''Defines a generator to brute force words'''

    def __init__(self, alf: str | list[str]):
        '''
        Initiates the class.

        - alf : the alphabet to use.

        '''

        self.alf = alf
        self.N = len(alf)

    def _convert_to_base(self, n: int) -> list[int]:
        '''
        Converts `n` from base 10 to base `self.N` :

            n = sum_{k = 0}^p a_k N^k

        - n : the number to convert.

        Return the list [a_0, a_1, ..., a_p]
        '''

        if n == 0:
            return [0]
    
        ret = []
        while n > 0:
            ret.append(n % self.N)
            n //= self.N

        return ret

    def get_word(self, n: int) -> str:
        '''
        Return the word number `n`.

        It converts `n` to base `self.N`.

        E.g :
            0 -> a
            1 -> b
            ...
            25 -> z
            26 -> ba
            27 -> bb
            28 -> bc
            ...

        Note that 'aa', 'aaa', ... are missing (because they correspond to 00, 000, ... = 0).

        - n : the index of the word.
        '''
    
        digits = self._convert_to_base(n)[::-1]

        return ''.join(self.alf[k] for k in digits)

##-Hash
def hasher(txt: str, h: str) -> str:
    '''
    Calculates the hash of `txt`, using the algorithm `h`.

    - txt : the text to hash ;
    - h   : the name of the algorithm (function name).
    '''

    h_str = tuple(algorithms_available)

    if h in h_str:
        try:
            ret = eval(h_str[h_str.index(h)])(txt.encode()).hexdigest()

        except:
            ret = new(h_str[h_str.index(h)], txt.encode()).hexdigest()

    else:
        raise ValueError(f'The hash function "{h}" was not found !')

    return ret

def test_word(word: str, expected: str, h: str = 'md5') -> bool:
    '''
    Tests if `h(word)` is `expected`.

    - word     : the clear word to test ;
    - expected : the expected hash digest ;
    - h        : the hash algorithm name.
    '''

    return hasher(word, h) == expected


##-Test
if __name__ == '__main__':
    alf = 'abcdefghijklmnopqrstuvwxyz'

    G = BruteForceGen(alf)

    for k in (0, 1, 2, 24, 25, 26, 27):
        print(k, G.get_word(k))

    # for k in range(1000):
    #     print(k, G.get_word(k))

    print(hasher('test', 'md5'))
    print(hasher('tests', 'md5'))
    print(hasher('aaaaa', 'md5'))
