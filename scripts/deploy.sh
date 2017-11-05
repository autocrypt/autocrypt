#!/bin/bash

# To debug your ssh connection enable this...
# scp -r -v \
#   -o StrictHostKeyChecking=no \
#   -o PasswordAuthentication=no \
#   -o IdentitiesOnly=yes \
#   -i $TRAVIS_BUILD_DIR/id_rsa \
#   $TRAVIS_BUILD_DIR/doc/_build ${DEPLOY_USER}@autocrypt.org:~/test

rsync -a $TRAVIS_BUILD_DIR/doc/_build ${DEPLOY_USER}@autocrypt.org:test \
  -e "ssh -o StrictHostKeyChecking=no -o PasswordAuthentication=no -i $TRAVIS_BUILD_DIR/id_rsa"
