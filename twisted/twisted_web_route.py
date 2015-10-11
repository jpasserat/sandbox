import sys

from twisted.python import log
from twisted.web import server, resource
from twisted.internet import reactor


# The idea is to 1 Resource per route and separate code in render_GET (like Flask route decorator maps function)


log.startLogging(sys.stdout)

root = resource.Resource()

class SimpleX(resource.Resource):
    """ Base class for route
    """
    isLeaf = False

    def __init__(self, render_callable):
        resource.Resource.__init__(self)
        self.doRender = render_callable

    def getChild(self, name, request):
        # Only usefull if you want to serve route/ (w/ ending slash)
        # in addition to route (w/o ending slash)
        if name == '':
            return self
        return resource.Resource.getChild(self, name, request)

    def render_GET(self, request):
        log.msg("SimpleX %r %r %s." % (request.prepath, request.postpath, request.args))
        return self.doRender(request)


def route(uri):
    def decorated(func):
        uri_path = [x for x in uri.split('/')
                    if len(x) > 0]
        if len(uri_path) == 0:
            resrc = SimpleX(func)
            root.putChild('', resrc)
        elif len(uri_path) == 1:
            first = uri_path.pop()
            resrc = SimpleX(func)
            root.putChild(first, resrc)
        else:
            father = root
            for u in uri_path[:-1]:
                resrc = resource.NoResource()
                father.putChild(u, resrc)
                father = resrc
            last = uri_path[-1]
            resrc = SimpleX(func)
            father.putChild(last, resrc)
        return func
    return decorated


# Serve http://127.0.0.1:8080/
@route('')
def home(request):
    return "Welcome Home %r %r %s." % (request.prepath, request.postpath, request.args)

# Serve http://127.0.0.1:8080/foo/bar?k=v&k1=v1
# but NOT http://127.0.0.1:8080/foo 
@route('foo/bar')
def foobar(request):
    return "foo/bar %r %r %s." % (request.prepath, request.postpath, request.args)

# Serve http://127.0.0.1:8080/hello/?k=v&k1=v1
@route('hello')
def hello(request):
    timeout = 3
    request.write("hello world %r after %s seconds" % (request.args, timeout))
    d = request.notifyFinish()
    d.addCallback(lambda _: log.msg("finished normally"))
    d.addErrback(log.msg, "error")
    reactor.callLater(timeout, request.finish)
    return server.NOT_DONE_YET

# Any other root will raise an HTTP error 404 NOT_FOUND
	
site = server.Site(root)
reactor.listenTCP(8080, site)
reactor.run()
