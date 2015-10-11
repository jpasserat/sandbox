


def decorator_level0(decorated_func):
    """ Decorator does not take any arguments.
    """
    print "decorator_level0: the decorated func %r" % (decorated_func,)
    return decorated_func

def decorator_level0_plus(decorated_func):
    """ Decorator does not take any arguments.
    We access the arguments of the decorated function.
    """
    print "decorator_level0_plus: the decorated func %r" % (decorated_func,)
    def wrapper(*largs, **lkwargs):
        print "decorated_level0_plus: the decorated func's args %r %r" % (largs, lkwargs)
        res = decorated_func(*largs, **lkwargs)
        return res
    return wrapper

def decorator_level1(*args, **kwargs):
    """ Decorator does take arguments.
    """
    print "decorator_level1: the decorator's args %r %r" % (args, kwargs,)
    def decorated(decorated_func):
        print "decorator_level1: the decorated func %r" % (decorated_func,)
        return decorated_func
    return decorated

def decorator_level1_plus(*args, **kwargs):
    """ Decorator does take arguments.
    We access the arguments of the decorated function.
    """
    print "decorator_level1_plus: the decorator's args %r %r" % (args, kwargs,)
    def decorated(decorated_func):
        print "decorator_level1_plus: the decorated func %r" % (decorated_func,)
        def wrapper(*largs, **lkwargs):
            print "decorator_level1_plus: the decorated func's args %r %r" % (largs, lkwargs)
            res = decorated_func(*largs, **lkwargs)
            return res
        return wrapper
    return decorated

def decorator_level1_tricky(func=None, **kwargs):
    """ Decorator takes arguments or not.
    We access the arguments of the decorated function.
    """
    print "decorator_level1_tricky: the decorator's args %s %r" % (func, kwargs,)
    def decorated(decorated_func):
        print "decorator_level1_tricky: the decorated func %r" % (decorated_func,)
        def wrapper(*largs, **lkwargs):
            print "decorator_level1_tricky: the decorated func's args %r %r" % (largs, lkwargs)
            res = decorated_func(*largs, **lkwargs)
            return res
        return wrapper
    if func is None:
        return decorated
    else:
        return decorated(func)


def add(x, y):
    z = x + y
    print 'x + y = %s + %s = %s ' % (x, y, z,)

@decorator_level0
def hello_world_00(x, y):
    add(x, y)

@decorator_level0_plus
def hello_world_01(x, y):
    add(x, y)

@decorator_level1('/', methods=['a', 'b'])
def hello_world_10(x, y):
    add(x, y)

@decorator_level1()
def hello_world_11(x, y):
    add(x, y)

@decorator_level1_plus('/', methods=['a', 'b'])
def hello_world_12(x, y):
    add(x, y)

@decorator_level1_plus()
def hello_world_13(x, y):
    add(x, y)

@decorator_level1_tricky(uri='/', methods=['a', 'b'])
def hello_world_20(x, y):
    add(x, y)

@decorator_level1_tricky
def hello_world_21(x, y):
    add(x, y)


def parametrize(argnames, argvalues):
    argnames = argnames.split(",")
    for param_index, valset in enumerate(argvalues):
        assert len(valset) == len(argnames)
    def decorated(func):
        def wrapper(*args, **kwargs):
            res = []
            for valset in argvalues:
                kwargs.update(dict(zip(argnames, valset)))
                res.append(func(*args, **kwargs))
            return res
        return wrapper
    return decorated

@parametrize("y,z",[
    ("3", 8),
    ("2", 6),
    ("6", 42),
]) 
def hello_world_param(x, y, z):
    print 'Hello World! %r ' % (list((x, y, z,)),)

if __name__ == '__main__':
    hello_world_00(1, 2)
    hello_world_01(3, 4)
    hello_world_10(5, 6)
    hello_world_11(7, 8)
    hello_world_12(9, 10)
    hello_world_13(11, 12)
    hello_world_20(13, 14)
    hello_world_21(15, 16)

    #res = the_decorator_1("jean")(int)('3')
    #print type(res), res
