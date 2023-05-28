# Using node:16-alpine base image
FROM node:16-alpine 

# Set /app as the default work directory
WORKDIR /app

# copy package.json to the working directory for packages installation
COPY package.json /app

# Install npm dependencies
RUN npm install

# Copy all the project files to the working directory
COPY . .

# Expose the port of your application to bind with the host port
EXPOSE 80

# run your app
CMD ["npm", "run", "start"]

# docker build -t basic-node-server .  
# docker tag basic-node-server:latest alejandro945/basic-node-server:latest
# docker push alejandro945/basic-node-server:latest
# sudo docker run -it -p 80:80 -d basic-node-server  
