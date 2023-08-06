from notebook.utils import url_path_join
from notebook.base.handlers import IPythonHandler
import os
from tornado.web import StaticFileHandler
import mimetypes
import inspect

class HelloWorldHandler(IPythonHandler):
    def get(self):
        self.finish("Hello, Jupyter!")

class FileHandler(StaticFileHandler):
    def get_content_type(self):
        mime_type, encoding = mimetypes.guess_type(self.absolute_path)
        return mime_type or "application/octet-stream"
    

def load_jupyter_server_extension(nb_app):
    web_app = nb_app.web_app
    host_pattern = '.*$'
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Handler for /roboweb-server-extension/<file>
    web_path = os.path.join(base_dir, "static")
    web_route = url_path_join(web_app.settings["base_url"], "roboweb-server-extension/(.*)")
    web_app.add_handlers(host_pattern, [(web_route, FileHandler, {"path": web_path})])  

def _jupyter_server_extension_paths():
    print("Returning module")
    return [{"module": "roboweb_server.ext"}]
