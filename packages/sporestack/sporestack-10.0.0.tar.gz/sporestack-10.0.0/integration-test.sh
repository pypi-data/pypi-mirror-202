#!/bin/sh

# These are pretty hacky and need to be cleaned up, but serve a purpose.

# Set REAL_TESTING_TOKEN for more tests.

set -ex

export SPORESTACK_DIR=$(pwd)/dummydotsporestackfolder

rm -r $SPORESTACK_DIR
mkdir $SPORESTACK_DIR

sporestack version
sporestack version | grep '[0-9]\.[0-9]\.[0-9]'

sporestack api-endpoint
sporestack api-endpoint | grep api.sporestack.com

sporestack token list
sporestack token list 2>&1 | wc -l | grep '2$'

sporestack token import importediminvalid --key "imaninvalidkey"
sporestack token list | grep importediminvalid
sporestack token list | grep imaninvalidkey
sporestack server launch --no-quote --token neverbeencreated --operating-system debian-11 --days 1 2>&1 | grep 'does not exist'

# Online tests start here.

sporestack token create --dollars 50 --currency fakecurrency ihaveafakecurrency 2>&1 | grep 'value is not a valid'
sporestack server launch --no-quote --token importediminvalid --operating-system debian-11 --days 1 2>&1 | grep 'ensure this value has at least 32'

sporestack server flavors | grep vcpu
sporestack server operating-systems | grep debian-11

if [ -z "$REAL_TESTING_TOKEN" ]; then
	echo "REAL_TESTING_TOKEN not set, not finishing tests."
	echo Success
	exit 0
else
	echo "REAL_TESTING_TOKEN is set, will continue testing."
fi

sporestack token import realtestingtoken --key "$REAL_TESTING_TOKEN"
sporestack token balance realtestingtoken | grep -F '$'
sporestack token messages realtestingtoken
sporestack token servers realtestingtoken

sporestack server launch --no-quote --token realtestingtoken --operating-system debian-11 --days 1 --hostname sporestackpythonintegrationtestdelme
sporestack server topup --token realtestingtoken --hostname sporestackpythonintegrationtestdelme --days 1
sporestack server info --token realtestingtoken --hostname sporestackpythonintegrationtestdelme
sporestack server json --token realtestingtoken --hostname sporestackpythonintegrationtestdelme
sporestack server start --token realtestingtoken --hostname sporestackpythonintegrationtestdelme
sporestack server stop --token realtestingtoken --hostname sporestackpythonintegrationtestdelme
sporestack server rebuild --token realtestingtoken --hostname sporestackpythonintegrationtestdelme
sporestack server delete --token realtestingtoken --hostname sporestackpythonintegrationtestdelme
sporestack server forget --token realtestingtoken --hostname sporestackpythonintegrationtestdelme

echo Success
