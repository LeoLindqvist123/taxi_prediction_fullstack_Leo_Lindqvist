import json
from taxipred.utils.constants import DATA_PATCH

def read_json():

  with open (DATA_PATCH / model.joblib, "r") as file:
    data = json.load(file)

  return data