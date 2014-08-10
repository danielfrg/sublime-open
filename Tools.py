from collections import namedtuple
from os.path import abspath, expanduser, join

def unexpanduser(path):
    # FIXME: What about ~user? What about anchor?
    path = abspath(expanduser(path))
    user_home = join('~', '')
    user_path = join(abspath(expanduser(user_home)), '')
    return path.replace(user_path, user_home)

# inspired by: http://stackoverflow.com/a/6849299
class lazy:

    def __init__(self, fget):
        self.fget = fget

    def __get__(self, obj, cls):
        if obj is None:
            return self
        value = self.fget(obj)
        setattr(obj, self.fget.__name__, value)
        return value

# from asyncio import Future # requires Python 3.4
# from concurrent.futures import Future # requires bundled multiprocessing
# inspired by: https://github.com/tornadoweb/tornado/blob/v4.0.0/tornado/concurrent.py#L43
class Future:
    __Done = namedtuple('__Done', 'result exception')

    def __init__(self, executor=None):
        self.__done = None
        self.__callbacks = []
        if executor:
            executor(self.set_result, self.set_exception)

    def running(self):
        return not self.__done

    def done(self):
        return self.running()

    def result(self):
        if self.__check_done().exception is not None:
            raise self.__done.exception
        return self.__done.result

    def exception(self):
        return self.__check_done().__exception

    def add_done_callback(self, on_done):
        if self.__done:
            on_done(self)
        else:
            self.__callbacks += [on_done]

    # inspired by: Promises/A+ API without chaining
    def then(self, on_resolved=None, on_rejected=None):
        resolved = lambda: on_resolved and on_resolved(self.__done.result)
        rejected = lambda: on_rejected and on_rejected(self.__done.exception)
        self.add_done_callback(lambda x: rejected() if self.__done.exception else resolved())

    def catch(self, on_rejected=None):
        self.then(on_rejected=on_rejected)

    def set_result(self, result=None):
        self.__set_done(result)

    def set_exception(self, reason=None):
        if not isinstance(reason, BaseException):
            reason = Exception(reason or "DummyFuture unspecified reason")
        self.__set_done(exception=reason)

    def __check_done(self):
        if not self.__done:
            raise Exception("DummyFuture does not support blocking for results")
        return self.__done

    def __set_done(self, result=None, exception=None):
        if self.__done:
            raise Exception("DummyFuture already done")
        self.__done = self.__Done(result, exception)
        for cb in self.__callbacks:
            # XXX: no error handling
            cb(self)
        self.__callbacks = None
