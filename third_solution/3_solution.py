#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
THIRD PROBLEM

Two ways of implementing cached-like behavior for subsequent function calls, both based on 'Memoize' pattern
    https://wiki.python.org/moin/PythonDecoratorLibrary#Memoize


@author: Ismar Sehic, <https://github.com/sheha>

June, 2017

"""

import collections, functools, time, ipdb
from datetime import datetime, timedelta

CACHE_LIFECYCLE = 10
CACHE_TIME_TO_LIVE = timedelta(minutes=1)


class MemoCache(object):
    """
    CLASS BASED FUNCTION CACHING DECORATOR
    Implementing the __call__ magic method which does everything under the hood once the decorator is applied to a 
    function.
            
    Preserves function call meta as a dict((args): result, init_timestamp, passcount), and subsequently retrieves 
    the result by key[args], but doesn't evaluate the result except only once, on initial call per key.
    
    Can be expanded in various ways, i.e. by adding persistence of some kind, perhaps Mongo or Couch non-RDBMS DB...
    This class simply keeps a dictionary with args as key in memory while the function is running.
        
    Does not support caching for functions taking mutable arguments, can be implemented with cPickle module.
                          
    """

    def __init__(self, func):
        self.func = func
        self.cached = {}

        self.passcount = 0

        self.ttl = CACHE_TIME_TO_LIVE
        self.lifecycle = CACHE_LIFECYCLE

    def __call__(self, *args):
        self.passcount += 1

        if not isinstance(args, collections.Hashable):
            print '> Only hashable args supported! Skipping caching, regular evaluation ...'
            return self.func(*args)

        if args in self.cached and self.validate(args):

                print '> Key found. Returning from cached...'
                self.cached[args]['count'] = self.passcount
                print '> pass: {}, result: {}'.format(self.passcount, self.cached[args]['result'])
                return self.cached[args]['result']

        else:
            print '> Key not found or expired. Init cache...'
            del self.cached[args]
            self.cached[args] = {'result': self.func(*args), 'timestamp': datetime.now(), 'count': self.passcount}
            print 'pass: {}, result: {}'.format(self.cached[args]['count'], self.cached[args]['result'])
            return self.cached[args]['result']

    def __get__(self, obj, objtype):
        """ Instance methods """
        return functools.partial(self.__call__, obj)

    def __repr__(self):
        return self.func.__doc__

    def validate(self, args):
        """ Makes sure that the cached is valid for 5 minutes or 10 subsequent calls """
        young = (datetime.now() - self.cached[args]['timestamp']) < self.ttl
        fresh = self.cached[args]['count'] in range(0, self.lifecycle)
        return True if young and fresh else False


class LazyMemoCache(object):
    """
    LAZY LOADING FUNCTION CACHING DECORATOR
    Enables a dictionary property to be lazy-loaded, in a similar fashion to lazy_property.
    
    Exceptions raised by the decorated function will be wrapped as KeyErrors and raised.
    """

    def __init__(self, func):
        self.orig_func = func
        self.func = func
        self.cached = {}
        self.passcount = 0

        self.ttl = CACHE_TIME_TO_LIVE
        self.lifecycle = CACHE_LIFECYCLE

    def __get__(self, obj, objtype):
        self.func = functools.partial(self.orig_func, obj)
        return self

    def __getitem__(self, *key):
        try:
            return self.cached[key]
        except KeyError:  # Value not loaded yet
            try:
                value = self.func(*key)
            except TypeError:
                print '> Only hashable args supported! Skipping caching, regular evaluation ...'
            self.cached[key] = value
            return value

    def __setitem__(self, value, *key):
        """
        Set is provided for convenience, it should be avoided - this
        dict is backed by a function, breaking that contract isn't advisable.
        """
        self.cached[key] = value

    def __delitem__(self, *key):
        """Clears the given value, re-accessing it recalls the function"""
        del self.cached[key]

    def __iter__(self):
        raise NotImplementedError("Unable to iter over lazy-loaded dictionary")

    def __contains__(self):
        raise NotImplementedError("Unable to do contains checks on lazy-loaded dictionary")

    def validate(self, args):
        """ Makes sure that the cached is valid for 5 minutes or 10 subsequent calls """
        young = (datetime.now() - self.cached[args]['timestamp']) < self.ttl
        fresh = self.cached[args]['count'] in range(0, self.lifecycle)
        return True if young and fresh else False


def main():
    @MemoCache
    def simplesum(a, b):
        return a + b

    def test_simplesum(a, b, x, t):
        for i in xrange(x):
            time.sleep(t)
            print simplesum(a, b)

    test_simplesum(5, 5, 12, 100)

    # test_simplesum(4, 4, 7, 100)


    @MemoCache
    def fibonacci(n):
        if n > 1:
            return fibonacci(n - 1) + fibonacci(n - 2)
        else:
            return n

    print fibonacci(10)


if __name__ == '__main__':
    main()
