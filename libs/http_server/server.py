import os
import json
from flask import Flask
from flask import render_template


class http_server:
  def __init__(self, name="pf_http",  log=None, debug=False):
    static_folder = os.path.join(os.path.dirname(__file__), "ui/static")
    template_folder = os.path.join(os.path.dirname(__file__), "ui/templates")
    self.debug=debug
    self.app = Flask(import_name=name, static_folder=static_folder , template_folder=template_folder)

    @self.app.route("/")
    def main():
      return render_template('./main_tmpl.html')

    @self.app.route("/genre")
    def genre():
      return render_template('./genre_list_tmpl.html')

    @self.app.route("/genre_list")
    def genre_list():
      with open (os.path.join(os.path.dirname(__file__), "../../dbs/genre_test.json")) as f:
        jsonStr = json.load(f)
        return json.dumps(jsonStr)



    @self.app.route("/act")
    def act():
      return render_template('./act_list_tmpl.html')


    @self.app.route("/hello_world")
    def hello_world():
      return "Hello World"


  def run(self):
    self.app.run(debug=self.debug)
    
