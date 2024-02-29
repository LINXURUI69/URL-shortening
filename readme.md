# Homework 3: Virtualization using containers (Docker)

This document outlines the steps required to deploy services using Docker and test them locally and within a Kubernetes (K8s) cluster.

## Deploying Services with `docker-compose`

1. To deploy your services, navigate to the directory containing your `docker-compose.yaml` file and run the following command:

```bash
docker-compose up
```
## Local Testing

The services are exposed on the following ports for local testing through HTTP methods:

URL-Shortening Service: Available at `localhost:5001`
Authentication Service: Available at `localhost:5000`

You can use tools like curl or Postman to test the HTTP endpoints.

## Testing in Kubernetes Cluster

The services are also deployed in a Kubernetes (K8s) cluster and can be tested on the following URLs:

URL-Shortening Service: Exposed at port 31984, accessible via `http://145.100.135.225:31984/`

Authentication Service: Exposed at port 31650, accessible via `http://145.100.135.226:31650/`

Ensure your Kubernetes cluster is correctly set up and accessible before attempting to test these services.

## Used files

`Dockerfile.authentication` is used in assignment 3.1 and 3.2
`Dockerfile.url_shorening` is used in assignment 3.1 and 3.2
`docker-compose.yaml` is used in assignment 3.1
`authentication.yaml` and `urlshorten.yaml` are used in assignment 3.2