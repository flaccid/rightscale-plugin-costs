# Set base image
FROM  alpine

# Install dependencies
RUN apk update
RUN apk upgrade
RUN apk add python
RUN apk add py2-requests

# Create working directory
WORKDIR /home/dev/rl-overage

# Move scripts into container
COPY  . .

RUN ["chmod", "+x", "/home/dev/rl-overage/entrypoint.sh"]

# todo setup CRON to update plugin hourly
