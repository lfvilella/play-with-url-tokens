#!/bin/bash

if [[ $1 = 'prod' ]]
then
    uvicorn api:app --host 0.0.0.0
else
    uvicorn api:app --host 0.0.0.0 --reload
fi