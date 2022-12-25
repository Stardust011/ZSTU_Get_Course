import yaml
import os

def load_config(yaml_name):
    with open(yaml_name+'.yaml', 'r') as f:
        config = yaml.safe_load(f)
    return config