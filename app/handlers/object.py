import tornado
import tornado.httpclient

import motor
import bson.json_util

from baseHandler import BaseHandler

class SaveHandler(BaseHandler):

    @tornado.web.asynchronous
    def post(self):
        userObject = tornado.escape.json_decode(self.request.body)
        urlSplit = self.request.path.split('/')

        userObject['type'] = urlSplit[1]
#	userObject['user'] = self.current_user
        try :
            del userObject['_xsrf']
        except KeyError :
            pass

        db = self.settings['db']

        if '_id' in userObject :
            # Update the entry
            objectId = bson.objectid.ObjectId(userObject['_id'])
            userObject['_id'] = objectId
            db.objects.update({ '_id' : objectId }, userObject, callback=self._on_update)
        else :
            object = tornado.escape.json_encode(userObject)
            db.objects.insert(bson.json_util.loads( object ), callback=self._on_save)

    def _on_save(self, result, error) :
        if error :
            raise tornado.web.HTTPError(500, error)
        else :
            oid = {'_id' : tornado.escape.json_decode(bson.json_util.dumps(result))['$oid']}
            self.write(oid)
        self.finish()

    def _on_update(self, result, error) :
        if error :
            raise tornado.web.HTTPError(500, error)
        else :
            oid = {'_id' : tornado.escape.json_decode(self.request.body)['_id']}
            self.write(oid)
        self.finish()

class GetHandler(BaseHandler):

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        id = self.get_argument("id", None)
        bsonID = bson.objectid.ObjectId(id)

        urlSplit = self.request.path.split('/')
        type = urlSplit[1]

        document = yield motor.Op(self.settings['db'].objects.find_one, {"_id" : bsonID, "type" : type })

        document['_id'] = id
        self.write(bson.json_util.dumps(document))
        self.finish()

class GetAllHandler(BaseHandler):

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        urlSplit = self.request.path.split('/')
        type = urlSplit[1]

        cursor = self.settings['db'].objects.find( { "type" : type } )

        docList = []
#       for document in (yield motor.Op(cursor.to_list)):
        while (yield cursor.fetch_next):
            document = cursor.next_object()
            document['_id'] = tornado.escape.json_decode(bson.json_util.dumps(document['_id']))['$oid']
            document['DT_RowId'] = document['_id']
            document['DT_RowClass'] = 'clickableRow'
            docList.append(document)
        object = { 'object' : docList }
        self.write(tornado.escape.json_encode(object))
        self.finish()

class DeleteHandler(BaseHandler):


    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        objectID = tornado.escape.json_decode(self.request.body)
        bsonID = bson.objectid.ObjectId(objectID['_id'])

        urlSplit = self.request.path.split('/')
        type = urlSplit[1]

        result = yield motor.Op(self.settings['db'].objects.remove, {"_id" : bsonID, "type" : type })

        self.write(result)
        self.finish()
