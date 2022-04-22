# init a base image (Alpine is small Linux distro)
FROM python:alpine
# define the present working directory
WORKDIR /api-trade
# copy the contents into the working dir
ADD . /api-trade

EXPOSE 80
# ENV FLASK_APP=app.py

# run pip to install the dependencies of the flask app
RUN pip install -r requirements.txt
# define the command to start the container
CMD ["python3", "app.py"]