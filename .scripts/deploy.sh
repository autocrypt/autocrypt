#!/bin/bash
set -e
set -u
set -x
# To debug your ssh connection enable this...
# scp -r -v \
#   -o StrictHostKeyChecking=no \
#   -o PasswordAuthentication=no \
#   -o IdentitiesOnly=yes \
#   -i $TRAVIS_BUILD_DIR/id_rsa \
#   $TRAVIS_BUILD_DIR/doc/_build ${DEPLOY_USER}@${DEPLOY_SERVER}:~/test

mkdir -p -m 0700 ~/.ssh
openssl aes-256-cbc -K $encrypted_ee89c1e228aa_key -iv $encrypted_ee89c1e228aa_iv -in .credentials/autocrypt.id_rsa.enc -out ~/.ssh/id_rsa -d
chmod 600 ~/.ssh/id_rsa
cat .credentials/autocrypt.org.hostkeys >> ~/.ssh/known_hosts
printf "Host *\n" >> ~/.ssh/config
printf " %sAuthentication no\n" ChallengeResponse Password KbdInteractive >> ~/.ssh/config

rsync -avz $TRAVIS_BUILD_DIR/doc/_build/html/ \
  ${DEPLOY_USER}@${DEPLOY_SERVER}:build/${TRAVIS_BRANCH/\//_}

rsync -avz $TRAVIS_BUILD_DIR/doc/_build/latex/autocrypt*.pdf \
  ${DEPLOY_USER}@${DEPLOY_SERVER}:build/${TRAVIS_BRANCH/\//_}
