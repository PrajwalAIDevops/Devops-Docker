# Personal Website (Flask)

Simple Flask personal website with a clean template structure.

## Run locally (Windows)

1) Create venv:

```bat
python -m venv .venv
```

2) Activate:

```bat
.\.venv\Scripts\activate
```

3) Install deps:

```bat
pip install -r requirements.txt
```

4) Start:

```bat
set FLASK_DEBUG=1
python app.py
```

Open: `http://localhost:5000`

## Deploy notes
This project is ready to be containerized/deployed later (e.g., AWS ECS/EC2), but the current setup is for local usage.

