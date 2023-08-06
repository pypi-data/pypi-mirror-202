import os
import requests

api_key = os.environ["NARC_API_KEY"]

base_url = "https://narc.goapollo.ai/api/v1/"

def mappings(text, source="free text"):
    url = f"{base_url}mappings"
    headers = {
        "source": source,
        "api-key": api_key
    }
    payload = text
    r = requests.post(url,headers=headers,json=payload)
    return r.json()

def mappings_bulk(text):
    url = f"{base_url}mappings_bulk"
    headers = {
        "api-key": api_key
    }
    payload = text
    r = requests.post(url,headers=headers,json=payload)
    return r.json()

def mappings_insights(technique_id):
    url = f"{base_url}mappings_insights"
    headers = {
        "technique-id": technique_id,
        "api-key": api_key
    }
    r = requests.get(url,headers=headers)
    return r.json()

def chains(text, source="free text"):
    url = f"{base_url}chains"
    headers = {
        "source": source,
        "api-key": api_key
    }
    payload = text
    r = requests.post(url,headers=headers,json=payload)
    return r.json()

def chains_bulk(text):
    url = f"{base_url}chains_bulk"
    headers = {
        "api-key": api_key
    }
    payload = text
    r = requests.post(url,headers=headers,json=payload)
    return r.json()

def chains_insights(technique_id):
    url = f"{base_url}chains_insights"
    headers = {
        "technique-id": technique_id,
        "api-key": api_key
    }
    r = requests.get(url,headers=headers)
    return r.json()

def custom_common_chains(text):
    url = f"{base_url}custom_common_chains"
    headers = {
        "api-key": api_key
    }
    payload = text
    r = requests.post(url,headers=headers,json=payload)
    return r.json()

def custom_longest_chain(text):
    url = f"{base_url}custom_longest_chain"
    headers = {
        "api-key": api_key
    }
    payload = text
    r = requests.post(url,headers=headers,json=payload)
    return r.json()