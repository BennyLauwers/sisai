# base image
FROM python:3.7.11
# set web server root as working dir
WORKDIR /home/site/wwwroot
# install required packages
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pyyaml==6.0
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

# copy all files
COPY . .

# expose port 8000
EXPOSE 8000

# start flask app using Gunicorn
ENV GUNICORN_CMD_ARGS="--bind 0.0.0.0:8000 --timeout 600 --workers=4"
CMD ["gunicorn","app:app"]