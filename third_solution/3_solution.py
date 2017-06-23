#!/usr/bin/python
# -*- coding: utf-8 -*-

import collections, functools
from datetime import datetime, timedelta, time
import ipdb


CACHE_LIFECYCLES = 10
CACHE_TIME_TO_LIVE = timedelta(minutes=5)

class memoCache(object):
    """
    Our 'caching' decorator as a class, implementing the __call__ magic method 
    which does everything under the hood once the decorator is triggered.
    
    Although we are referring to this as 'caching', it leaves a lot to be desired in terms 
    of proper caching mechanism, but it's simpleness, speed and efficiency made it into 
    'Memoization' - common Py pattern,famous for being a standard part of Fibonacci numbers iterative 
    implementation....
    
    Preserves function call result as a dict((arg1, arg2): res), and then just retrieves the result by key[args], but 
    doesn't evaluate the result, that is done only once, on initial call per key.
    Every subsequent call with same args uses the same evaluated value.
    Pretty cheap solution for expensive work loads.
    
    https://wiki.python.org/moin/PythonDecoratorLibrary#Memoize
    http://code.activestate.com/recipes/325905/
    http://code.activestate.com/recipes/496879/

    
    """

    instances = {}
    ttl_timeouts = {}

    def __init__(self, func):
        self.func = func
        self.cache = {}
        self.call_counter = 0
        self.init_call_timer = None


    def __call__(self, *args):

        self.call_counter += 1


        # if not isinstance(args, collections.Hashable):
        #     return self.func(*args)
        #
        # def _cache_valid():
        #     if self.init_call_timer:
        #         ipdb.set_trace()
        #         return datetime.now() - self.init_call_timer < self.max_lifespan \
        #                or self.call_counter in range(1, self.max_lifecycles)
        #
        # if args in self.cached:
        #     ipdb.set_trace()
        #     if _cache_valid():
        #         self.call_counter += 1
        #         print 'iz kesha->'
        #         return self.cached[args]
        #     else:
        #         self.cached[args] = {}
        #         print 'muerto kesh->'
        #         return self.func(*args)
        #
        # else:
        #     ipdb.set_trace()
        #     res = self.func(*args)
        #     self.cached[args] = res
        #     self.init_call_timer = datetime.now()
        #     self.call_counter += 1
        #     print 'tek unilazi'
        #     return res
        try:
            return self.cache[args]
        except KeyError:
            value = self.func(*args)
            self.cache[args] = value
            return value
        except TypeError:
            return self.func(*args)

    def __get__(self, obj, objtype):
        '''Support instance methods.'''
        return functools.partial(self.__call__, obj)

    @staticmethod
    def count(f):
        "Return exec count of specific instance"
        return memoCache.instances[f].call_counter


if __name__ == '__main__':

    @memoCache
    def simplesum(a, b):
        return a + b

    print simplesum(5,5)
    print simplesum(6,4)
    print simplesum(5,5)
    print simplesum(6,4)
    print simplesum(7,7)
    print simplesum(97,7)
    print simplesum(7,7)
    print simplesum(97,7)






