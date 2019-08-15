#!/bin/bash
cd python
docker build -t my-python-app .

docker run -it -p 8080:8080 --rm --name my-python-running-app my-python-app