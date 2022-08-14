# Set base image (host OS)
FROM python:3.8-alpine

# By default, listen on port 5000
EXPOSE 5000/tcp

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# RUN apk add --no-cache --update \
#     python3 python3-dev gcc g++\
#     gfortran musl-dev build-base libevent-dev freetype-dev libpng-dev openblas-dev 

RUN apk add g++ postgresql-dev cargo gcc python3-dev libffi-dev musl-dev zlib-dev jpeg-dev


# Install any dependencies
RUN pip install --upgrade pip setuptools && \ 
    pip install -r requirements.txt && \
    pip install --no-use-pep517 pandas 


# Copy the content of the local src directory to the working directory
ADD static ./static
ADD templates ./templates
COPY app.py .
COPY covid_tracer.py .
COPY main.py .
COPY proximityCalculator.py .
COPY .env .



# Specify the command to run on container start
CMD [ "python", "./app.py" ]