import json
import os

import cherrypy
from jinja2 import Environment, FileSystemLoader

# GET CURRENT DIRECTORY
from helper import get_redis_connection, get_sorted_list
from scrapper import main1

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
env = Environment(loader=FileSystemLoader(CUR_DIR), trim_blocks=True)


class Index(object):
    @cherrypy.expose
    def index(self):
        template = env.get_template('templates/home.html')
        r = get_redis_connection()
        try:
            users = json.loads(r.get('ten_users'))
        except:
            main1()  # If file was not downloaded then download the latest file.
            users = json.loads(r.get('ten_users'))

        return template.render(users=users, name='JAYANTH')


@cherrypy.expose
class UserService(object):
    @cherrypy.tools.json_out()
    def POST(self, name):
        r = get_redis_connection()
        users = json.loads(r.get('users'))
        response = {}
        try:
            res = [user for user in users if name.lower() in user["name"].lower()]  # search by name (substring match)

            result = get_sorted_list(res, 'dict')

            response['success'] = True
            response['users'] = result[:10]
            response['length'] = res.__len__()
            return response
        except:
            response['success'] = False
            return response


if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/get_users': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './static'
        }
    }
    webapp = Index()
    webapp.get_users = UserService()
    cherrypy.server.socket_host = '0.0.0.0'
    cherrypy.quickstart(webapp, '/', conf)
