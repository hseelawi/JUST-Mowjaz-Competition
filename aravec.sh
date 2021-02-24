#! /bin/bash

set -e

if [[ $ARAVEC ]]
then
        curl $ARAVEC --output embeddings.zip
else
        curl 'https://bakrianoo.s3-us-west-2.amazonaws.com/aravec/full_uni_sg_300_twitter.zip' --output embeddings.zip
fi

unzip embeddings.zip -d models/ 
