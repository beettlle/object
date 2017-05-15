import glob
import os
import re
import socket
import time

import tornado.ioloop
import tornado.gen
import tornado.httpserver
import tornado.httpclient
import tornado.options
import tornado.web

import motor.motor_tornado
import bson.json_util

##
# Import project files
##

import app.handlers

##
# Function definitions
##

def almost_apache_style_log(handler):
    '''without status code and body length'''
    req = handler.request
    print '%s - - [%s +0800] "%s %s %s" - - "%s" "%s"' % (req.remote_ip, time.strftime("%d/%b/%Y:%X"), req.method, req.uri, req.version, getattr(req, 'referer', '-'), req.headers['User-Agent'])

##
# Main Process
##

if __name__ == "__main__":

    root = os.path.dirname(__file__)

    settings = {
	"static_path" : os.path.join(root, 'static'),
	"template_path" : os.path.join(root, 'templates'),
	"cookie_secret": "6c54837d36e5f5fbc8c314b9612f6e31",
	"xsrf_cookies": True,
	"gzip" : True,
	"log_function": almost_apache_style_log,
	"objects" : [],
	"debug" : True,
    }

    settings['objects'] = map(lambda x : x.split('.')[0].split('/')[2], glob.glob(settings['static_path'] + "/json/*.json"))

    application = tornado.web.Application([
    (r"/favicon.ico", tornado.web.StaticFileHandler, dict(path=settings['static_path'])),
    (r"/", app.handlers.templateHandler.IndexHandler),
	(r"/\w+/form.html", app.handlers.templateHandler.FormHandler),
	(r"/\w+/list.html", app.handlers.templateHandler.ListHandler),
	(r"/\w+/save", app.handlers.object.SaveHandler),
	(r"/\w+/delete", app.handlers.object.DeleteHandler),
	(r"/\w+/get", app.handlers.object.GetHandler),
	(r"/\w+/getAll", app.handlers.object.GetAllHandler),
    ],
    **settings)

#    tornado.options.options['log_file_prefix'].set('/var/log/tornado/access_log.log')
    tornado.options.parse_command_line()

# backlog = `cat /proc/sys/net/core/somaxconn`
# increase /proc/sys/net/ipv4/tcp_max_syn_backlog
    server = tornado.httpserver.HTTPServer(application)
    server.bind(8888, family=socket.AF_INET, backlog=1024)
    server.start(1)

#    db = motor.motor_tornado.MotorClient('mongodb://test_user:test_password@ds041387.mlab.com:41387/testing').testing
    db = motor.motor_tornado.MotorClient('mongodb://localhost:27017').objectdb
    application.settings['db'] = db

    tornado.ioloop.IOLoop.instance().start()
