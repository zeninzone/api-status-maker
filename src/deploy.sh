#!/bin/bash

RANDSTR=$(mktemp --dry-run XXXXX)

docker build -t alsaheem/api-status-checker:latest .

docker push alsaheem/api-status-checker:latest