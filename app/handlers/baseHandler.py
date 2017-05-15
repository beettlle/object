import tornado

class BaseHandler(tornado.web.RequestHandler):

    def get_current_user(self):
        u = self.get_secure_cookie("user")
        if not u:
                return None
        user = tornado.escape.json_decode(u)
        return user['user_id']

    def prepare(self):
	# Leave breadcrumbs so we know where to come back to after authentication
	if not self.current_user and (self.request.path.split('/')[-1] != 'login'):
		pathcrumb = {'url' : self.request.path}
		self.set_secure_cookie("pathcrumb", tornado.escape.json_encode(pathcrumb))
