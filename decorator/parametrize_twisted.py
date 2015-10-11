from twisted.internet import reactor, defer
from twisted.python.util import println


def parametrize(argnames, argvalues):
    argnames = argnames.split(",")
    for param_index, valset in enumerate(argvalues):
        assert len(valset) == len(argnames)
    def decorated(func):
        def wrapper(*args, **kwargs):
            dl = []
            for valset in argvalues:
                kwargs.update(dict(zip(argnames, valset)))
                dl.append(defer.maybeDeferred(func, *args, **kwargs))
            return defer.gatherResults(dl)
        return wrapper
    return decorated

@parametrize("input,expected",[
    ("3+5", 8),
    ("2*3", 6),
    ("6*9", 54),
]) 
def test_eval(input, expected):
    print 'input %r expected %r ' % (input, expected,)
    if eval(input) == expected:
        return True
    else:
        raise ValueError("input %r <> expected %r" % (input, expected,))

if __name__ == '__main__':
    d = test_eval()
    d.addBoth(println)
    reactor.run()
