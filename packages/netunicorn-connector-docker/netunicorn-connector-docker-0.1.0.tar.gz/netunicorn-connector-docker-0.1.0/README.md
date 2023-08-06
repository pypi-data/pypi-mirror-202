# netunicorn-connector-docker
This is a netunicorn connector for a local Docker infrastructure.


This connector works only with the local Docker daemon, requires current user to be in the docker group
and always presents a single host with the name "dockerhost".

## Usage
1. Attach the connector to the existing netunicorn director instance
2. Provide a docker socket or tcp endpoint to the connector
3. Optionally: ensure that use has access to the docker socket or tcp endpoint and is in the docker group