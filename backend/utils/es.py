from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os

load_dotenv()
ES_HOST = os.getenv("HOST")
ES_USER = os.getenv("USER")
ES_PASS = os.getenv("PASSWORD")

def get_elastic():
    return Elasticsearch(
        ES_HOST,
         basic_auth=(ES_USER, ES_PASS),
         verify_certs=False,
    )