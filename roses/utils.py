import os
import json

# TODO make this thing awesome

def read_json_file(filename):
  """
  File name regarding to roses folder.
  """
  base_path = os.path.dirname(os.path.abspath(__file__))
  path = "".join([base_path, "/", filename])
  with open(path) as f:
    content = json.loads(f.read())
  return content