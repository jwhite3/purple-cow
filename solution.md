# purple-cow
Welcome to this lovely trail project!

## Requirements
- python 3.10
- Docker

## Setup
Since this project is implemented in python with FastAPI, there are a few benefits if devs use PyCharm when working on
this project.
Setup is easier/faster, and a few run configurations are available with the repo to use right off the bat.

### PyCharm setup
To set up with PyCharm:
- Clone the repo and open as a new project in PyCharm
- Create a new interpreter with `venv`
- Install requirements:
```shell
pip install --upgrade pip  # Make sure that pip is upgraded
pip install -r requirements.txt
```
- Try out one of the run configurations!
  - Dockerfile (build/deploy purple-cow locally)
  - Test API (execute unittests)
  - Purple Cow (run the application locally)

### Sans PyCharm
- Clone the repo
- Create a virtual environment with `venv`
```shell
python3 -m venv  # Optionally add a path if you'd like to store the venv file elsewhere
```
- Activate the virtual environment
```shell
source <path to venv>/bin/activate 
```
- Install requirements the same way as above
- Try running the tests with:
```shell
pytest tests
```

### Application configuration
To change the port, update the environment variable, `UVICORN_PORT` with the desired port value.


## Run the application
You can run the application locally either with the included run configuration (if using PyCharm), or with the
following command in the repo after activating the virtual environment:
```shell
python3 -m uvicorn cow.app.main:app
```

## Build/Deploy
From the repo directory:
```shell
docker-compose build
```

Run the container:
```shell
docker-compose up
```

## Automatic documentation:
Once the application is running you can view the main API documentation by hitting the root, `localhost:3000/`.
There are also more "traditional" open-api style docs available at `/docs` where you can also try out some endpoints 
from the UI.

## Future work
- Add an actual DB. The current in-memory solution is fine, but not persistent if the application goes down.
Additionally, an assumption was made that the item ids would be provided by the client, but ideally that would be
controlled server-side (likely as a human-readable unique id, so that the url is more memorable for a particular item)
in the DB.
- Many of the endpoints are not protected against things like race-conditions, and so there might be surprising
results if multiple users are adding/deleting content
- Handle common exceptions globally rather than per path operation function.
- Add restrictions to who can add/delete 
- Add user documentation with sphinx.
The static documents can then be hosted by the application.
I added them to "/design-docs" here because "/docs" is already used by FastAPI, but this could be named anything really.
- Add a build step to the GitHub Workflow
- Make host configurable 


## Notes
Typically, I wouldn't commit directly to master, but I figured that it would take too much time to set up and use a
proper git workflow with issues, prs, etc. Even though it makes me feel all funny, commit to master!