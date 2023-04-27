import os
import yaml
ini_path = os.path.join(os.getcwd(),'config','config.yml')

def load_config():
    with open(ini_path, 'r') as file:
        cfg = yaml.safe_load(file)
    return cfg['main']