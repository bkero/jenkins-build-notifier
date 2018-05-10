#!/usr/bin/env python

import os

# URL to your Jenkins instance (with trailing slash)
jenkins_url = os.getenv("JENKINS_URL") or 'http://localhost:8080'

# A secret build token to be passed onto Jenkins to prove legitimacy
jenkins_build_token = os.getenv("JENKINS_BUILD_TOKEN") or 'abc123'

# The source IP of phabricator's incoming traffic
phabricator_ip = os.getenv("PHABRICATOR_IP") or '127.0.0.1'

# The path that Phabricator will make a request to
build_path = os.getenv("BUILD_PATH") or '/buildByToken/buildWithParameters'

# What interface JBN should listen on
listen = os.getenv("LISTEN") or '127.0.0.1'

# What port JBN should listen on
port = os.getenv("PORT") or 8000
