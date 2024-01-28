+++
title = 'privateGPT Clear Ingested Files'
date = 2024-01-27T23:25:28-05:00
draft = false
+++

# PrivateGPT

I've been following [privateGPT](https://github.com/imartinez/privateGPT) for quite sometimes now. Recently, they have made some big updates to the application. It now supports a web UI and backend API.

![privateGPT](/img/2024-01-27-private-gpt-clear-ingested-files/private-gpt.png)

# Problem & Solution

More than often, you may wish chat with another set of documents. The current UI does not consists of a clear ingested file option. Normally, you would stop the server, and manually remove `/local_data/private_gpt/qdrant` folder to clear off the vector database. But if you don't wish to restart, I've written a small python script to make use of the newly ingest API.

```python
# `delete-ingested.py`
import requests

def get_doc_ids():
    url = "http://localhost:8001/v1/ingest/list"
    headers = {
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        doc_ids = [doc["doc_id"] for doc in data["data"]]
        return doc_ids
    else:
        print("Error: API call failed with status code:", response.status_code)
        return []

# Write a function to delete all the documents
# that have been ingested into the system
def delete_docs(doc_ids):
    url = "http://localhost:8001/v1/ingest/" + doc_ids
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    response = requests.delete(url, headers=headers)

    if response.status_code == 200:
        print("All documents deleted successfully")
    else:
        print("Error: API call failed with status code:", response.status_code)


doc_ids = get_doc_ids()

# Loop through the doc_ids and delete them
for doc_id in doc_ids:
    delete_docs(doc_id)
```

Simply run this script to clear the ingested/indexed file.
```bash
python3 delete-ingested.py
```
