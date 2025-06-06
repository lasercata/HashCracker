#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#--------------------------------
#
# Author            : Lasercata
# Last modification : 2025.04.03
# Version           : v1.0.0
#
#--------------------------------

'''File defining the threading part'''

##-Imports
from multiprocessing import Pool, Manager
from os import sched_getaffinity # to get the number of cores

from datetime import datetime as dt

from src.hash_crack import BruteForceGen, test_word
from src.utils import boxed_print


##-Global
# pool = None


##-Threading
def get_nb_available_threads():
    '''Returns the number of available threads'''

    return len(sched_getaffinity(0))

def found(i, n, word, t0, stop_event, verbose):
    '''Defines what to do when the password is found'''

    if verbose:
        print(f'\nThread {i}/{n}: Found in {dt.now() - t0}s !')
        boxed_print(word)

    else:
        print(word)

    # Stop all the threads :
    stop_event.set()


def thread_i(i: int, n: int, alf: str, expected: str, hash_func: str, stop_event, min_: int = 0, limit: int | None = None, verbose: bool = False):
    '''
    Code run by the thread #i.

    - i          : the id of the current thread (in [|0 ; n - 1|]) ;
    - n          : the number of threads launched ;
    - alf        : the alphabet ;
    - expected   : the hash to crack ;
    - hash_func  : the name of the hash function to use ;
    - stop_event : the Manager.Event that is set when password is found to stop all the processes ;
    - min_       : the minimum length of the words to try ;
    - limit      : the maximum length of the words to try. If None, there is no limit ;
    - verbose    : indicate if being verbose or not ;
    '''

    #---Init
    large_nb = 1000000
    G = BruteForceGen(alf)
    t0 = dt.now()

    if limit is not None:
        mx = G.N ** limit
        cond = lambda x: x < mx

    else:
        cond = lambda x: True

    #---Loop
    word_nb = int(G.N ** (min_ - 1) + i - 1)
    while cond(word_nb):
        word = G.get_word(word_nb)

        if verbose:
            if word_nb % large_nb == 0:
                print(f'Testing word "{word}" (length: {len(word)}, #{word_nb}, {dt.now() - t0}s elapsed)')

        if test_word(word, expected, hash_func):
            found(i, n, word, t0, stop_event, verbose)
            return

        word_nb += n

        # This checks the `stop_event` event in order to stop the current thread if it is set (when password found).
        # stop_event.is_set() is slow, so we check only once every `large_nb`.
        if word_nb % large_nb < n and stop_event.is_set():
            return

def launch_multithreads(hsh: str, alf: str, hash_func: str, min_: int = 0, limit: int | None = None, verbose: bool = True, nb_threads=None):
    '''
    Launch a sample test on multiple threads.

    - hsh        : the hash to crack ;
    - alf        : the alphabet to use to brute force ;
    - hash_func  : the name of the hash function to use ;
    - min_       : the minimum length of the words to try ;
    - limit      : the maximum length of the words to try. If None, there is no limit ;
    - verbose    : indicate if being verbose or not ;
    - nb_threads : the number of threads to use. If None (default), will be set to the number of available cores.
    '''

    #---Number of threads
    if nb_threads == None:
        nb_threads = get_nb_available_threads()

    if verbose:
        print(f'Launching the cracker with {nb_threads} threads ...')

    #---Initialisation of the threads
    mng = Manager()
    stop_event = mng.Event()

    args_lst = [
        (
            k,
            nb_threads,
            alf,
            hsh,
            hash_func,
            stop_event,
            min_,
            limit,
            verbose,
        )
        for k in range(nb_threads)
    ]

    # Starting the threads
    t0 = dt.now()

    try:
        with Pool(nb_threads) as p:
            global pool
            pool = p
            p.starmap(thread_i, args_lst)

    except KeyboardInterrupt:
        print('Stopped.')


    t1 = dt.now()

    #---Print results
    if verbose:
        print(f'{t1 - t0}s elapsed.')



##-Run tests
if __name__ == '__main__':
    hsh_ = 'not a hash' # not a hash
    test = '098f6bcd4621d373cade4e832627b4f6' # md5 of 'test'
    tests = 'b61a6d542f9036550ba9c401c80f00ef' # md5 of 'tests'
    aaaaa = '594f803b380a41396ed63dca39503542' # md5 of 'aaaaa'
    testing = 'ae2b1fca515949e5d54fb22b8ed95575' # md5 of 'testing'

    alf = 'abcdefghijklmnopqrstuvwxyz'

    launch_multithreads(aaaaa, alf, 'md5')
    print()
    launch_multithreads(tests, alf, 'md5')
    # launch_multithreads(hsh_, alf)
    # launch_multithreads(testing, alf)
