# Set base image
FROM alpine

# Install python, requests and json
RUN 	apk update
RUN 	apk add python
RUN		apk add py2-requests
RUN 	apk add py-simplejson

# Create app directory
WORKDIR /home/dev/rs-plugin-cost-scripts

# Move plugin cost scripts into container
COPY . .
