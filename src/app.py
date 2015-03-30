from flask import Flask, session, jsonify, request, g, send_from_directory

from flask.ext.cache import Cache
from flask.ext.cors import CORS, cross_origin

from models import UrlInfo
import controller

import DatabaseSettings

app = Flask(__name__)
cache = Cache(app,config={'CACHE_TYPE': 'simple'})

# Turn on debugging
app.debug = True

@app.route('/')
def home():
    return send_from_directory('html', 'index.html')

@app.route('/<path:path>')
def other_html(path):
    return send_from_directory('html', path)

@app.route('/info/<url>')
def info(url):
  return url

@app.route('/api/<url>')
@cross_origin(origin='*')
@cache.cached(timeout=(5*60))
def api(url):
  return poll_services(url)

@app.route('/api/nocache/<url>')
@cross_origin(origin='*')
def poll_services(url):
  testResponse = UrlInfo()
  testResponse.url = url
  url = url.replace("http://","")
  url = url.replace("www.", "")
  controller.add_if_not_present(url)
  facebookInteractions = {'likes':10, 'shares':4}
  testResponse.interactions['facebook'] = controller.get_facebook(url)
  testResponse.interactions['twitter'] = controller.get_twitter(url)
  testResponse.interactions['google'] = controller.get_google(url)
  out = testResponse.__dict__
  if controller.get_history_num(url) >= 10:
    out['showGraph'] = True
  else:
    out['showGraph'] = False
  return jsonify(out)

@app.route('/api/history/<url>')
def history(url):
  url = url.replace("http://","")
  url = url.replace("www.", "")
  return jsonify(controller.get_history(url))

if __name__ == '__main__':
  app.run(DatabaseSettings.thishostname)
