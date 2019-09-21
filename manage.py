import cherrypy
import os, os.path
import redis
import settings
import json

REDIS_CON = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB_ID)

class EquityResults(object):
    @cherrypy.expose
    def index(self):
        return open('index.html')

@cherrypy.expose
class EquityResultsWebService(object):
    def GET(self, equity_name = None):
        results = []
        equities_list = REDIS_CON.get("top_ten_equity")
        equities_list = json.loads(equities_list)
        if equity_name:
            equity_name += "*"
            equities_list = REDIS_CON.keys(equity_name)     
        for equity in equities_list:
            result = {"name": equity, "equity_mini": REDIS_CON.get(equity)}
            results.append(result)
        response = json.dumps({"last_updated_on": REDIS_CON.get("last_updated_on"), "results_mini": results})
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

    webapp = EquityResults()
    webapp.generator = EquityResultsWebService()
    cherrypy.quickstart(webapp, '/', conf)