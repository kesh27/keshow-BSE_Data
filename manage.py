import cherrypy
import os, os.path
import redis
import settings
import json

class EquityResults(object):
    @cherrypy.expose
    def index(self):
        return open('index.html')

@cherrypy.expose
class EquityResultsWebService(object):

    def __init__(self):  
        self.redis_con = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB_ID, password=settings.REDIS_PASSWORD)
    
    def GET(self, equity_name = None):
        results = []
        equities_list = self.redis_con.get("top_ten_equity")
        equities_list = json.loads(equities_list)
        if equity_name:
            equity_name += "*"
            equities_list = self.redis_con.keys(equity_name)     
        for equity in equities_list:
            result = {"name": equity, "equity_mini": self.redis_con.get(equity)}
            results.append(result)
        response = json.dumps({"last_updated_on": self.redis_con.get("last_updated_on"), "results_mini": results})
        return response

if __name__ == '__main__':
    conf = {
        '/': {
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/generator': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher()
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }

    cherrypy.config.update({'server.socket_host': '0.0.0.0',
                            'server.socket_port': settings.APP_PORT})

    webapp = EquityResults()
    webapp.generator = EquityResultsWebService()
    cherrypy.quickstart(webapp, '/', conf)