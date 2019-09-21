import cherrypy
import os, os.path
import redis
from etc import settings
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
        if equity_name:
            equity_mini = REDIS_CON.get(equity_name)
            if equity_mini:
                result = {"name": equity_name, "equity_mini": equity_mini}
                results.append(result)
                response = json.dumps({"last_updated_on": REDIS_CON.get("last_updated_on"), "results_mini": results})
                return response
        top_ten_equities = REDIS_CON.get("top_ten_equity")
        top_ten_equities = json.loads(top_ten_equities)       
        for equity in top_ten_equities:
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