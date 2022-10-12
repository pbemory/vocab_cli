import csv, os, random
import config
from wordnik_api_client import WordnikClient

wordnik_client = WordnikClient()

results = wordnik_client.get_def("overhang")

