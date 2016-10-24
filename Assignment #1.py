import numpy as np
import matplotlib.pyplot as plt
import sys
import json


fname = open("dictionary.json").read()
mydictionary = json.loads(fname)
keys = mydictionary.keys()
keys = sorted(keys, key=len)
for key in keys:
    print key
