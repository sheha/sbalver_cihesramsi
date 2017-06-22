#!/usr/bin/python
# -*- coding: utf-8 -*-
import collections, functools
from datetime import datetime, timedelta
import ipdb


class FnCache(object):

    def __init__(self, func):
        self.func = func
        self.cached = {}
        self.callcounter = 0
        self.init_call_timer = None

        self.max_lifecycles = 11
        self.max_lifespan = timedelta(minutes=5)

    def __call__(self, *args):

        if not isinstance(args, collections.Hashable):
            return self.func(*args)

        def _healthy_cache():
            if self.init_call_timer:
                # print self.init_call_timer
                # print self.callcounter
                # print datetime.now() - self.init_call_timer < self.max_lifespan or self.callcounter in range(1, self.max_lifecycles)
                ipdb.set_trace()
                return datetime.now() - self.init_call_timer < self.max_lifespan or self.callcounter in range(1, self.max_lifecycles)

        if args in self.cached:
            ipdb.set_trace()
            if _healthy_cache():
                self.callcounter += 1
                print 'iz kesha->'
                return self.cached[args]
            else:
                self.cached[args] = {}
                print 'muerto kesh->'
                return self.func(*args)

        else:
            ipdb.set_trace()
            res = self.func(*args)
            self.cached[args] = res
            self.init_call_timer = datetime.now()
            self.callcounter += 1
            print 'tek unilazi'
            return res

    def __get__(self, obj, objtype):
        '''Support instance methods.'''
        return functools.partial(self.__call__, obj)


if __name__ == '__main__':

    @FnCache
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






