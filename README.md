# Media Search

This project implements a lightweight media search system using **FastAPI** and **Elasticsearch**, built to retrieve and serve media content stored in an Elasticsearch index.

## 🚀 Project Overview
- **Backend**: Python + FastAPI
- **Search engine**: Elasticsearch
- **Auth**: Basic HTTP Auth (provided)

## 📂 Directory Structure
```bash
├── backend/
│ ├── main.py # FastAPI application entrypoint
│ ├── utils/
│ │ └── es.py # Elasticsearch client config
├── app.py
├── .env
├── requirements.txt
├── README.md
└── venv/ 
```

## Setup Configuration
1. Make a copy of '.env_example' file as '.env' file and fill out the required values

### Create a Virtual Environment

### Pre-Requisite
 - `Python 3.12.3`
 - `elasticsearch<9.0.0,>=8.0.0`

```bash
python3 -m venv venv
source venv/bin/activate
```
### Install dependencies

```bash
pip install -r requirements.txt
```
### Run the app

```bash
python app.py
```

### Test CURL command
This should return a JSON response from the imago index

```bash
curl -u elastic:<PASSWORD> <HOST>:<PORT>/<INDEX>/_search -k

# -u provides username:password
# -k skips SSL certificate validation
```

