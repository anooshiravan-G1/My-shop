# Pull base image
FROM python:3.8
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Set work directory
WORKDIR /code
# Install dependencies
RUN apt-get update && apt-get install -y gettext zlib1g-dev
COPY Pipfile Pipfile.lock /code/
#RUN pip install pipenv && pipenv install --system
COPY requirements.txt ./
RUN pip install -r requirements.txt
                     
# COPY requirements.txt ./
# RUN pipenv install -r requirements.txt

# Copy project
COPY . /code/