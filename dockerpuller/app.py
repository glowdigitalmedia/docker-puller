from flask import Flask
from flask import request
import json

app = Flask(__name__)
config = None

@app.route('/', methods=['POST'])
def hook_listen():
    if request.method == 'POST':
        token = request.args.get('token')
        #import ipdb; ipdb.set_trace()
        if token == config['token']:
            hook = request.args.get('hook')
            payload = request.get_json()
            print payload
            print payload['repository']['owner']
            print config
            return "ok", 200
        else:
            return "Invalid token", 400

def load_config():
    with open('config.json') as config_file:    
        return json.load(config_file)

if __name__ == '__main__':
    config = load_config()
    app.run(host=config['host'], port=config['port'])
