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
    def GET(self):
        top_ten_equities = REDIS_CON.get("top_ten_equity")
        top_ten_equities = json.loads(top_ten_equities)
        results = []
        for equity in top_ten_equities:
            data = REDIS_CON.get(equity)
            result = {"name": equity, "equity_mini": data}
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