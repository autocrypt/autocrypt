#!/bin/bash

# only attempt to deploy if we know the secrets for the ssh key
test $encrypted_ee89c1e228aa_key || exit 0
test $encrypted_ee89c1e228aa_iv || exit 0

# Prepare the ssh homedir.
#
# Decrypting the ssh private key for deploying to the server.
# See https://docs.travis-ci.com/user/encrypting-files/ for details.
mkdir -p -m 0700 ~/.ssh
openssl aes-256-cbc -K $encrypted_ee89c1e228aa_key -iv $encrypted_ee89c1e228aa_iv -in .credentials/autocrypt.id_rsa.enc -out ~/.ssh/id_rsa -d
chmod 600 ~/.ssh/id_rsa
cat .credentials/autocrypt.org.hostkeys >> ~/.ssh/known_hosts
printf "Host *\n" >> ~/.ssh/config
printf " %sAuthentication no\n" ChallengeResponse Password KbdInteractive >> ~/.ssh/config

# To debug your ssh connection enable this...
# scp -r -v \
#   -o StrictHostKeyChecking=no \
#   -o PasswordAuthentication=no \
#   -o IdentitiesOnly=yes \
#   -i $TRAVIS_BUILD_DIR/id_rsa \
#   $TRAVIS_BUILD_DIR/doc/_build ${DEPLOY_USER}@autocrypt.org:~/test

rsync -avz $TRAVIS_BUILD_DIR/doc/_build/html/ \
  ${DEPLOY_USER}@autocrypt.org:build/${TRAVIS_BRANCH/\//_}

rsync -avz $TRAVIS_BUILD_DIR/doc/_build/latex/autocrypt*.pdf \
  ${DEPLOY_USER}@autocrypt.org:build/${TRAVIS_BRANCH/\//_}
