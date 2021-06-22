#!/bin/bash

pushd `dirname $0` >/dev/null

aws s3 cp ./glue s3://${GLUE_SCRIPT_BUCKET}/ --exclude "*" --include "*.py" --recursive

popd >/dev/null
