import tornado
import tornado.httpclient
from tornado import gen

import motor
import bson.json_util

from baseHandler import BaseHandler

class IndexHandler(BaseHandler):
    """HTTP Handler to serve index page"""
    def get(self, page=None):
        self.render("index.html", objects=self.application.settings['objects'] )

class FormHandler(BaseHandler):
    """HTTP Handler to serve form page"""
    def get(self, page=None):
        urlSplit = self.request.path.split('/')
        if urlSplit[2] == 'form.html' :
                if self.get_argument("id", None) :
                        id = self.get_argument("id", None)
                        bottle = id
                else :
                        bottle = 0
                self.render("form.html", objects=self.application.settings['objects'], id=bottle, type=urlSplit[1])
        else :
                raise tornado.web.HTTPError(404, "File not found")

class ListHandler(BaseHandler):

    """HTTP Handler to serve the list page"""
    @gen.coroutine
    def get(self, page=None):
        urlSplit = self.request.path.split('/')
        if urlSplit[2] == 'list.html' :
                http_client = tornado.httpclient.AsyncHTTPClient()
                staticUrl = self.static_url("json/" + urlSplit[1] + ".json")
                jsonUrl = "http://localhost:8888" + staticUrl
                response = yield http_client.fetch(jsonUrl, method="GET", user_agent="Object")
                self.webRequest(response)
        else :
                raise tornado.web.HTTPError(404, "File not found")

    def webRequest(self, response) :
        if response.error :
                raise tornado.web.HTTPError(500, "Internal Server Error")
        else :
                webObject = tornado.escape.json_decode(response.body)
                urlSplit = self.request.path.split('/')
                userObject = webObject['html']
                categories = []
                values = []
                for o in userObject :
                        if ("caption" in o) and ("validate" in o) and ("required" in o["validate"]) :
                                if o['type'] != "hidden" :
                                        categories.append(o['caption'])
                                        mData = tornado.escape.native_str(o['name'])
                                        values.append({'mData' : mData, "sDefaultContent" : "-" })

                self.render("list.html", objects=self.application.settings['objects'], type=urlSplit[1], titles=categories, classes=values)
