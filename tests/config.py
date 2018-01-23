import json

def key(key):
  with open('config.json') as json_file:
    config = json.load(json_file)
    return(config[key])