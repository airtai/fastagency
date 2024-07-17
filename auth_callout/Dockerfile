# Use the official Node.js 20 image as a parent image
FROM node:20-alpine

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy the auth_callout directory contents into the container at /usr/src/app
COPY ./ .

# Install pnpm
RUN npm install -g pnpm && ls -lah

# Install any dependencies
RUN pnpm install --force

# Define the command to run your app using pnpm serve
ENTRYPOINT []
CMD ["/bin/sh", "-c", "./run-auth-callout.sh"]
