#!/bin/bash

docker build -t alsaheem/api-status-checker:latest .

docker push alsaheem/api-status-checker:latest

# docker run -p 5001:5000 -v ./config/config.ini:/app/config/config.ini alsaheem/api-status-checker:latest
