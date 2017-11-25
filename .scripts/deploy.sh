#!/bin/bash

# To debug your ssh connection enable this...
# scp -r -v \
#   -o StrictHostKeyChecking=no \
#   -o PasswordAuthentication=no \
#   -o IdentitiesOnly=yes \
#   -i $TRAVIS_BUILD_DIR/id_rsa \
#   $TRAVIS_BUILD_DIR/doc/_build ${DEPLOY_USER}@${DEPLOY_SERVER}:~/test

rsync -avz $TRAVIS_BUILD_DIR/doc/_build/html/ \
  ${DEPLOY_USER}@${DEPLOY_SERVER}:build/${TRAVIS_BRANCH/\//_}

rsync -avz $TRAVIS_BUILD_DIR/doc/_build/latex/autocrypt*.pdf \
  ${DEPLOY_USER}@${DEPLOY_SERVER}:build/${TRAVIS_BRANCH/\//_}
