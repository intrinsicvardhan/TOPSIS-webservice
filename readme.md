# TOPSIS Web Application Docker Container

This repository contains the dockerfile and necessary files to create a docker container

## Prerequisites
-   Docker installed on your machine 
-   A CSV file with the data you want to rank using TOPSIS

## Building the Docker Image 

TO build the docker image, navigate to the directory containing the docker file and run the following in your shell 

```bash 
docker build -t topsis-web-app .
```

Running the docker container 
-   After the image is built, you can run the container with the following commd:

```bash
docker run -p 5000:5000 -d topsis-web-app
```

The command maps port 5000 inside the container to port 5000 on your machine 

Once the container is running, you can access the web application by navigating to 
```bash
http://localhost:5000
```
