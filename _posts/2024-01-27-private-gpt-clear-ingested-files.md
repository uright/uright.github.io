---
title: "privateGPT Clear Ingested Files"
description: "Streamline Your privateGPT Experience: A Guide to Effortlessly Clearing Ingested Files with a Custom Python Script"
date: 2024-01-27 23:25:28 -0500
categories: [Tech, AI]
tags: [privategpt, python, api]
image:
  path: /assets/img/2024-01-27-private-gpt-clear-ingested-files/private-gpt.png
  alt: privateGPT Clear Ingested Files
redirect_from:
  - /blogs/2024-01-27-private-gpt-clear-ingested-files/
---

# privateGPT: An Overview and Recent Updates

As an avid follower of [privateGPT](https://github.com/imartinez/privateGPT), I have been closely monitoring its evolution. Recently, privateGPT has undergone significant enhancements, notably the integration of a web-based User Interface (UI) and a robust backend Application Programming Interface (API).

# Addressing a Common Challenge: Efficiently Managing Ingested Documents

A frequent scenario for privateGPT users involves the need to interact with a fresh set of documents. However, the current UI lacks a direct feature for clearing previously ingested files. Traditionally, this would require stopping the server and manually deleting the `/local_data/private_gpt/qdrant` folder to reset the vector database. For those seeking a more streamlined approach that avoids server restarts, I have developed a concise Python script. This script leverages the newly introduced ingest API to efficiently manage your documents.

## The Solution: A Python Script for Simplified File Management

Below is the Python script I crafted, titled delete-ingested.py. This script is designed to list and delete all documents that have been ingested into privateGPT, thereby simplifying the file management process:

```bash
# Install required dependency
echo "requests" >> requirements.txt
pip install -r requirements.txt
```

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

## Executing the Script
To clear the ingested/indexed files, simply execute the script with the following command:

```bash
python3 delete-ingested.py
```