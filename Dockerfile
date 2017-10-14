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

RUN	parent_acc="$(cat /run/secrets/parent_acc)"

# setup CRON to update plugin hourly
# todo CRON
