# Random_team, Computational Creativity course, 2019

## How to run the stuff

In our group folder there is a file called *random_team_main_config.json*. 
Use this one to run *main.py* and test how our project works. Currently project
just read *dummy.jpg* and changes its color space.

To initialize the repository go the following steps:

First, from the main folder go to folder *random_team* and run

```bash
python3 -m venv venv
```

**NOTE:** Virtual environment should be called *venv* to exclude it from commits.

Then run virtual environment:

```bash
venv\Scripts\activate
```

Inside virtual environment run:

```bash
pip install -r ../requirements.txt
```

This will install all Python packages from the main folder. Personally I ran into
problem with *opencv-contrib-python*. Directly installing it 
from pip console solved my problem:

```bash
pip install opencv-contrib-python
```

This installs exactly the same version as listed in requirements. Please, note, that all libraries
following *opencv-contrib-python* in *requirements.txt* will not be installed
if installation fails at that step. So, you'll have to install them manually.
