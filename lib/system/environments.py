import os
import yaml

class ConfigEnvs:
  def __init__(self):
    main_path     = os.path.abspath(os.path.dirname(__name__))
    load_env_file = open(f'{main_path}/config.yml', 'r').read()
    load_env_data = yaml.safe_load(load_env_file)
    for group in load_env_data:
      for env in load_env_data[group]:
        value = load_env_data[group][env]
        os.environ[env] = str(value)