import yaml

CONFIG_FILE = 'moneytransfer.yml'

# Returns the parsed configuration as a dictionary.  PyYAML makes deserializing into objects
# a pain, so we just use a dictionary for this test.
def parseConfig():
  with open(CONFIG_FILE) as f:
    return yaml.safe_load(f)
