FROM python:3.12-alpine3.20

# set working directory
WORKDIR /app

# TLDR; To build Psycopg2 dependency we need the packages gcc musl-dev postgresql-dev
RUN apk add postgresql-libs
RUN apk add --virtual .build-deps gcc musl-dev postgresql-dev

# We also need CURL to properly load the batch of data
RUN apk add curl

# install python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN apk --purge del .build-deps

# Copy the entire application code into the container
COPY app/ ./app

# Copy the start.sh script into the container
COPY start.sh ./

# Copy the data.csv to be inserted upon start
COPY data.csv ./

# Ensure the start.sh script is executable
RUN chmod +x /app/start.sh

# Set PYTHONPATH to allow app module imports
ENV PYTHONPATH=/app

# Set the default command to run the startup script
CMD ["./start.sh"]