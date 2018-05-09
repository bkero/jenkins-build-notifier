#!/usr/bin/env python
"""This is the flask app for intercepting and forwarding HTTP requests"""

from flask import Flask, request
import requests

# URL to your Jenkins instance (with trailing slash)

JENKINS_URL = 'http://localhost:8080'
JENKINS_BUILD_TOKEN = 'abc123'
PHABRICATOR_IP = '127.0.0.1'
BUILD_PATH = '/buildByToken/buildWithParameters'

APP = Flask(__name__)


@APP.route('/')
def index():
    """Drive-by connection or internet probe"""
    return "Go away"


@APP.route(BUILD_PATH)
def build_by_token():
    """Connection sent HTTP URI conforming to spec"""
    # VALIDATE SOURCE IP
    if request.remote_addr != PHABRICATOR_IP:
        return 'You are not phabicator. Go away.'

    # GET THE PARAMETERS
    # EXAMPLE:  https://ci.example.com/buildByToken/\
    #           buildWithParameters?job=test-example&\
    #           DIFF_ID=${buildable.diff}&PHID=${target.phid}

    job = request.args.get('job')
    diff_id = request.args.get('DIFF_ID')
    if diff_id < 1:
        print("Error: diff_id %s invalid in request %s"
              % (diff_id, request.url))
        return 'Bad Request'
    phid = request.args.get('PHID')
    if phid < 1:
        print "Error: phid %s is invalid in request %s" % (phid, request.url)
        return 'Bad Request'
    token = request.args.get('token')

    print "Forwarding request job: %s diff_id: %s phid: %s to %s" % \
          (job, diff_id, phid, JENKINS_URL + BUILD_PATH)

    # CONSTRUCT A PAYLOAD
    params = {'job': job,
              'DIFF_ID': diff_id,
              'PHID': phid,
              'token': token}

    # POST REQUEST TO JENKINS
    requ = requests.get(JENKINS_URL + BUILD_PATH, params=params)

    # READ HTTP RETURN CODE
    if requ.status_code not in [200, 201]:
        print "Error! Status code %s returned for %s" % (requ.status_code, request.url)
        return "Not OK"
    return "OK"
