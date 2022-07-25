# Sample Project

## Requirements:

1. [Github account]
2. [Heroku account]
3. [Vs code IDE]
4. [GIT cli]
5. [for git command documentation:] https://git-scm.com/docs/gittutorial

Creating  conda environment
```

conda create -p <venv name> python==3.7 -y

```

```

conad activate <venv name>
or 
conda activate <venv name>/
```

```
pip install -r requirements.txt

```

```

While pushing to git ignore the <venv name> file
add respective <venv name> in .gitignore file in environment list

```
```
to add files:
 git add .
 git add filename
 ```
 > Note: to ignore any files add the respective file in git.ignore file. For folder add <folder name> /
 ```
 to check git status
 ```
 ```
 to check the version of files
git log
```
```
git commit -m "message"
to commit changes
```
``` 
to push changes to git hub
git push origin <branch name>
```

``` 
to check remote url
git remote -v
```

To setup CI/CD pipeline in herooku we need 3 steps:
1. HEROKU_EMAIL = vikaslakkacs@gmail.com
2. HEROKU_API_KEY = <API key>
3. HEROKU_APP_NAME = ml-regression-vilakka


BUILD DOCKER IMAGE
```
docker build -t <image_name>:<tagname>
```
> Note: image name for docker must be lower case


to list docker image
```
docker images
```
to run docker image
```
docket run -p 5000:5000 -e PORT=5000 <image id> (you will get in the docker image syntax details)
```
Common issues:
```
Port is already in use: check what is using the port with command: sudo lsof -i tcp:5000
If any port is using then kill if necessary: sudo kill -9 <PID>
Else: change the port name
```

to check the run container
```
docker ps
```
to stop docker container
```
docker stop <container_id>
```


```
Create setup file and provide the inputs
script: python setup.py install
```