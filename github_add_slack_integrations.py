#!/usr/bin/env python

"""This tool takes in a JSON list of integrations in a file named
integrations.json (in current working directory), formatted like:

       { "channel1": { "slackToken": "NNNN/XXXX/YYYYYYYYYYZ",
                       "repos": ["repo1", "repo2"]
                      },
         "channel2": { "slackToken": "NNNN/ZZZZ/DDDDDDDDDDD",
                       "repos": ["repo1", "repo2"]
                      }
       } 

You should also populate 'OWNER_NAME' at the top, and configure the file
'.github_token' in your home directory with a github API token.
"""
__author__ = "William Yardley"

import requests
import sys
from os.path import expanduser

API_URL='https://api.github.com'
SLACK_BASE_URL = 'https://hooks.slack.com/services/'
OWNER_NAME=''

def create_webhook(github_token, repo, slack_webhook):

    call = '%s/repos/%s/%s/hooks' % (API_URL, OWNER_NAME, repo)
    payload = { "name": "web",
                "config": {
                   "url": slack_webhook,
                   "content_type": "json"
                 }
               }
    response = requests.post(call, json=payload,
          headers={'Authorization': github_token})
    if response.status_code == 201:
        print >> sys.stderr, "Added integration for %s" % repo
    else:
        errors = list()
        for error in response.json()['errors']:
            errors.append(error['message'])
        print >> sys.stderr, "Error (repo %s): %s: %s (code %s)" % (repo,
            response.json()['message'], ','.join(errors),
            response.status_code)

def main():

    home = expanduser('~')
    cfg = open(home + '/.github_token', 'r')
    github_token = 'token ' + cfg.readlines()[0].rstrip()

    with open('integrations.json') as data_file:    
        integrations = json.load(data_file)

    for channel, values in integrations.iteritems():
        slack_webhook = SLACK_BASE_URL + values['slackToken']
        for repo in values['repos']:
            create_webhook(github_token, repo, slack_webhook)

if __name__ == "__main__":
    main()
