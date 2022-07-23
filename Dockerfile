FROM python:3.7
## Copy all the workfiles (.) top /app
COPY . /app
## Assign work directory as /app folder
WORKDIR /app
### Install all the requirements
RUN pip install -r requirements.txt
## Set the port when creating docker
EXPOSE $PORT
## run gunicorn
CMD gunicorn --workers=1 --bind 0.0.0.0:$PORT app:app