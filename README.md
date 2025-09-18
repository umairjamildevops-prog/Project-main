# CI/CD Pipeline for Flask App with GitHub Actions & Docker

## Objective

Implement a **CI/CD pipeline** to: - Build & test a Python Flask app -
Containerize it with Docker - Automate build & push to Docker Hub using
**GitHub Actions** - Deploy locally using the pushed Docker image

------------------------------------------------------------------------

## Tools Used

-   Python (Flask, Pytest)
-   Docker & Docker Compose
-   GitHub Actions (CI/CD)
-   Docker Hub (container registry)
-   AWS EC2 (optional for deployment)

------------------------------------------------------------------------

## Project Structure

    my-flask-cicd/
    ├── app.py
    ├── requirements.txt
    ├── tests/
    │   └── test_app.py
    ├── Dockerfile
    ├── docker-compose.yml
    └── .github/
        └── workflows/
            └── ci.yml

------------------------------------------------------------------------

## Steps

### 1. Create Repository & Clone

``` bash
git config --global init.defaultBranch main
mkdir my-flask-cicd && cd my-flask-cicd
git init
git remote add origin https://github.com/<your-username>/my-flask-cicd.git
```

------------------------------------------------------------------------

### 2. Application Code & Tests

**app.py**

``` python
from flask import Flask, jsonify

app = Flask(__name__)

@app.get("/")
def index():
    return jsonify(message="Hello from CI/CD!"), 200

@app.get("/healthz")
def healthz():
    return jsonify(status="ok"), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
```

**requirements.txt**

    flask==3.0.3
    gunicorn==21.2.0
    pytest==8.2.0

**tests/test_app.py**

``` python
from app import app

def test_healthz():
    client = app.test_client()
    res = client.get("/healthz")
    assert res.status_code == 200
    assert res.get_json()["status"] == "ok"
```

------------------------------------------------------------------------

### 3. Containerization

**Dockerfile**

``` dockerfile
FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8000
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "app:app"]
```

**docker-compose.yml**

``` yaml
version: "3.8"
services:
  web:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
```

**Local test**

``` bash
docker compose up --build -d
curl http://localhost:8000/healthz
docker compose down
```

------------------------------------------------------------------------

### 4. CI/CD with GitHub Actions

#### 4.1 Add Docker Hub Secrets in GitHub

-   `DOCKERHUB_USERNAME`
-   `DOCKERHUB_TOKEN`

#### 4.2 Workflow file: `.github/workflows/ci.yml`

``` yaml
name: CI-CD

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

env:
  IMAGE_NAME: ${{ secrets.DOCKERHUB_USERNAME }}/my-flask-cicd

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Run tests
        run: pytest -q

  build-and-push:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Log in to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Set up Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: |
            ${{ env.IMAGE_NAME }}:latest
            ${{ env.IMAGE_NAME }}:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

------------------------------------------------------------------------

### 5. Commit & Push

``` bash
git add .
git commit -m "CI/CD: Flask app, Docker, GH Actions"
git branch -M main
git push -u origin main
```

------------------------------------------------------------------------

### 6. Run Image Locally (after CI/CD push)

``` bash
docker pull <your-username>/my-flask-cicd:latest
docker run -d -p 8000:8000 --name my-flask-app <your-username>/my-flask-cicd:latest
curl http://localhost:8000/
docker stop my-flask-app && docker rm my-flask-app
```

------------------------------------------------------------------------

## Proof of Work

### GitHub Actions Workflow
![Workflow](https://github.com/sanjay720813/CI-CD-Pipeline-with-GitHub-Actions-Docker/blob/main/workflows-action.png)

### Pytest Results
![Tests](https://github.com/sanjay720813/CI-CD-Pipeline-with-GitHub-Actions-Docker/blob/main/test.png)

### Build and Push Logs
![Build and Push](https://github.com/sanjay720813/CI-CD-Pipeline-with-GitHub-Actions-Docker/blob/main/build-and-push.png)

### Docker Hub Repository
![Docker Hub Repo](https://github.com/sanjay720813/CI-CD-Pipeline-with-GitHub-Actions-Docker/blob/main/docker%20hub%20repo.png)

### Running Container
![Running Container](https://github.com/sanjay720813/CI-CD-Pipeline-with-GitHub-Actions-Docker/blob/main/Running%20container.png)

### Flask Image in Docker
![Flask Image](https://github.com/sanjay720813/CI-CD-Pipeline-with-GitHub-Actions-Docker/blob/main/my-flask%20image.png)

### Local Deployment
![Local Deployment](https://github.com/sanjay720813/CI-CD-Pipeline-with-GitHub-Actions-Docker/blob/main/deploy%20local.png)
