#!/bin/sh

set -xeu

rm -rf package
rm -f os-proxy-lambda.zip
mkdir -p package
pip install --target ./package -r requirements.txt
cp *.py package/
cd package
zip -r ../os-proxy-lambda.zip .
cd ..