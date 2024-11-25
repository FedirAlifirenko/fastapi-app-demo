# Backend API (FastAPI app)

## Development
### Installation
#### Install python3.12 virtual environment and activate it
```commandline
python3.12 -m venv .venv
source .venv/bin/activate
```
#### Install Poetry in the previously created virtual environment
```commandline
pip install poetry
```
#### Install project using poetry
```commandline
poetry config virtualenvs.create false
poetry install --with dev
```

### Testing
#### Locally
Run lint checks
```commandline
poetry run task lint
```
Run tests
```commandline
poetry run task test
```

#### Docker
Run tests in docker
```commandline
docker compose run --rm test
```


### Running
Run everything in docker
```commandline
docker compose up
```
Open [http://localhost:8000/docs](http://localhost:8000/docs) in your browser to see the API documentation.
