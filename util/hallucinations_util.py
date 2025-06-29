import json

hallucinations = []
#collect hallucinations
with open("util/hallucinations.json", "r") as json_file:
  # Load the JSON data into a Python object (list or dict)
  hallucinations = json.load(json_file)

def check_hallucination(input):
  return (input.lstrip().startswith("*")) or (input in hallucinations)