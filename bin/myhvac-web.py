from myhvac_web import app
from myhvac_web.main import *

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop


def start():
    LOG.info('Starting web server...')
    LOG.debug('Enable flask debug: %s', CONF.rest_api.debug)
    LOG.debug('Enable port: %s', CONF.rest_api.port)
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(CONF.rest_api.port)
    IOLoop.instance().start()


def stop():
    LOG.info('Stopping web server...')
    IOLoop.instance().stop()

if __name__ == '__main__':
    init()
    start()
