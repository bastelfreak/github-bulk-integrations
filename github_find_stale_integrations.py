#!/usr/bin/env python

"""
You should configure the file '.github_token' in your home directory
with a github API token. Additionally, Make sure to update 'OWNER_NAME'
near the top.

"""

__author__ = "William Yardley"

import argparse
import requests
import os
import sys
from os.path import expanduser

API_URL='https://api.github.com'
OWNER_NAME=''
github_token=str()

def _arg_parser():

    filename = os.path.basename(__file__)
    if filename.endswith('.pyc'):
        filename = filename[:-1]

    parser = argparse.ArgumentParser(prog=filename,
       description="""This tool will try to find Github hooks matching
       certain patterns, and, optionally, delete them.""")
    parser.add_argument('-p', '--pattern', required=True,
       help='''Literal pattern (not regexp) to look for in the URL (for
            hipchat, just use "hipchat" as the pattern)''')
    parser.add_argument('-d', '--delete', action='store_true',
       default=False, help='Delete hooks, rather than just identifying them.')

    return parser

def get_github_token():

    home = expanduser('~')
    cfg = open(home + '/.github_token', 'r')
    github_token = 'token ' + cfg.readlines()[0].rstrip()

    return github_token


def get_repos():

    repos = list()
    call = '%s/orgs/%s/repos' % (API_URL, OWNER_NAME)

    i = 1
    while True:
        params = {'page':i, 'per_page':100}
        response = requests.get(call, params=params,
              headers={'Authorization': github_token})
        if response.status_code == 200:
            if len(response.json()) > 0:
                for item in response.json():
                    repos.append(item['name'])
            else:
                break
        else:
            print >> sys.stderr, "Got error %s" % response.status_code
        i += 1

    return repos


def get_hooks(repo):

    datadict = dict()
    call = '%s/repos/%s/%s/hooks' % (API_URL, OWNER_NAME, repo)

    response = requests.get(call,
          headers={'Authorization': github_token})
    for item in response.json():
        if item['name'] == 'web':
            item_id = item['id']
            datadict[item_id] = item['config']['url']
        elif item['name'] == 'hipchat':
            item_id = item['id']
            datadict[item_id] = 'hipchat'

    return datadict

def delete_hook(repo, hook_id):

    call = '%s/repos/%s/%s/hooks/%s' % (API_URL, OWNER_NAME, repo, hook_id)
    response = requests.delete(call, headers={'Authorization': github_token})
    if response.status_code == 204:
        print >> sys.stderr, "Deleted hook %s on repo %s" % (hook_id, repo)
    else:
        print >> sys.stderr, ("Error %s for hook %s on repo %s" %
           (response.status_code, hook_id, repo))

def main():

    args = _p.parse_args()
    global github_token
    github_token=get_github_token()

    repos = get_repos()
    for repo in repos:
        hooks = get_hooks(repo)
        for hook_id, url in hooks.iteritems():
            if args.pattern in url:
                if args.delete:
                    delete_hook(repo, hook_id)
                else:
                    print "%s, %s, %s" % (repo, hook_id, url)

# Build pydoc from argparser help
_p = _arg_parser()
__doc__ += _p.format_help()

if __name__ == "__main__":
    main()
