#!/usr/bin/env python3

"""This tool takes in a JSON list of integrations in a file named
integrations.json (in current working directory), formatted like:

       { "room1": { "slackToken": "NNNN/XXXX/YYYYYYYYYYZ",
                       "repos": ["repo1", "repo2"]
                  },
         "room2": { "slackToken": "NNNN/ZZZZ/DDDDDDDDDDD",
                       "repos": ["repo1", "repo2"]
                  }
       }

You should also populate 'OWNER_NAME' at the top, and configure the file
'.github_token' in your home directory with a github API token.
"""
__author__ = "William Yardley"

from os.path import expanduser
import requests
import yaml


API_URL = 'https://api.github.com'
OWNER_NAME = 'voxpupuli'

def create_webhook(github_token, repo):
    ''' connects to github and creates an IRC hook '''
    call = '%s/repos/%s/%s/hooks' % (API_URL, OWNER_NAME, repo)
    payload = {"name": "irc",
               "active": True,
               "events": ["push", "pull_request"],
               "config": {
                   "server": "chat.freenode.net",
                   "room": "#voxpupuli-notifications",
                   "message_without_join": True,
                   "long_url": False,
                   "notice": False,
                   "no_colors": False,
                   "ssl": True
               }
              }
    response = requests.post(call, json=payload,
                             headers={'Authorization': github_token,
                                      'Accept': 'application/vnd.github.v3+json'})
    if response.status_code == 201:
        print("Added integration for %s" % repo)
    else:
        print("Error (repo %s): %s: code %s" % (repo,response.json(), response.status_code))

def main():
    ''' entrypoint. reads all modules and afterwards calls the create_webhook() for all modules'''
    home = expanduser('~')
    cfg = open(home + '/.github_token', 'r')
    github_token = 'token ' + cfg.readlines()[0].rstrip()

    with open('managed_modules.yml') as stream:
        try:
            repos = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    for repo in repos:
        create_webhook(github_token, repo)

if __name__ == "__main__":
    main()
