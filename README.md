# Sample Project

## Requirements:

1. [Github account]
2. [Heroku account]
3. [Vs code IDE]
4. [GIT cli]

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