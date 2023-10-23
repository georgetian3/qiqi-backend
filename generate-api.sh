#!/bin/bash

curl -C - -o openapi-generator.jar --url https://repo1.maven.org/maven2/org/openapitools/openapi-generator-cli/7.0.1/openapi-generator-cli-7.0.1.jar
rm openapi.json
python3 main.py --openapi
java -jar openapi-generator.jar generate -i openapi.json -g dart -o ~/repos/qiqi-app/lib/api
#python3 fix_api.py