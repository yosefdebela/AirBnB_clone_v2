# fabric_test4.py
from fabric import task, Config
import yaml

# Load YAML config manually
with open('fabric.yaml') as f:
    config_dict = yaml.safe_load(f)

config = Config(overrides=config_dict)

@task
def create(c):
    c.local('pwd')
    c.local('mkdir yosef')