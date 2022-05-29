#!/bin/bash

# The following environment variables need to be defined in the deployent.yaml file of the extractor:

sleep 5
echo '--------- Pod Diagnostics --------------'
echo "PATH: ${PATH}"
unset AWS_DEFAULT_REGION
unset AWS_ACCESS_KEY_ID
unset AWS_SECRET_ACCESS_KEY

PYTHON=`which python3`
AWS=`which aws`

echo "Which python? ${PYTHON}"
echo "Which aws? ${AWS}"

echo "Is printenv there?"
ls -l /usr/bin/printenv
test_printenv=$?
echo "Is python3 there?"
ls -l /usr/local/bin/python3
test_python3=$?
echo "Is aws there?"
ls -l /usr/local/bin/aws
test_aws=$?
echo "Is /usr/bin there?"
ls -ld /usr/bin
test_usr_bin=$?
echo "Is /usr/local/bin there?"
ls -ld /usr/local/bin
echo "Is /usr there?"
ls -ld /usr
echo '----------------------------------------'
if [ "${test_printenv}" != "0" ] || [ "${test_python3}" != "0" ] || [ "${test_aws}" != "0" ] || [ "${test_usr_bin}" != "0" ]; then
    # Obtain the sleep period before crashing pod
    if [[ -z "${CRASH_SLEEP_DURATION}" ]]; then
        sleep_duration=120
    else
        sleep_duration=$CRASH_SLEEP_DURATION
    fi
    echo "[`date`] Reality Dysfunction detected, pod will now enter ${sleep_duration} seconds of sleep and then crash."
    sleep $sleep_duration
    exit 1
fi

echo '----------------------------------------'

# Registering to Nexus

if [[ -z "${NO_REGISTRATION_REQUIRED}" ]] && [[ "$IS_REST_EXTRACTOR" != "True" ]]; then
#    cd /opt/docker/common
    $PYTHON -m beehive_infra.common.register
else
    echo "No registration required."
fi

error=$?
if [ "${error}" != "0" ]; then
    echo "There was an error reported by register.py, aborting initialization and dying..."
    exit 1
else
    echo "Extractor started successfully."
    cd /opt/docker/extractor
    if [ "$IS_REST_EXTRACTOR" = "True" ]
    then
      echo "Running rest extractor."
      uvicorn rest_extractor:app --proxy-headers --host 0.0.0.0 --port 80
#      tail -f /dev/null
    else
      echo "Running asynchronous extractor."
      $PYTHON /opt/docker/extractor/extractor.py
    fi
fi