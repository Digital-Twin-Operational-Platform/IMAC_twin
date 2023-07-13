# Template_DTOP
This is the fundamental architecture for generating a new DTOP system

## Deployment Instruction
There are two main methods for deploying this app

### Gunicorn/Waitress with Virtual Environment
Gunicorn is not available on windows platforms due to dependcy on the FCNTL module, only Unix-based systems. Waitress is an alternative with similar usage.

- To run the DTOP system, first create a virtual environment in the main folder

For linux:
```bash
python3 -m venv env
```
For Anaconda:
```bash
python -m venv env
```

- Then enter the environment

For linux:
```bash
source env/bin/activate
```
For Anaconda:
```bash
env\Scripts\activate
```

- Update pip to current version

For linux/Anaconda:
```bash
pip install --upgrade pip
```

- Then install requirements

For linux/Anaconda:
```bash
pip install -r requirements.txt
```

- Then run the application

For linux:
```bash
gunicorn --bind=127.0.0.1:5000 "digitaltwin:create_app()"
```
For Anaconda (needs admin rights):
```bash
waitress-serve --listen=127.0.0.1:5000 --call "digitaltwin:create_app"
```

- Then, in a web browser, go to either 127.0.0.1:5000 or localhost:5000 to access the DTOP platform

### Docker Development deployment
- Ensure that `docker` and `docker compose` are both installed on the deployment machine

Use this option for deployment on a machine where the certificates are not installed (https) and a http connection is sufficient.
```bash
docker compose up --build -d
```

Then, in a web browser, go to either 127.0.0.1 or local host to access the DTOP platform.
The docker deployment uses nginx to convert from port 5000 to port 80, which is the regular http port.

- Note: the `--build` flag will (re)build the images before running them.
- Note: the `-d` flag will run the images in detached mode (i.e. as a background processes).