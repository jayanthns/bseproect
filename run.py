import os
import cherrypy
from jinja2 import Environment, FileSystemLoader
import json
from scripts.srapper import get_redis_connection

# GET CURRENT DIRECTORY
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
            users = None

        return template.render(users=users, name='JAYANTH')

@cherrypy.expose
class UserService(object):
    @cherrypy.tools.json_out()
    def POST(self, name):
        r = get_redis_connection()
        users = json.loads(r.get('users'))
        response = {}
        try:
            res = [user for user in users if name == user["name"]]
            print res.__len__()

            response['success'] = True
            response['users'] = res
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
    
    cherrypy.config.update({
        'server.socket_host': '13.127.129.1',
        'server.socket_port': 80,
    })
    cherrypy.quickstart(webapp, '/', conf)