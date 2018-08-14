#!/bin/bash

USERID=test
NOTEID=n-1010
CONTENT=testing123
REQID=r-1010
PROFILE=1527

echo
echo "########## testing create.py ##########"
python test/test_create.py $USERID $NOTEID $CONTENT $REQID $PROFILE

echo
echo "########## testing get.py ##########"
python test/test_get.py $USERID $NOTEID $REQID $PROFILE

echo
echo "########## testing list.py ##########"
python test/test_list.py $USERID $REQID $PROFILE

echo
echo "########## testing update.py ##########"
python test/test_update.py $USERID $NOTEID $CONTENT $REQID $PROFILE
