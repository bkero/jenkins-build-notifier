#!/usr/bin/env python
"""This is the flask app for intercepting and forwarding HTTP requests"""

from __future__ import print_function
from flask import Flask, request
import requests
import config

# URL to your Jenkins instance (with trailing slash)


APP = Flask(__name__)


@APP.route('/')
def index():
    """Drive-by connection or internet probe"""
    return "Go away"


@APP.route(config.build_path)
def build_by_token():
    """Connection sent HTTP URI conforming to spec"""
    # VALIDATE SOURCE IP
    if request.remote_addr != config.phabricator_ip:
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
        print("Error: phid %s is invalid in request %s" % (phid, request.url))
        return 'Bad Request'
    token = request.args.get('token')

    print("Forwarding request job: %s diff_id: %s phid: %s to %s" %
          (job, diff_id, phid, config.jenkins_url + config.build_path))

    # CONSTRUCT A PAYLOAD
    params = {'job': job,
              'DIFF_ID': diff_id,
              'PHID': phid,
              'token': token}

    # POST REQUEST TO JENKINS
    requ = requests.get(config.jenkins_url + config.build_path, params=params)

    # READ HTTP RETURN CODE
    if requ.status_code not in [200, 201]:
        print("Error! Status code %s returned for %s" %
              (requ.status_code, request.url))
        return "Not OK"
    return "OK"


if __name__ == '__main__':
    APP.run(host=config.listen, port=config.port)
