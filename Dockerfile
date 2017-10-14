# Set base image
FROM alpine

# Install dependencies
RUN 	apk update
RUN   apk upgrade
RUN 	apk add python
RUN		apk add py2-requests
# RUN 	apk add py-simplejson

# Create working directory
WORKDIR /home/dev/rl-overage

# Move scripts into container
COPY . .

# setup CRON to update plugin hourly
#todo CRON
