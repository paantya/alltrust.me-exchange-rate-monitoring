#!/bin/bash

docker stop $(basename $(pwd))
docker rm $(basename $(pwd))
docker run --restart always -v $(pwd):$(pwd) --name $(basename $(pwd)) python:3.6-slim /bin/sh -c "/usr/local/bin/python -m pip install --upgrade pip; cd $(pwd); pip3 install -r ./requirements.txt; pip3 cache purge; python3 ./scripts/fetch_data.py 2> w.err"
