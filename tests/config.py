import json

def read_config(key):
  with open('config.json') as json_file:
    config = json.load(json_file)
    return(config[key])