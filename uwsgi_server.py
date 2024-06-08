from main import *
import cherrypy, datetime, os, os.path

cherrypy.config.update({'engine.autoreload.on': False})
cherrypy.server.unsubscribe()
cherrypy.engine.start()

wsgiapp = cherrypy.tree.mount(SAE23_Website())
