# Docker for server

## build
The docker is easily built using the following command - By default, it builds the docker for the **develop** branch:

```
 docker build . -t iotagent-turtle 
```

If we want to build other branch, we could define the branch we want to use this way:
```
 docker build . -t iotagent-turtle --build-arg BRANCH=integration-cb-httpserver
```

Everything will install in /proc/IotAgent-turtle inside the container. The default config file will be the following one:

```
{
  "broker": "http://orion-ld:1026",
  "logger": {
    "path": "./logs/access.log",
    "level": "debug",
    "rotation": "20 days",
    "retention": "1 months",
    "format": "<level>{level: <8}</level> <green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> request id: {extra[request_id]} - <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>"
  }
}
```

## Use
Let's suppose the image is named **iotagent-turtle** and we want to expose port 5000 in order to work. We can also imagine that we want to remove the container when it finishes, we can do it this way:
```
docker run --rm -p 5000:5000 --name io  iotagent-turtle
```

However, we might have Orion-ld somewhere else. Therefore, we can provide the IP address of the host "orion-ld" where our Context Broker is listening this way:
```
docker run --rm -p 5000:5000 --name io --add-host=orion-ld:192.168.1.206  iotagent-turtle
```

### Overriding config.json
We could create our own config.json and the default configuration file in the docker:
```
docker run --rm -p 5000:5000 --name io -v our-local-config.json:/opt/IoTAgent-turtle/common/config.json iotagent-turtle
```

### As docker file

We can consider writing a docker-compose.yaml file as the following one to start everything (orion-ld, the name of our orion server is named according to our config.json file -- see "broker" key):

```
version: "3.8"
services:
  orion-ld:
    image: fiware/orion-ld
    hostname: orion-ld
    container_name: orion-ld
    expose:
      - 1026
    ports:
      - 1026:1026
    depends_on:
      - fiware-orion-ld-mongo-db
    command: -dbhost fiware-orion-ld-mongo-db -logLevel DEBUG -experimental

  fiware-orion-ld-mongo-db:
    image: mongo:5.0
    hostname: mongo-db
    networks:
      - default
    command: --nojournal
    volumes:
      - /data/docker/orion-ld/mongodb:/data

  iotagent-turtle:
    image: iotagent-turtle:latest
    hostname: ioagent-turtle
    container_name: iotagent-turtle
    expose:
      - 5000
    ports:
      - 5000:5000
    networks:
      - default
```
 
