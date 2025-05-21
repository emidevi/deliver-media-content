from elasticsearch import Elasticsearch
from dotenv import load_dotenv, find_dotenv
import os
import urllib3

# If there is an issue with the SSL certificate, please ignore it while sending the http request.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
load_dotenv()

ES_HOST = os.getenv("HOST")
ES_USER = os.getenv("ELASTICUSER")
ES_PASS = os.getenv("PASSWORD")

def get_elastic():
    return Elasticsearch(
        ES_HOST,
        basic_auth=(ES_USER, ES_PASS),
        verify_certs=False
    )