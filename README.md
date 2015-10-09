# github-bulk-integrations
A couple of quick scripts I wrote to bulk-add integrations (into slack), and to bulk-delete some slack (and hipchat) integrations. The Slack side of the integration will need to already exist (for a given channel) before you can use this.

See pydoc and / or '-h' output for more information on usage. The tools expect a file called <~/.github_token> containing only a github authentication token.

These are provided on a best-effort basis in case they're helpful for someone else, with or without adaption.

They require the 'requests' module (and, 'argparse' for github_find_stale_integrations.py), and were tested on Python 2.7.x, though should work with 2.6 or later.
